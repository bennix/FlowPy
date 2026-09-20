"""Python behavior matrix; every entry runs generated source, not a mock evaluator."""
import ast
import base64
import copy
import hashlib
import json
import random
import re
import unittest

from test_engine import node, edge, graph
from engine import GraphError, export_python, import_python, source_body, validate
from server import execute


def run_direct(g):
    scope = {'__name__': 'test_generated_module'}
    exec(compile(source_body(g), '<generated>', 'exec'), scope)
    return scope['run_graph']()


def call_graph(code, args=None, kwargs=None, name='f'):
    return graph([node('fn','Function',name=name,code=code),node('call','Call',args=args or [],kwargs=kwargs or {})],[edge('fn','function','call','function')])


FUNCTION_CASES = [
 ('no_arguments','def f():\n    return 42',[],{},42),
 ('positional','def f(a,b):\n    return a+b',[2,3],{},5),
 ('keyword_order','def f(a,b):\n    return a-b',[],{'b':3,'a':7},4),
 ('defaults','def f(a=4,b=5):\n    return a*b',[],{},20),
 ('default_override','def f(a=4,b=5):\n    return a*b',[3],{'b':6},18),
 ('positional_only','def f(a,/,b=2):\n    return a+b',[3],{'b':4},7),
 ('keyword_only','def f(*,value):\n    return value',[],{'value':8},8),
 ('varargs','def f(*args):\n    return sum(args)',[1,2,3,4],{},10),
 ('kwargs','def f(**kwargs):\n    return sorted(kwargs.items())',[],{'b':2,'a':1},[('a',1),('b',2)]),
 ('mixed_signature','def f(a,/,b=2,*args,c=3,**kwargs):\n    return [a,b,args,c,kwargs]',[1,4,5,6],{'c':9,'z':10},[1,4,(5,6),9,{'z':10}]),
 ('annotations','def f(x: int) -> str:\n    return str(x)',[12],{},'12'),
 ('recursive','def f(n):\n    return 1 if n < 2 else n*f(n-1)',[6],{},720),
 ('nested_closure','def f(x):\n    def add(y):\n        return x+y\n    return add(7)',[3],{},10),
 ('nonlocal','def f():\n    x=0\n    def inner():\n        nonlocal x\n        x += 1\n        return x\n    return [inner(),inner()]',[],{},[1,2]),
 ('lambda_as_def','f = lambda x, y=2: x*y',[4],{},8),
 ('lambda_varargs','f = lambda *args, **kwargs: sum(args)+sum(kwargs.values())',[1,2],{'a':3},6),
 ('decorator','def double(fn):\n    def wrapper(*args,**kwargs):\n        return fn(*args,**kwargs)*2\n    return wrapper\n@double\ndef f(x):\n    return x+1',[3],{},8),
 ('decorator_factory','def times(n):\n    def decorate(fn):\n        return lambda x: n*fn(x)\n    return decorate\n@times(3)\ndef f(x):\n    return x+2',[4],{},18),
 ('async','async def f(x):\n    await asyncio.sleep(0)\n    return x+1',[5],{},6),
 ('classmethod','class C:\n    base=3\n    @classmethod\n    def method(cls,x):\n        return cls.base+x\nf=C.method',[5],{},8),
 ('staticmethod','class C:\n    @staticmethod\n    def method(x):\n        return x*2\nf=C.method',[5],{},10),
 ('bound_method','class C:\n    def __init__(self,x):\n        self.x=x\n    def method(self,y):\n        return self.x+y\nf=C(5).method',[6],{},11),
 ('callable_instance','class C:\n    def __call__(self,x):\n        return x*3\nf=C()',[4],{},12),
 ('partial','from functools import partial\ndef add(a,b):\n    return a+b\nf=partial(add,7)',[2],{},9),
 ('generator_consumed','def generate():\n    yield 1\n    yield 2\ndef f():\n    return list(generate())',[],{},[1,2]),
 ('function_returning_function','def factory(n):\n    return lambda x: x+n\nf=factory(8)',[2],{},10),
 ('comprehension','def f(values):\n    return {x:x*x for x in values}',[[1,2,3]],{},{1:1,2:4,3:9}),
 ('unicode_identifiers','def 函数(值):\n    return 值.upper()\nf=函数',['中文abc'],{},'中文ABC'),
 ('custom_awaitable','class Awaitable:\n    def __await__(self):\n        async def inner():\n            return 17\n        return inner().__await__()\ndef f():\n    return Awaitable()',[],{},17),
]

