# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5a2m55Sf5oiQ57up566h55CG77ya5a2X5YW45LiO6ZuG5ZCIIiwid2VlayI6NywiZGVzY3JpcHRpb24iOiLlrZflhbjlop7liKDmlLnmn6XjgIHpm4blkIjkuqTlubblt67ku6Xlj4rph43lpI3lgLzmtojpmaTjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImlucHV0IiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiLovpPlhaXmlbDmja4iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6eyJBbGljZSI6ODUsIkJvYiI6NTksIkNoZW4iOjkyfX19LHsiaWQiOiJsb2dpYyIsInR5cGUiOiJQeXRob24iLCJ0aXRsZSI6IlB5dGhvbiDlpITnkIYiLCJ4IjozNTAsInkiOjgwLCJjb25maWciOnsiY29kZSI6InNjb3JlcyA9IGRpY3QodmFsdWUpXG5zY29yZXMudXBkYXRlKEJvYj02NSwgRG9yYT03OClcbmRlbCBzY29yZXNbJ0RvcmEnXVxucGFzc2VkID0ge25hbWUgZm9yIG5hbWUsIHNjb3JlIGluIHNjb3Jlcy5pdGVtcygpIGlmIHNjb3JlID49IDYwfVxucmVnaXN0ZXJlZCA9IHsnQWxpY2UnLCAnQm9iJywgJ0NoZW4nLCAnRG9yYSd9XG5yZXN1bHQgPSB7J3Njb3Jlcyc6IHNjb3JlcywgJ3Bhc3NlZCc6IHNvcnRlZChwYXNzZWQpLCAnbWlzc2luZyc6IHNvcnRlZChyZWdpc3RlcmVkLXNldChzY29yZXMpKSwgJ3NoYXJlZCc6IHNvcnRlZChwYXNzZWQgJiByZWdpc3RlcmVkKSwgJ3VuaXF1ZV9zY29yZXMnOiBzb3J0ZWQoc2V0KHNjb3Jlcy52YWx1ZXMoKSkpfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoi57uT5p6cIiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW5wdXQiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImxvZ2ljIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsic2NvcmVzIjp7IkFsaWNlIjo4NSwiQm9iIjo2NSwiQ2hlbiI6OTJ9LCJwYXNzZWQiOlsiQWxpY2UiLCJCb2IiLCJDaGVuIl0sIm1pc3NpbmciOlsiRG9yYSJdLCJzaGFyZWQiOlsiQWxpY2UiLCJCb2IiLCJDaGVuIl0sInVuaXF1ZV9zY29yZXMiOls2NSw4NSw5Ml19fX0sInZlcmlmaWVkIjp0cnVlfQ==
# FlowPy source sha256: b17634a012d0e2ea2fc53cddee055fc7b481ec5986eb30c19b6ee56f52b2e838
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': {'Alice': 85, 'Bob': 59, 'Chen': 92}}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    scores = dict(value)
    scores.update(Bob=65, Dora=78)
    del scores['Dora']
    passed = {name for name, score in scores.items() if score >= 60}
    registered = {'Alice', 'Bob', 'Chen', 'Dora'}
    result = {'scores': scores, 'passed': sorted(passed), 'missing': sorted(registered-set(scores)), 'shared': sorted(passed & registered), 'unique_scores': sorted(set(scores.values()))}
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
            trace['input'] = results['input']
        current_node = 'logic'
        if results['input'] is not None:
            results['logic'] = node_logic({'value': results['input']['value']})
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
