"""Separate process for each run; results go to a dedicated file, not stdout."""
import contextlib
import io
import json
import math
import sys
import time
from engine import source_body


class BoundedLog(io.StringIO):
    def write(self, text):
        remaining = 100000 - self.tell()
        if remaining > 0:
            super().write(text[:remaining])
        return len(text)


def safe_repr(value):
    try:
        return repr(value)[:50000]
    except Exception:
        return '<无法显示的 %s>' % type(value).__name__


def json_view(value, active=None, depth=0):
    """Convert only the UI snapshot; keep real objects intact between nodes."""
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, str):
        return value if len(value) <= 50000 else value[:50000] + '… <已截断>'
    if isinstance(value, float):
        return value if math.isfinite(value) else repr(value)
    if depth > 25:
        return '<嵌套过深，显示已截断>'
    if not isinstance(value, (dict, list, tuple)):
        return safe_repr(value)
    active = set() if active is None else active
    if id(value) in active:
        return '<循环引用>'
    active.add(id(value))
    try:
        if isinstance(value, dict):
            result = {}
            for i, (key, item) in enumerate(value.items()):
                if i >= 10000:
                    result['<截断>'] = '仅显示前 10000 项'
                    break
                key = key if isinstance(key, str) else safe_repr(key)
                result[key] = json_view(item, active, depth + 1)
            return result
        result = [json_view(item, active, depth + 1) for item in value[:10000]]
        if len(value) > 10000:
            result.append('<仅显示前 10000 项>')
        return result
    finally:
        active.remove(id(value))


def main():
    graph = json.load(sys.stdin)
    sys.stdin = io.StringIO(graph.get('stdin', ''))
    output = {'ok': False, 'results': {}, 'trace': []}
    log = BoundedLog()
    start = time.perf_counter()
    trace_values = {}
    try:
        namespace = {'__name__': 'flowpy_run'}
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            exec(compile(source_body(graph), '<graph>', 'exec'), namespace)
            output['results'] = namespace['run_graph'](trace_values)
        output['ok'] = True
    except BaseException as exc:
        output['error'] = str(exc) or type(exc).__name__
        output['results'] = trace_values
    output['trace'] = [
        {'node': node_id, 'status': 'skipped' if value is None else 'completed'}
        for node_id, value in trace_values.items()
    ]
    output['logs'] = log.getvalue()
    output['duration'] = round((time.perf_counter() - start) * 1000, 2)
    with open(sys.argv[1], 'w', encoding='utf-8') as file:
        json.dump(json_view(output), file, ensure_ascii=False, allow_nan=False)


if __name__ == '__main__':
    main()
