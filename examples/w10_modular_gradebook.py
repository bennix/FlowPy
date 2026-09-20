# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5qih5Z2X5YyW6YeN5p6E77ya5oiQ57up566h55CGIiwid2VlayI6MTAsImRlc2NyaXB0aW9uIjoiTW9kdWxlIOWumuS5ieeLrOeri+WRveWQjeepuumXtCDihpIgR2V0IOaPkOWPliBzdW1tYXJpemUg4oaSIENhbGwg5Lyg5YWl5oiQ57up44CCIiwic3RkaW4iOiIiLCJub2RlcyI6W3siaWQiOiJtb2R1bGUiLCJ0eXBlIjoiTW9kdWxlIiwidGl0bGUiOiJNb2R1bGUiLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJuYW1lIjoiZ3JhZGVib29rIiwiY29kZSI6ImRlZiB2YWxpZGF0ZV9zY29yZXMocmVjb3Jkcyk6XG4gICAgaWYgbm90IHJlY29yZHMgb3IgYW55KG5vdCAwIDw9IHNjb3JlIDw9IDEwMCBmb3Igc2NvcmUgaW4gcmVjb3Jkcy52YWx1ZXMoKSk6XG4gICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoJ+aIkOe7qeW/hemhu+WcqCAwIOWIsCAxMDAg5LmL6Ze077yM5LiU6K6w5b2V5LiN5Li656m6JylcbiAgICByZXR1cm4gZGljdChyZWNvcmRzKVxuXG5kZWYgc3VtbWFyaXplKHJlY29yZHMpOlxuICAgIHNjb3JlcyA9IHZhbGlkYXRlX3Njb3JlcyhyZWNvcmRzKVxuICAgIHJldHVybiB7J2NvdW50JzogbGVuKHNjb3JlcyksICdhdmVyYWdlJzogcm91bmQoc3VtKHNjb3Jlcy52YWx1ZXMoKSkvbGVuKHNjb3JlcyksMiksICd0b3AnOiBtYXgoc2NvcmVzLGtleT1zY29yZXMuZ2V0KX0ifX0seyJpZCI6ImdldCIsInR5cGUiOiJHZXQiLCJ0aXRsZSI6IkdldCIsIngiOjM1MCwieSI6ODAsImNvbmZpZyI6eyJwYXRoIjoic3VtbWFyaXplIn19LHsiaWQiOiJjYWxsIiwidHlwZSI6IkNhbGwiLCJ0aXRsZSI6IkNhbGwiLCJ4Ijo2ODAsInkiOjgwLCJjb25maWciOnsiYXJncyI6W3siQWxpY2UiOjg1LCJCb2IiOjY1LCJDaGVuIjo5Mn1dfX0seyJpZCI6Im91dCIsInR5cGUiOiJPdXRwdXQiLCJ0aXRsZSI6Ik91dHB1dCIsIngiOjEwMTAsInkiOjgwLCJjb25maWciOnt9fV0sImVkZ2VzIjpbeyJzb3VyY2UiOiJtb2R1bGUiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImdldCIsImluIjoidmFsdWUifSx7InNvdXJjZSI6ImdldCIsIm91dCI6InZhbHVlIiwidGFyZ2V0IjoiY2FsbCIsImluIjoiZnVuY3Rpb24ifSx7InNvdXJjZSI6ImNhbGwiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsiY291bnQiOjMsImF2ZXJhZ2UiOjgwLjY3LCJ0b3AiOiJDaGVuIn19fSwidmVyaWZpZWQiOnRydWV9
# FlowPy source sha256: 9a78934f49ac10213f294f1c0f99a114e0a601bcd9f67193ec50b5f0ac72c291
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_module(inputs):
    # Module
    import types, sys
    module = types.ModuleType('gradebook')
    sys.modules[module.__name__] = module
    exec(compile("def validate_scores(records):\n    if not records or any(not 0 <= score <= 100 for score in records.values()):\n        raise ValueError('成绩必须在 0 到 100 之间，且记录不为空')\n    return dict(records)\n\ndef summarize(records):\n    scores = validate_scores(records)\n    return {'count': len(scores), 'average': round(sum(scores.values())/len(scores),2), 'top': max(scores,key=scores.get)}", '<module>', 'exec'), module.__dict__)
    return {'value': module}


def node_get(inputs):
    # Get
    value = inputs.get('value')
    for key in ['summarize']:
        if key:
            value = value[int(key)] if isinstance(value, (list, tuple)) else value[key] if isinstance(value, dict) else getattr(value, key)
    return {'value': value}


def node_call(inputs):
    # Call
    function = inputs.get('function')
    if not callable(function):
        raise TypeError('请连接函数定义、Lambda 或可调用对象')
    args = inputs.get('args', [{'Alice': 85, 'Bob': 65, 'Chen': 92}])
    kwargs = inputs.get('kwargs', {})
    if not isinstance(args, list) or not isinstance(kwargs, dict):
        raise TypeError('args 必须是 list，kwargs 必须是 dict')
    if 'value' in inputs:
        args = [inputs['value'], *args]
    result = function(*args, **kwargs)
    if inspect.isawaitable(result):
        result = asyncio.run(_await_result(result))
    return {'value': result}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'module'
        if True:
            results['module'] = node_module({})
        else:
            results['module'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'module', 'status': 'skipped' if results['module'] is None else 'completed'})
            else:
                trace['module'] = results['module']
        current_node = 'get'
        if results['module'] is not None:
            results['get'] = node_get({'value': results['module']['value']})
        else:
            results['get'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'get', 'status': 'skipped' if results['get'] is None else 'completed'})
            else:
                trace['get'] = results['get']
        current_node = 'call'
        if results['get'] is not None:
            results['call'] = node_call({'function': results['get']['value']})
        else:
            results['call'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'call', 'status': 'skipped' if results['call'] is None else 'completed'})
            else:
                trace['call'] = results['call']
        current_node = 'out'
        if results['call'] is not None:
            results['out'] = node_out({'value': results['call']['value']})
        else:
            results['out'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'out', 'status': 'skipped' if results['out'] is None else 'completed'})
            else:
                trace['out'] = results['out']
    except Exception as exc:
        raise RuntimeError(f'节点 {current_node}: {exc}') from exc
    return results


if __name__ == '__main__':
    from pprint import pprint
    pprint(run_graph())
