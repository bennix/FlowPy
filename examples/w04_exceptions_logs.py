# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5byC5bi45o2V6I635LiO5omT5Y2w6LCD6K+VIiwid2VlayI6NCwiZGVzY3JpcHRpb24iOiLlr7nmraPluLjovpPlhaXjgIHpmaTpm7blkozml6DmlYjmlbDlrZfpgJDpobnmtYvor5XvvIzlvILluLjkuI3kvJrkuK3mlq3mlbTkuKrmibnmrKHjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6InBhaXJzIiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiJDb25zdGFudCIsIngiOjMwLCJ5Ijo4MCwiY29uZmlnIjp7InZhbHVlIjpbWzEyLDNdLFsxLDBdLFsiYmFkIiwyXV19fSx7ImlkIjoiZnVuY3Rpb24iLCJ0eXBlIjoiRnVuY3Rpb24iLCJ0aXRsZSI6IkZ1bmN0aW9uIiwieCI6MzQwLCJ5IjozMzAsImNvbmZpZyI6eyJuYW1lIjoic2FmZV9kaXZpZGUiLCJjb2RlIjoiZGVmIHNhZmVfZGl2aWRlKHBhaXIpOlxuICAgIHRyeTpcbiAgICAgICAgYSwgYiA9IG1hcChmbG9hdCwgcGFpcilcbiAgICAgICAgcmV0dXJuIHsnb2snOiBUcnVlLCAndmFsdWUnOiBhIC8gYn1cbiAgICBleGNlcHQgKFZhbHVlRXJyb3IsIFR5cGVFcnJvciwgWmVyb0RpdmlzaW9uRXJyb3IpIGFzIGV4YzpcbiAgICAgICAgcHJpbnQodHlwZShleGMpLl9fbmFtZV9fLCBwYWlyKVxuICAgICAgICByZXR1cm4geydvayc6IEZhbHNlLCAnZXJyb3InOiB0eXBlKGV4YykuX19uYW1lX199In19LHsiaWQiOiJtYXAiLCJ0eXBlIjoiTWFwIiwidGl0bGUiOiJNYXAiLCJ4IjozNDAsInkiOjgwLCJjb25maWciOnt9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoiT3V0cHV0IiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoicGFpcnMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im1hcCIsImluIjoiaXRlbXMifSx7InNvdXJjZSI6ImZ1bmN0aW9uIiwib3V0IjoiZnVuY3Rpb24iLCJ0YXJnZXQiOiJtYXAiLCJpbiI6ImZ1bmN0aW9uIn0seyJzb3VyY2UiOiJtYXAiLCJvdXQiOiJpdGVtcyIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOlt7Im9rIjp0cnVlLCJ2YWx1ZSI6NC4wfSx7Im9rIjpmYWxzZSwiZXJyb3IiOiJaZXJvRGl2aXNpb25FcnJvciJ9LHsib2siOmZhbHNlLCJlcnJvciI6IlZhbHVlRXJyb3IifV19fSwidmVyaWZpZWQiOnRydWV9
# FlowPy source sha256: e555c6e56c3b831db22c3c15cd2bf77b2bc5b23ed824db84b738d95c6ad141e4
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_pairs(inputs):
    # Constant
    return {'value': [[12, 3], [1, 0], ['bad', 2]]}


def node_function(inputs):
    # Function
    value = inputs.get('value')
    def safe_divide(pair):
        try:
            a, b = map(float, pair)
            return {'ok': True, 'value': a / b}
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            print(type(exc).__name__, pair)
            return {'ok': False, 'error': type(exc).__name__}
    if not callable(safe_divide):
        raise TypeError('定义必须输出可调用对象')
    return {'function': safe_divide}


def node_map(inputs):
    # Map
    items = inputs.get('items', [])
    if not isinstance(items, list):
        raise TypeError('列表输入必须是 list')
    if len(items) > 1000:
        raise ValueError('输入列表超过循环上限')
    acc = []
    for index, item in enumerate(items):
        result = None
        if 'function' in inputs:
            result = inputs['function'](item)
            if inspect.isawaitable(result):
                result = asyncio.run(_await_result(result))
        else:
            result = item
        acc.append(result)
    return {'items': acc, 'count': len(acc)}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'pairs'
        if True:
            results['pairs'] = node_pairs({})
        else:
            results['pairs'] = None
        if trace is not None:
            trace['pairs'] = results['pairs']
        current_node = 'function'
        if True:
            results['function'] = node_function({})
        else:
            results['function'] = None
        if trace is not None:
            trace['function'] = results['function']
        current_node = 'map'
        if results['pairs'] is not None and results['function'] is not None:
            results['map'] = node_map({'items': results['pairs']['value'], 'function': results['function']['function']})
        else:
            results['map'] = None
        if trace is not None:
            trace['map'] = results['map']
        current_node = 'out'
        if results['map'] is not None:
            results['out'] = node_out({'value': results['map']['items']})
        else:
            results['out'] = None
        if trace is not None:
            trace['out'] = results['out']
    except Exception as exc:
        raise RuntimeError(f'节点 {current_node}: {exc}') from exc
    return results


if __name__ == '__main__':
    from pprint import pprint
    pprint(run_graph())
