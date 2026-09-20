import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import GraphError, export_python, import_python, source_body, validate
from server import execute


def node(id, kind, **config):
    return {'id': id, 'type': kind, 'x': 10, 'y': 10, 'config': config}


def edge(source, out, target, inp):
    return {'source': source, 'out': out, 'target': target, 'in': inp}


def graph(nodes, edges=()):
    return {'version': 1, 'name': 'Test', 'nodes': nodes, 'edges': list(edges)}


class EngineTests(unittest.TestCase):
    def run_graph(self, g):
        result = execute(g)
        self.assertTrue(result['ok'], result)
        return result['results']

    def test_regex_match_shape_and_flags(self):
        g = graph([node('text', 'LoadText', text='ord-123456'), node('match', 'RegexMatch', pattern=r'ORD-(?P<id>\d{6})', flags=['IGNORECASE'])], [edge('text', 'text', 'match', 'text')])
        match = self.run_graph(g)['match']
        self.assertEqual(match, {'ok': True, 'groups': {'id': '123456'}, 'matches': ['ord-123456'], 'span': [0, 10]})
        g['nodes'][0]['config']['text'] = 'invalid'
        self.assertEqual(self.run_graph(g)['match'], {'ok': False, 'groups': {}, 'matches': [], 'span': None})

    def test_true_and_false_branches_do_not_execute_inactive_business(self):
        for condition in (True, False):
            g = graph([node('cond', 'If', condition=condition), node('yes', 'Python', code='result = "yes"'), node('no', 'Python', code='result = "no"')], [edge('cond', 'true', 'yes', 'gate'), edge('cond', 'false', 'no', 'gate')])
            result = self.run_graph(g)
            self.assertIsNone(result['no' if condition else 'yes'])
            self.assertEqual(result['yes' if condition else 'no']['value'], 'yes' if condition else 'no')

    def test_skips_propagate(self):
        g = graph([node('branch', 'If', condition=False), node('a', 'Python', code='raise Exception("must never run")'), node('b', 'Python', code='raise Exception("must never run")')], [edge('branch', 'true', 'a', 'gate'), edge('a', 'value', 'b', 'value')])
        self.assertEqual(self.run_graph(g)['b'], None)

    def test_findall_map_callback(self):
        g = graph([node('find', 'RegexFindall', text='1 2 3', pattern=r'\d+'), node('fn', 'Lambda', params='x', expression='int(x) * 2'), node('map', 'Map')], [edge('find', 'matches', 'map', 'items'), edge('fn', 'function', 'map', 'function')])
        self.assertEqual(self.run_graph(g)['map'], {'items': [2, 4, 6], 'count': 3})

    def test_filter_predicate_and_break_continue(self):
        g = graph([node('list', 'Constant', value=['ORD-123456', 'bad', 'ORD-234567']), node('predicate', 'Lambda', params='item', expression=r're.search(r"^ORD-\d{6}$", item) is not None'), node('filter', 'Filter')], [edge('list', 'value', 'filter', 'items'), edge('predicate', 'function', 'filter', 'function')])
        self.assertEqual(self.run_graph(g)['filter']['items'], ['ORD-123456', 'ORD-234567'])
        g = graph([node('list', 'Constant', value=[1, 2, 3, 4]), node('loop', 'Loop', code='if item == 2:\n    continue\nif item == 4:\n    break\nresult = item * 10')], [edge('list', 'value', 'loop', 'items')])
        self.assertEqual(self.run_graph(g)['loop']['items'], [10, 30])

    def test_function_signature_and_call_expansion(self):
        code = 'def f(a, /, *args, b=2, **kwargs):\n    return [a, list(args), b, kwargs]'
        g = graph([node('fn', 'Function', name='f', code=code), node('call', 'Call', args=[1, 3, 4], kwargs={'b': 8, 'name': 'A'})], [edge('fn', 'function', 'call', 'function')])
        self.assertEqual(self.run_graph(g)['call']['value'], [1, [3, 4], 8, {'name': 'A'}])

    def test_async_decorators_and_closure(self):
        code = 'def decorator(fn):\n    async def wrapped(x):\n        return await fn(x) + 1\n    return wrapped\n@decorator\nasync def transform(x):\n    return x * 2'
        g = graph([node('fn', 'Function', name='transform', code=code), node('call', 'Call', args=[3])], [edge('fn', 'function', 'call', 'function')])
        self.assertEqual(self.run_graph(g)['call']['value'], 7)
        g = graph([node('val', 'Constant', value=5), node('fn', 'Lambda', params='x', expression='x + value'), node('call', 'Call', args=[3])], [edge('val', 'value', 'fn', 'value'), edge('fn', 'function', 'call', 'function')])
        self.assertEqual(self.run_graph(g)['call']['value'], 8)

    def test_bound_method_and_higher_order(self):
        g = graph([node('fn', 'Python', code='result = "hello {}".format'), node('call', 'Call', args=['world'])], [edge('fn', 'value', 'call', 'function')])
        self.assertEqual(self.run_graph(g)['call']['value'], 'hello world')

    def test_regex_sub_callback_split_and_switch(self):
        g = graph([node('fn', 'Lambda', params='m', expression='str(int(m.group()) * 2)'), node('sub', 'RegexSub', text='a1 b2', pattern=r'\d+'), node('split', 'RegexSplit', pattern=r'\s+'), node('rules', 'RegexSwitch', text='https://example.com', rules=[{'pattern': '^http', 'case': 'url'}, {'pattern': '.+', 'case': 'plain'}]), node('switch', 'Switch', cases=['url'])], [edge('fn', 'function', 'sub', 'repl'), edge('sub', 'text', 'split', 'text'), edge('rules', 'case', 'switch', 'value')])
        result = self.run_graph(g)
        self.assertEqual(result['split']['parts'], ['a2', 'b4'])
        self.assertTrue(result['switch']['matched'])

    def test_cycle_types_duplicate_input_and_invalid_ports(self):
        with self.assertRaises(GraphError):
            validate(graph([node('a','Python'),node('b','Python')],[edge('a','value','b','value'),edge('b','value','a','value')]))
        with self.assertRaises(GraphError):
            validate(graph([node('a','LoadText'),node('b','If')],[edge('a','text','b','condition')]))
        with self.assertRaises(GraphError):
            validate(graph([node('a','LoadText'),node('b','RegexMatch')],[edge('a','text','b','text'),edge('a','text','b','text')]))
        with self.assertRaises(GraphError):
            validate(graph([node('a','LoadText'),node('b','RegexMatch')],[edge('a','missing','b','text')]))

    def test_errors_include_node_and_partial_results(self):
        result = execute(graph([node('a','Constant',value=1),node('bad','RegexMatch',text='x',pattern='[')]))
        self.assertFalse(result['ok'])
        self.assertIn('bad',result['error'])
        self.assertEqual(result['results']['a']['value'],1)

    def test_timeout(self):
        result = execute(graph([node('loop','Python',code='while True:\n    pass')]),timeout=.2)
        self.assertFalse(result['ok'])
        self.assertIn('已停止',result['error'])

    def test_roundtrip_and_standalone_python(self):
        g = graph([node('a','RegexMatch',text='ORD-123456',pattern=r'ORD-(?P<id>\d{6})')])
        source = export_python(g)
        restored = import_python(source)
        self.assertEqual(restored['mode'],'roundtrip')
        self.assertEqual(restored['graph'],g)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'standalone.py'
            path.write_text(source)
            result = subprocess.run([sys.executable,str(path)],cwd=folder,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('123456',result.stdout)

    def test_modified_source_preserved_and_imported_module_scope(self):
        g = graph([node('a','Python',code='result = 2')])
        source = export_python(g).replace('result = 2','result = 9')
        self.assertEqual(import_python(source)['mode'],'opaque')
        imported=import_python('import re\npattern = r"\\d+"\ndef find(s):\n    return re.findall(pattern,s)\nresult = find("a12b34")\n')
        self.assertEqual(self.run_graph(imported['graph'])['python1']['value'],['12','34'])

    def test_bool_and_iteration_contracts(self):
        result=execute(graph([node('a','Constant',value=[1]),node('b','Filter',code='result = item')],[edge('a','value','b','items')]))
        self.assertFalse(result['ok'])
        self.assertIn('bool',result['error'])
        result=execute(graph([node('a','Constant',value=[1,2]),node('b','Map',limit=1)],[edge('a','value','b','items')]))
        self.assertFalse(result['ok'])
        self.assertIn('上限',result['error'])


if __name__ == '__main__':
    unittest.main()
