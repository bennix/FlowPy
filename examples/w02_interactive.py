# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5Lqk5LqS5byPIEJNSSAvIGlucHV0KCkiLCJ3ZWVrIjoyLCJkZXNjcmlwdGlvbiI6IuS9v+eUqOmAkOihjOagh+WHhui+k+WFpemHjeeOsOS6pOS6ku+8m+WvvOWHuuWQjuWPr+WcqOe7iOerr+WunumZhei+k+WFpeOAgiIsInN0ZGluIjoiNzBcbjEuNzVcbiIsIm5vZGVzIjpbeyJpZCI6ImludGVyYWN0aXZlIiwidHlwZSI6IlB5dGhvbiIsInRpdGxlIjoi6L6T5YWl5LiO6KGo6L6+5byPIiwieCI6MzAsInkiOjgwLCJjb25maWciOnsiY29kZSI6IndlaWdodCA9IGZsb2F0KGlucHV0KCfkvZPph40oa2cp77yaJykpXG5oZWlnaHQgPSBmbG9hdChpbnB1dCgn6Lqr6auYKG0p77yaJykpXG5pZiB3ZWlnaHQgPD0gMCBvciBoZWlnaHQgPD0gMDpcbiAgICByYWlzZSBWYWx1ZUVycm9yKCfkvZPph43lkozouqvpq5jlv4XpobvkuLrmraPmlbAnKVxucmVzdWx0ID0gcm91bmQod2VpZ2h0IC8gaGVpZ2h0ICoqIDIsIDIpXG5wcmludChmJ0JNSSA9IHtyZXN1bHR9JykifX0seyJpZCI6Im91dCIsInR5cGUiOiJPdXRwdXQiLCJ0aXRsZSI6Ik91dHB1dCIsIngiOjM4MCwieSI6ODAsImNvbmZpZyI6e319XSwiZWRnZXMiOlt7InNvdXJjZSI6ImludGVyYWN0aXZlIiwib3V0IjoidmFsdWUiLCJ0YXJnZXQiOiJvdXQiLCJpbiI6InZhbHVlIn1dLCJjaGVja3MiOnsib3V0Ijp7InZhbHVlIjoyMi44Nn19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: 3e71edeb5fd89169c77adeafe09ea26c131aade85a2a1da694b9f03e5ca62f6a
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_interactive(inputs):
    # 输入与表达式
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    weight = float(input('体重(kg)：'))
    height = float(input('身高(m)：'))
    if weight <= 0 or height <= 0:
        raise ValueError('体重和身高必须为正数')
    result = round(weight / height ** 2, 2)
    print(f'BMI = {result}')
    return {'value': result}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'interactive'
        if True:
            results['interactive'] = node_interactive({})
        else:
            results['interactive'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'interactive', 'status': 'skipped' if results['interactive'] is None else 'completed'})
            else:
                trace['interactive'] = results['interactive']
        current_node = 'out'
        if results['interactive'] is not None:
            results['out'] = node_out({'value': results['interactive']['value']})
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