FUNCTION_ERROR_CASES = [
 ('missing_required','def f(a):\n    return a',[],{}),
 ('too_many_positionals','def f(a):\n    return a',[1,2],{}),
 ('duplicate_binding','def f(a):\n    return a',[1],{'a':2}),
 ('positional_only_keyword','def f(a,/):\n    return a',[],{'a':2}),
 ('keyword_only_positional','def f(*,a):\n    return a',[2],{}),
 ('unexpected_keyword','def f(a):\n    return a',[2],{'b':3}),
 ('function_exception','def f():\n    raise ValueError("intentional failure")',[],{}),
 ('not_callable','f = 42',[],{}),
]


class PythonSemanticsTests(unittest.TestCase):
    def test_call_value_precedes_expanded_args(self):
        g=call_graph('def f(a,b,*,c):\n    return [a,b,c]',[2],{'c':3})
        g['nodes'].insert(0,node('value','Constant',value=1))
        g['edges'].append(edge('value','value','call','value'))
        self.assertEqual(run_direct(g)['call']['value'],[1,2,3])

    def test_connected_args_and_kwargs_override_config(self):
        g=call_graph('def f(a,b):\n    return a+b',[100],{'b':100})
        g['nodes'] += [node('args','Constant',value=[3]),node('kwargs','Constant',value={'b':4})]
        g['edges'] += [edge('args','value','call','args'),edge('kwargs','value','call','kwargs')]
        self.assertEqual(run_direct(g)['call']['value'],7)

    def test_async_map_and_filter(self):
        for kind,code,expected in [('Map','async def f(x):\n    return x*2',[2,4,6]),('Filter','async def f(x):\n    return x%2 == 1',[1,3])]:
            with self.subTest(kind=kind):
                g=graph([node('list','Constant',value=[1,2,3]),node('f','Function',name='f',code=code),node('loop',kind)],[edge('list','value','loop','items'),edge('f','function','loop','function')])
                self.assertEqual(run_direct(g)['loop']['items'],expected)

    def test_mutable_default_obeys_python_function_lifetime(self):
        g=graph([node('list','Constant',value=[1,2,3]),node('f','Function',name='f',code='def f(x, seen=[]):\n    seen.append(x)\n    return list(seen)'),node('map','Map')],[edge('list','value','map','items'),edge('f','function','map','function')])
        self.assertEqual(run_direct(g)['map']['items'],[[1],[1,2],[1,2,3]])
        self.assertEqual(run_direct(g)['map']['items'],[[1],[1,2],[1,2,3]])

    def test_function_returning_closure_can_be_called_again(self):
        g=call_graph('def f(n):\n    return lambda x: x+n',[5])
        g['nodes'].append(node('second','Call',args=[7]))
        g['edges'].append(edge('call','value','second','function'))
        self.assertEqual(run_direct(g)['second']['value'],12)

    def test_generator_can_flow_to_consumer(self):
        g=call_graph('def f():\n    yield 1\n    yield 2')
        g['nodes'].append(node('consume','Python',code='result=list(value)'))
        g['edges'].append(edge('call','value','consume','value'))
        self.assertEqual(run_direct(g)['consume']['value'],[1,2])

    def test_invalid_python_detected_before_export(self):
        for code in ['break','continue','await asyncio.sleep(0)','def bad(:\n  pass']:
            with self.subTest(code=code),self.assertRaises(GraphError):
                export_python(graph([node('bad','Python',code=code)]))

    def test_python_logs_and_system_exit(self):
        result=execute(graph([node('n','Python',code='print("你好")\nimport sys\nprint("warning",file=sys.stderr)\nresult=42')]))
        self.assertTrue(result['ok'])
        self.assertIn('你好',result['logs'])
        self.assertIn('warning',result['logs'])
        result=execute(graph([node('n','Python',code='raise SystemExit(2)')]))
        self.assertFalse(result['ok'])

    def test_complex_output_serialization(self):
        result=execute(graph([node('n','Python',code='result = {("tuple",1): {1,2}, "cycle": []}\nresult["cycle"].append(result)')]))
        self.assertTrue(result['ok'],result)
        self.assertIn('cycle',result['results']['n']['value'])

    def test_nonfinite_numbers_remain_valid_json(self):
        result=execute(graph([node('n','Python',code='result = [float("nan"),float("inf"),float("-inf")]')]))
        json.dumps(result,allow_nan=False)

    def test_log_bound(self):
        result=execute(graph([node('n','Python',code='print("x" * 200000)\nresult = True')]))
        self.assertTrue(result['ok'])
        self.assertLessEqual(len(result['logs']),100000)


for name,code,args,kwargs,expected in FUNCTION_CASES:
    def test(self,code=code,args=args,kwargs=kwargs,expected=expected):
        self.assertEqual(run_direct(call_graph(code,args,kwargs))['call']['value'],expected)
    setattr(PythonSemanticsTests,'test_function_'+name,test)
for name,code,args,kwargs in FUNCTION_ERROR_CASES:
    def test(self,code=code,args=args,kwargs=kwargs):
        with self.assertRaises(RuntimeError):
            run_direct(call_graph(code,args,kwargs))
    setattr(PythonSemanticsTests,'test_binding_error_'+name,test)


