# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5a2m55Sf5oiQ57up566h55CG77ya5YiX6KGo5LiO5YWD57uEIiwid2VlayI6NiwiZGVzY3JpcHRpb24iOiLmlrDlop7jgIHkv67mlLnjgIHliKDpmaTjgIHmjpLluo/kuI7ogZrlkIjvvJvlhYPnu4Tkv53nlZnkuI3lj6/lj5jorrDlvZXjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImlucHV0IiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiLovpPlhaXmlbDmja4iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6W1siQWxpY2UiLDg1XSxbIkJvYiIsNTldLFsiQ2hlbiIsOTJdXX19LHsiaWQiOiJsb2dpYyIsInR5cGUiOiJQeXRob24iLCJ0aXRsZSI6IlB5dGhvbiDlpITnkIYiLCJ4IjozNTAsInkiOjgwLCJjb25maWciOnsiY29kZSI6InN0dWRlbnRzID0gW2xpc3Qocm93KSBmb3Igcm93IGluIHZhbHVlXVxuc3R1ZGVudHMuYXBwZW5kKFsnRG9yYScsIDc4XSlcbmZvciByb3cgaW4gc3R1ZGVudHM6XG4gICAgaWYgcm93WzBdID09ICdCb2InOiByb3dbMV0gPSA2NVxuc3R1ZGVudHMgPSBbcm93IGZvciByb3cgaW4gc3R1ZGVudHMgaWYgcm93WzBdICE9ICdEb3JhJ11cbnJhbmtlZCA9IHNvcnRlZCgodHVwbGUocm93KSBmb3Igcm93IGluIHN0dWRlbnRzKSwga2V5PWxhbWJkYSByb3c6IHJvd1sxXSwgcmV2ZXJzZT1UcnVlKVxucmVzdWx0ID0geydyYW5rZWQnOiByYW5rZWQsICdhdmVyYWdlJzogcm91bmQoc3VtKHJvd1sxXSBmb3Igcm93IGluIHJhbmtlZCkvbGVuKHJhbmtlZCksIDIpLCAncGFzc2VkJzogc3VtKHNjb3JlID49IDYwIGZvciBfLCBzY29yZSBpbiByYW5rZWQpfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoi57uT5p6cIiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW5wdXQiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImxvZ2ljIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsicmFua2VkIjpbWyJDaGVuIiw5Ml0sWyJBbGljZSIsODVdLFsiQm9iIiw2NV1dLCJhdmVyYWdlIjo4MC42NywicGFzc2VkIjozfX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: 1d4f83e3a011054a6f4715b48b004b2832e2f98b34cf2a2f86a1c0008be0457a
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': [['Alice', 85], ['Bob', 59], ['Chen', 92]]}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    students = [list(row) for row in value]
    students.append(['Dora', 78])
    for row in students:
        if row[0] == 'Bob': row[1] = 65
    students = [row for row in students if row[0] != 'Dora']
    ranked = sorted((tuple(row) for row in students), key=lambda row: row[1], reverse=True)
    result = {'ranked': ranked, 'average': round(sum(row[1] for row in ranked)/len(ranked), 2), 'passed': sum(score >= 60 for _, score in ranked)}
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
