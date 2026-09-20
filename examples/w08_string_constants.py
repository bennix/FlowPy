# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5qCH5YeG5bqT77yac3RyaW5nIOS4juWPr+mHjeWkjemaj+acuuWtl+espuS4siIsIndlZWsiOjgsImRlc2NyaXB0aW9uIjoic3RyaW5nLmFzY2lpX2xldHRlcnMgLyBkaWdpdHPvvJvmlZnlrabnlKjpmo/mnLrmoIfor4bnrKbvvIzkuI3kvZzkuLrlr4bnoIHjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImxvZ2ljIiwidHlwZSI6IlB5dGhvbiIsInRpdGxlIjoiUHl0aG9uIiwieCI6MzAsInkiOjgwLCJjb25maWciOnsiY29kZSI6ImltcG9ydCBzdHJpbmdcbmltcG9ydCByYW5kb21cbnJuZyA9IHJhbmRvbS5SYW5kb20oMTIpXG5hbHBoYWJldCA9IHN0cmluZy5hc2NpaV9sZXR0ZXJzICsgc3RyaW5nLmRpZ2l0c1xudG9rZW4gPSAnJy5qb2luKHJuZy5jaG9pY2UoYWxwaGFiZXQpIGZvciBfIGluIHJhbmdlKDEyKSlcbnJlc3VsdCA9IHsnbGVuZ3RoJzogbGVuKHRva2VuKSwgJ3ZhbGlkJzogYWxsKGMgaW4gYWxwaGFiZXQgZm9yIGMgaW4gdG9rZW4pfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoiT3V0cHV0IiwieCI6MzgwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsibGVuZ3RoIjoxMiwidmFsaWQiOnRydWV9fX0sInZlcmlmaWVkIjp0cnVlfQ==
# FlowPy source sha256: c0f93945956fbad4fa1db5a8f7f923998735a518f86c0121d0486b2160d2767f
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_logic(inputs):
    # Python
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    import string
    import random
    rng = random.Random(12)
    alphabet = string.ascii_letters + string.digits
    token = ''.join(rng.choice(alphabet) for _ in range(12))
    result = {'length': len(token), 'valid': all(c in alphabet for c in token)}
    return {'value': result}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'logic'
        if True:
            results['logic'] = node_logic({})
        else:
            results['logic'] = None
        if trace is not None:
            trace['logic'] = results['logic']
        current_node = 'out'
        if results['logic'] is not None:
            results['out'] = node_out({'value': results['logic']['value']})
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