class GraphSemanticsTests(unittest.TestCase):
    def test_map_subgraph_item_index_and_acc(self):
        body=graph([node('item','Item'),node('fn','Python',code='result = value + sum(items)'),node('out','Output')],[edge('item','index','fn','value'),edge('item','acc','fn','items'),edge('fn','value','out','value')])
        g=graph([node('list','Constant',value=['a','b','c','d']),node('map','Map',body=body)],[edge('list','value','map','items')])
        self.assertEqual(run_direct(g)['map']['items'],[0,1,3,7])
        self.assertEqual(import_python(export_python(g))['graph'],g)

    def test_filter_subgraph_regex_ok(self):
        body=graph([node('item','Item'),node('regex','RegexMatch',pattern=r'^ORD-\d{6}$'),node('out','Output')],[edge('item','value','regex','text'),edge('regex','ok','out','value')])
        g=graph([node('list','Constant',value=['ORD-123456','invalid','ORD-654321']),node('filter','Filter',body=body)],[edge('list','value','filter','items')])
        self.assertEqual(run_direct(g)['filter']['items'],['ORD-123456','ORD-654321'])

    def test_nested_map_subgraphs(self):
        inner=graph([node('item','Item'),node('fn','Python',code='result=value*2'),node('out','Output')],[edge('item','value','fn','value'),edge('fn','value','out','value')])
        outer=graph([node('item','Item'),node('map','Map',body=inner),node('out','Output')],[edge('item','value','map','items'),edge('map','items','out','value')])
        g=graph([node('list','Constant',value=[[1,2],[3]]),node('map','Map',body=outer)],[edge('list','value','map','items')])
        self.assertEqual(run_direct(g)['map']['items'],[[2,4],[6]])

    def test_nested_error_has_both_node_ids(self):
        body=graph([node('broken','Python',code='raise ValueError("oops")'),node('out','Output')],[edge('broken','value','out','value')])
        g=graph([node('list','Constant',value=[1]),node('outer','Map',body=body)],[edge('list','value','outer','items')])
        with self.assertRaisesRegex(RuntimeError,'outer.*broken'):
            run_direct(g)

    def test_subgraph_requires_single_output(self):
        for nodes in [[node('item','Item')],[node('a','Output'),node('b','Output')]]:
            with self.subTest(nodes=nodes),self.assertRaises(GraphError):
                validate(graph([node('map','Map',body=graph(nodes))]))

    def test_switch_independent_case_ports_and_default(self):
        for value,expected in [('url','url'),('id','id'),('other','default')]:
            g=graph([node('val','Constant',value=value),node('s','Switch',cases=['url','id']),node('url','Output',value='url'),node('id','Output',value='id'),node('default','Output',value='default')],[edge('val','value','s','value'),edge('s','case_0','url','gate'),edge('s','case_1','id','gate'),edge('s','default','default','gate')])
            with self.subTest(value=value):
                results=run_direct(g)
                active=[key for key in ['url','id','default'] if results[key] is not None]
                self.assertEqual(active,[expected])

    def test_switch_duplicate_values_choose_first(self):
        g=graph([node('v','Constant',value='a'),node('s','Switch',cases=['a','a'])],[edge('v','value','s','value')])
        result=run_direct(g)['s']
        self.assertTrue(result['case_0'])
        self.assertFalse(result['case_1'])

    def test_topological_order_independent_of_node_array(self):
        nodes=[node('a','Constant',value=2),node('b','Python',code='result=value*3'),node('c','Python',code='result=value+4')]
        edges=[edge('a','value','b','value'),edge('b','value','c','value')]
        rng=random.Random(1234)
        for _ in range(20):
            rng.shuffle(nodes)
            self.assertEqual(run_direct(graph(nodes,edges))['c']['value'],10)

    def test_null_result_is_not_a_skipped_node(self):
        g=graph([node('a','Python',code='result=None'),node('b','Python',code='result = value is None')],[edge('a','value','b','value')])
        self.assertTrue(run_direct(g)['b']['value'])

    def test_gate_must_be_bool_at_runtime(self):
        g=graph([node('v','Constant',value='true'),node('out','Output')],[edge('v','value','out','gate')])
        with self.assertRaisesRegex(RuntimeError,'bool'):
            run_direct(g)

    def test_get_nested_list_and_dict(self):
        g=graph([node('v','Constant',value={'rows':[{'id':'123'}]}),node('get','Get',path='rows.0.id')],[edge('v','value','get','value')])
        self.assertEqual(run_direct(g)['get']['value'],'123')

    def test_empty_lists(self):
        for kind in ['Map','Filter','Loop']:
            with self.subTest(kind=kind):
                g=graph([node('list','Constant',value=[]),node('loop',kind,code='raise Exception("never")')],[edge('list','value','loop','items')])
                self.assertEqual(run_direct(g)['loop'],{'items':[],'count':0})

    def test_bad_shapes_raise_graph_error(self):
        for bad in [None,[],{'nodes':'bad'},{'nodes':[None]},{'nodes':[node('a','Python')],'edges':[None]},graph([{'id':1,'type':'Python'}]),graph([{'id':'x','type':'Python','config':None}])]:
            with self.subTest(bad=bad),self.assertRaises(GraphError):
                validate(bad)

    def test_limits_and_invalid_nodes(self):
        cases=[graph([]),graph([node('a','Missing')]),graph([node('a','Python'),node('a','Python')]),graph([node('1bad','Python')]),graph([node('a','Python')],[edge('a','value','missing','value')]),graph([node('n'+str(i),'Constant') for i in range(201)])]
        for bad in cases:
            with self.subTest(size=len(bad['nodes'])),self.assertRaises(GraphError):
                validate(bad)

    def test_import_rejects_syntax_error(self):
        with self.assertRaises(GraphError):
            import_python('def broken(:')

    def test_roundtrip_crlf(self):
        g=graph([node('a','Constant',value='中文')])
        self.assertEqual(import_python(export_python(g).replace('\n','\r\n'))['mode'],'roundtrip')

    def test_forged_metadata_cannot_override_actual_source(self):
        original=graph([node('a','Constant',value=1)])
        forged=graph([node('a','Constant',value=999)])
        lines=export_python(original).splitlines(keepends=True)
        lines[0]='# FlowPy graph v1: '+base64.b64encode(json.dumps(forged).encode()).decode()+'\n'
        self.assertEqual(import_python(''.join(lines))['mode'],'opaque')


