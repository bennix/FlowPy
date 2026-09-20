# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5qCH5YeG5bqT77ya5Y+M6Imy55CD5Y+356CBIiwid2VlayI6OCwiZGVzY3JpcHRpb24iOiJyYW5kb20uUmFuZG9tIOWbuuWumuenjeWtkOOAgXNhbXBsZSDml6Dph43lpI3mir3moLfjgIHmjpLluo/kuI7ljLrpl7Tmlq3oqIDjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImlucHV0IiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiLovpPlhaXmlbDmja4iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6eyJzZWVkIjo0Mn19fSx7ImlkIjoibG9naWMiLCJ0eXBlIjoiUHl0aG9uIiwidGl0bGUiOiJQeXRob24g5aSE55CGIiwieCI6MzUwLCJ5Ijo4MCwiY29uZmlnIjp7ImNvZGUiOiJpbXBvcnQgcmFuZG9tXG5ybmcgPSByYW5kb20uUmFuZG9tKHZhbHVlWydzZWVkJ10pXG5yZWQgPSBzb3J0ZWQocm5nLnNhbXBsZShyYW5nZSgxLCAzNCksIDYpKVxuYmx1ZSA9IHJuZy5yYW5kaW50KDEsIDE2KVxuYXNzZXJ0IGxlbihzZXQocmVkKSkgPT0gNiBhbmQgYWxsKDEgPD0gbiA8PSAzMyBmb3IgbiBpbiByZWQpXG5hc3NlcnQgMSA8PSBibHVlIDw9IDE2XG5yZXN1bHQgPSB7J3JlZCc6IHJlZCwgJ2JsdWUnOiBibHVlfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoi57uT5p6cIiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW5wdXQiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImxvZ2ljIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsicmVkIjpbMiw4LDksMjQsMjksMzNdLCJibHVlIjo1fX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: ce4fdd94105c692ef903a9c64f7eb6812f032fcd23a7a41d21311e302fbf319e
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': {'seed': 42}}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    import random
    rng = random.Random(value['seed'])
    red = sorted(rng.sample(range(1, 34), 6))
    blue = rng.randint(1, 16)
    assert len(set(red)) == 6 and all(1 <= n <= 33 for n in red)
    assert 1 <= blue <= 16
    result = {'red': red, 'blue': blue}
    return {'value': result}


def node_out(inputs):
    # 结果
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'input'
        if True:
            results['input'] = node_input({})
        else:
            results['input'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'input', 'status': 'skipped' if results['input'] is None else 'completed'})
            else:
                trace['input'] = results['input']
        current_node = 'logic'
        if results['input'] is not None:
            results['logic'] = node_logic({'value': results['input']['value']})
        else:
            results['logic'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'logic', 'status': 'skipped' if results['logic'] is None else 'completed'})
            else:
                trace['logic'] = results['logic']
        current_node = 'out'
        if results['logic'] is not None:
            results['out'] = node_out({'value': results['logic']['value']})
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
