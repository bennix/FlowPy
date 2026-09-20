"""Every preserved teaching flow must execute, round-trip, and run standalone."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from engine import export_python, import_python
from server import execute
from test_python_semantics import run_direct
from test_engine import node, edge, graph

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT/'examples'/(name+'.json')).read_text())


class CurriculumExamplesTests(unittest.TestCase):
    def test_all_course_weeks_have_saved_examples(self):
        weeks={json.loads(path.read_text())['week'] for path in (ROOT/'examples').glob('*.json')}
        self.assertTrue(set(range(2,12)).issubset(weeks))

    def test_bmi_invalid_inputs(self):
        for weight,height in [(0,1.75),(-10,1.75),(70,0),(70,-1.75),('bad',1.75)]:
            with self.subTest(weight=weight,height=height):
                g=load('w02_bmi')
                g['nodes'][0]['config']['value']={'weight':weight,'height':height}
                self.assertFalse(execute(g)['ok'])

    def test_bmi_classification_boundaries(self):
        for bmi,expected in [(18.49,'偏瘦'),(18.5,'正常'),(23.99,'正常'),(24,'超重'),(27.99,'超重'),(28,'肥胖')]:
            with self.subTest(bmi=bmi):
                g=load('w02_bmi')
                g['nodes'][0]['config']['value']={'weight':bmi*4,'height':2}
                self.assertEqual(run_direct(g)['out']['value']['category'],expected)

    def test_interactive_input_exhaustion_is_clear_error(self):
        g=load('w02_interactive');g['stdin']='70\n'
        result=execute(g)
        self.assertFalse(result['ok'])
        self.assertIn('EOF',result['error'])

    def test_guess_game_all_difficulties_and_loss(self):
        for level,target in [('easy',11),('normal',21),('hard',42)]:
            with self.subTest(level=level):
                g=load('w05_guess_number');g['stdin']=f'{level}\n{target}\n'
                result=execute(g)
                self.assertTrue(result['ok'],result)
                self.assertTrue(result['results']['out']['value']['won'])
                self.assertEqual(result['results']['out']['value']['attempts'],1)
        g=load('w05_guess_number');g['stdin']='hard\n1\n2\n3\n'
        result=execute(g)
        self.assertFalse(result['results']['out']['value']['won'])
        self.assertEqual(result['results']['out']['value']['attempts'],3)
        g['stdin']='unknown\n'
        self.assertFalse(execute(g)['ok'])

    def test_loan_zero_interest_and_invalid_terms(self):
        g=load('w08_loan')
        g['nodes'][0]['config']['value']={'principal':12000,'annual_rate':0,'months':12}
        self.assertEqual(run_direct(g)['out']['value']['monthly_payment'],1000)
        for payload in [{'principal':-1,'annual_rate':0,'months':12},{'principal':100,'annual_rate':-1,'months':12},{'principal':100,'annual_rate':0,'months':0},{'principal':100,'annual_rate':0,'months':1.5}]:
            with self.subTest(payload=payload):
                g['nodes'][0]['config']['value']=payload
                with self.assertRaises(RuntimeError):run_direct(g)

    def test_lottery_many_seeds_invariants(self):
        g=load('w08_lottery')
        for seed in range(50):
            with self.subTest(seed=seed):
                g['nodes'][0]['config']['value']={'seed':seed}
                value=run_direct(g)['out']['value']
                self.assertEqual(len(set(value['red'])),6)
                self.assertEqual(value['red'],sorted(value['red']))
                self.assertTrue(all(1<=n<=33 for n in value['red']))
                self.assertTrue(1<=value['blue']<=16)

    def test_salary_defaults_and_zero_tax(self):
        g=load('w09_salary_functions')
        call=next(n for n in g['nodes'] if n['type']=='Call')
        call['config']['kwargs']={}
        self.assertEqual(run_direct(g)['out']['value'],{'gross':11500,'net':10350.0,'employee':'anonymous'})
        call['config']['kwargs']={'tax_rate':0}
        self.assertEqual(run_direct(g)['out']['value']['net'],11500)
        call['config']['kwargs']={'tax_rate':1.5}
        with self.assertRaises(RuntimeError):run_direct(g)

    def test_module_input_validation_and_namespace(self):
        g=load('w10_modular_gradebook')
        call=next(n for n in g['nodes'] if n['type']=='Call')
        for records in [{},{'Alice':101},{'Alice':-1}]:
            with self.subTest(records=records):
                call['config']['args']=[records]
                with self.assertRaises(RuntimeError):run_direct(g)
        g=graph([node('module','Module',name='teaching_math',code='base=5\ndef add(x):\n    return x+base'),node('get','Get',path='add'),node('call','Call',args=[7])],[edge('module','value','get','value'),edge('get','value','call','function')])
        self.assertEqual(run_direct(g)['call']['value'],12)

    def test_real_python_module_can_be_imported_downstream(self):
        g=graph([node('module','Module',name='teaching_example',code='VALUE = 42'),node('consumer','Python',code='import teaching_example\nresult=teaching_example.VALUE')],[edge('module','value','consumer','value')])
        self.assertEqual(run_direct(g)['consumer']['value'],42)

    def test_pandas_empty_result_and_invalid_number(self):
        if importlib.util.find_spec('pandas') is None:self.skipTest('optional pandas is not installed')
        g=load('w11_basic_pandas')
        g['nodes'][0]['config']['value']=[{'name':'A','score':'20'}]
        result=execute(g)
        self.assertTrue(result['ok'],result)
        self.assertEqual(result['results']['out']['value']['records'],[])
        g['nodes'][0]['config']['value']=[{'name':'A','score':'bad'}]
        self.assertFalse(execute(g)['ok'])


def make_example_test(path):
    def test(self):
        g=json.loads(path.read_text())
        if 'pandas' in path.stem and importlib.util.find_spec('pandas') is None:
            self.skipTest('optional pandas is not installed')
        with self.subTest(stage='isolated_worker'):
            result=execute(g)
            self.assertTrue(result['ok'],result)
            for nid,expected in g['checks'].items():self.assertEqual(result['results'][nid],expected)
        with self.subTest(stage='roundtrip'):
            self.assertEqual(import_python(export_python(g))['graph'],g)
        with self.subTest(stage='saved_source_matches_graph'):
            self.assertEqual(path.with_suffix('.py').read_text(),export_python(g))
        with self.subTest(stage='standalone_no_editor_imports'),tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'workflow.py';source.write_text(export_python(g))
            runner='import runpy,sys,io,json; g=runpy.run_path(sys.argv[1]); sys.stdin=io.StringIO(sys.argv[2]); result=g["run_graph"](); print("\\n__RESULT__"+json.dumps(result["out"],ensure_ascii=False,default=repr))'
            proc=subprocess.run([sys.executable,'-c',runner,str(source),g.get('stdin','')],cwd=folder,capture_output=True,text=True,timeout=15)
            self.assertEqual(proc.returncode,0,proc.stderr)
            actual=json.loads(proc.stdout.rsplit('__RESULT__',1)[1])
            self.assertEqual(actual,g['checks']['out'])
    return test


for path in sorted((ROOT/'examples').glob('*.json')):
    setattr(CurriculumExamplesTests,'test_saved_'+path.stem,make_example_test(path))