class RegexParityTests(unittest.TestCase):
    def test_regex_matches_python_re_across_matrix(self):
        texts=['','中文 ORD-123456\nord-654321','a,b;;c','1 22 333','abc\ndef','Ångström','aaa']
        patterns=[r'ORD-(?P<id>\d{6})',r'\d+',r'(?P<letter>[a-z])',r'^.',r'a.*a',r'[,;]+',r'(?=a)',r'(?P<a>a)?b',r'\w+']
        flag_sets=[[],['IGNORECASE'],['MULTILINE'],['DOTALL'],['IGNORECASE','MULTILINE']]
        for text in texts:
            for pattern in patterns:
                for flags in flag_sets:
                    with self.subTest(text=text,pattern=pattern,flags=flags):
                        compiled_flags=0
                        for flag in flags:compiled_flags |= getattr(re,flag)
                        g=graph([node('match','RegexMatch',text=text,pattern=pattern,flags=flags),node('find','RegexFindall',text=text,pattern=pattern,flags=flags),node('split','RegexSplit',text=text,pattern=pattern,flags=flags),node('sub','RegexSub',text=text,pattern=pattern,flags=flags,repl='X')])
                        results=run_direct(g)
                        match=re.search(pattern,text,compiled_flags)
                        self.assertEqual(results['match']['ok'],match is not None)
                        self.assertEqual(results['match']['groups'],match.groupdict() if match else {})
                        self.assertEqual(results['find']['matches'],re.findall(pattern,text,compiled_flags))
                        self.assertEqual(results['split']['parts'],re.split(pattern,text,flags=compiled_flags))
                        self.assertEqual(results['sub']['text'],re.sub(pattern,'X',text,flags=compiled_flags))

    def test_verbose_pattern(self):
        g=graph([node('r','RegexMatch',text='ORD-123456',pattern='ORD-  # prefix\n(?P<id>\\d{6})',flags=['VERBOSE'])])
        self.assertEqual(run_direct(g)['r']['groups'],{'id':'123456'})

    def test_sub_named_backreference(self):
        g=graph([node('r','RegexSub',text='ORD-123456',pattern=r'ORD-(?P<id>\d+)',repl=r'ID=\g<id>')])
        self.assertEqual(run_direct(g)['r']['text'],'ID=123456')

    def test_invalid_regex_and_flags(self):
        with self.assertRaises(RuntimeError):run_direct(graph([node('r','RegexMatch',text='x',pattern='[')]))
        with self.assertRaises(GraphError):export_python(graph([node('r','RegexMatch',flags=['BAD'])]))

    def test_priority_rules_no_match_and_groups(self):
        g=graph([node('r','RegexSwitch',text='ORD-123',rules=[{'pattern':r'ORD-(?P<id>\d+)','case':'order'},{'pattern':'.+','case':'fallback'}])])
        self.assertEqual(run_direct(g)['r'],{'case':'order','groups':{'id':'123'},'ok':True})
        g['nodes'][0]['config']['text']=''
        self.assertEqual(run_direct(g)['r'],{'case':None,'groups':{},'ok':False})
