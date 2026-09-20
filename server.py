#!/usr/bin/env python3
"""Local-only FlowPy web server. Python nodes execute with the local user's rights."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from engine import GraphError, SPECS, export_python, import_python, validate

ROOT = Path(__file__).resolve().parent
PACKAGE_ALLOWLIST = {'pandas', 'requests', 'numpy', 'openpyxl', 'pyyaml'}


def execute(graph, timeout=10):
    validate(graph)
    with tempfile.TemporaryDirectory(prefix='flowpy-') as folder:
        result_path = Path(folder) / 'result.json'
        process = subprocess.Popen([sys.executable, str(ROOT / 'worker.py'), str(result_path)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, cwd=str(ROOT), start_new_session=True)
        try:
            _, stderr = process.communicate(json.dumps(graph), timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            return {'ok': False, 'error': '执行超过 %s 秒，已停止。' % timeout, 'results': {}, 'logs': '', 'duration': timeout * 1000}
        if not result_path.exists():
            return {'ok': False, 'error': stderr[-2000:] or 'Python 进程意外退出。', 'results': {}, 'logs': ''}
        if result_path.stat().st_size > 5_000_000:
            return {'ok': False, 'error': '输出超过 5 MB，请缩小结果。', 'results': {}, 'logs': ''}
        return json.loads(result_path.read_text())


def package_catalog():
    """Small, explicit extension catalog; never pass arbitrary shell text to pip."""
    installed = set()
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], capture_output=True, text=True, timeout=8, check=True)
        installed = {item['name'].lower() for item in json.loads(result.stdout)}
    except (subprocess.SubprocessError, json.JSONDecodeError, KeyError):
        pass
    return [{'name': name, 'installed': name in installed} for name in sorted(PACKAGE_ALLOWLIST)]


def install_package(name):
    name = str(name).lower()
    if name not in PACKAGE_ALLOWLIST:
        raise GraphError('只能安装扩展目录中的包：' + '、'.join(sorted(PACKAGE_ALLOWLIST)))
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', name], capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise GraphError((result.stderr or result.stdout or '安装失败')[-1200:])
    return {'ok': True, 'name': name, 'message': name + ' 已安装，可在 Python 或 ImportModule 节点中使用。'}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'web'), **kwargs)

    def json_response(self, payload, status=200):
        data = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        # Refuse cross-origin requests and DNS rebinding to this local execution API.
        expected = {'127.0.0.1:%s' % self.server.server_port, 'localhost:%s' % self.server.server_port}
        host = self.headers.get('Host', '')
        origin = self.headers.get('Origin')
        if host not in expected or (origin and origin not in {'http://' + h for h in expected}):
            return self.json_response({'error': '仅允许本机同源请求。'}, 403)
        if self.headers.get_content_type() != 'application/json':
            return self.json_response({'error': '需要 application/json。'}, 415)
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 2_000_000:
                return self.json_response({'error': '请求为空或超过 2 MB。'}, 413)
            data = json.loads(self.rfile.read(size))
            path = urlparse(self.path).path
            if path == '/api/run':
                return self.json_response(execute(data['graph']))
            if path == '/api/export':
                return self.json_response({'source': export_python(data['graph'])})
            if path == '/api/import':
                return self.json_response(import_python(data['source']))
            if path == '/api/validate':
                validate(data['graph'])
                return self.json_response({'ok': True})
            if path == '/api/packages/install':
                return self.json_response(install_package(data['name']))
            return self.json_response({'error': '接口不存在。'}, 404)
        except (GraphError, ValueError, TypeError, KeyError, AttributeError) as exc:
            return self.json_response({'error': str(exc)}, 400)

    def do_GET(self):
        if self.path == '/api/examples':
            examples = [json.loads(path.read_text()) for path in sorted((ROOT / 'examples').glob('*.json'))]
            return self.json_response(examples)
        if self.path == '/api/specs':
            return self.json_response(SPECS)
        if self.path == '/api/packages':
            return self.json_response(package_catalog())
        super().do_GET()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print('FlowPy → http://127.0.0.1:%s' % args.port, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
