import http.client
import json
from pathlib import Path
import threading
import unittest
from http.server import ThreadingHTTPServer

from server import Handler
from test_engine import node, edge, graph
from test_python_semantics import run_direct


class QuietHandler(Handler):
    def log_message(self,*args):
        pass


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.port=cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()

    def request(self,path,data=None,headers=None,method='POST',raw=None):
        connection=http.client.HTTPConnection('127.0.0.1',self.port,timeout=15)
        request_headers={'Content-Type':'application/json'}
        request_headers.update(headers or {})
        body=raw if raw is not None else json.dumps(data or {})
        connection.request(method,path,body if method=='POST' else None,request_headers)
        response=connection.getresponse();status=response.status
        content=response.read().decode();connection.close()
        return status,json.loads(content) if response.headers.get('Content-Type','').startswith('application/json') else content

    def test_home_and_specs(self):
        status,html=self.request('/',method='GET')
        self.assertEqual(status,200);self.assertIn('FlowPy',html)
        status,specs=self.request('/api/specs',method='GET')
        self.assertEqual(status,200);self.assertIn('Function',specs);self.assertIn('Assert',specs)

    def test_examples_catalog(self):
        status,examples=self.request('/api/examples',method='GET')
        self.assertEqual(status,200);self.assertGreaterEqual(len(examples),22)
        self.assertTrue(all(e['verified'] for e in examples))

    def test_run_input_and_output(self):
        g=graph([node('a','Python',code='result = int(input()) * 2')]);g['stdin']='21\n'
        status,result=self.request('/api/run',{'graph':g})
        self.assertEqual(status,200);self.assertTrue(result['ok']);self.assertEqual(result['results']['a']['value'],42)

    def test_export_import_api(self):
        g=graph([node('a','Constant',value=42)])
        status,export=self.request('/api/export',{'graph':g})
        self.assertEqual(status,200)
        status,imported=self.request('/api/import',{'source':export['source']})
        self.assertEqual(status,200);self.assertEqual(imported['graph'],g)

    def test_malformed_json_and_missing_graph(self):
        self.assertEqual(self.request('/api/run',raw='{bad')[0],400)
        self.assertEqual(self.request('/api/run',{})[0],400)
        self.assertEqual(self.request('/api/run',{'graph':None})[0],400)

    def test_unknown_api(self):
        self.assertEqual(self.request('/api/missing')[0],404)

    def test_wrong_content_type(self):
        self.assertEqual(self.request('/api/run',headers={'Content-Type':'text/plain'})[0],415)

    def test_cross_origin_is_rejected(self):
        self.assertEqual(self.request('/api/run',headers={'Origin':'https://other.example'})[0],403)

    def test_invalid_host_is_rejected(self):
        self.assertEqual(self.request('/api/run',headers={'Host':'attacker.example'})[0],403)

    def test_local_origin_is_accepted(self):
        status,result=self.request('/api/run',{'graph':graph([node('a','Constant',value=1)])},headers={'Origin':'http://127.0.0.1:%s'%self.port})
        self.assertEqual(status,200);self.assertTrue(result['ok'])

    def test_assertion_pass_and_failure(self):
        for value,expected,passed in [(42,42,True),([1,2],[1,2],True),(42,43,False)]:
            with self.subTest(value=value,expected=expected):
                g=graph([node('a','Constant',value=value),node('check','Assert',expected=expected)],[edge('a','value','check','value')])
                status,result=self.request('/api/run',{'graph':g})
                self.assertEqual(status,200);self.assertEqual(result['ok'],passed)
                if passed:self.assertTrue(result['results']['check']['passed'])
                else:self.assertIn('预期',result['error'])

    def test_assertion_connected_expectation(self):
        g=graph([node('a','Constant',value=42),node('expected','Constant',value=42),node('check','Assert',expected=999)],[edge('a','value','check','value'),edge('expected','value','check','expected')])
        self.assertTrue(run_direct(g)['check']['passed'])
