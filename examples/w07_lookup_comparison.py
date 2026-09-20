# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5YiX6KGo5ZKM5a2X5YW455qE5p+l5om+5a+55q+UIiwid2VlayI6NywiZGVzY3JpcHRpb24iOiLlkIzkuIDmibnmn6Xor6Lmr5TovoPnur/mgKfmn6Xmib7kuI7lrZflhbjmn6Xmib7vvIzmlq3oqIDnu5PmnpzkuIDoh7TvvJvkuI3miorogJfml7blvZPmraPnoa7mgKfjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImlucHV0IiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiLovpPlhaXmlbDmja4iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6eyJjb3VudCI6MjAwMCwicXVlcmllcyI6WzMsMTAwLDE5OTksMjUwMF19fX0seyJpZCI6ImxvZ2ljIiwidHlwZSI6IlB5dGhvbiIsInRpdGxlIjoiUHl0aG9uIOWkhOeQhiIsIngiOjM1MCwieSI6ODAsImNvbmZpZyI6eyJjb2RlIjoicmVjb3JkcyA9IFsoaSwgaSAqIDEwKSBmb3IgaSBpbiByYW5nZSh2YWx1ZVsnY291bnQnXSldXG5pbmRleCA9IGRpY3QocmVjb3Jkcylcbmxpc3RfcmVzdWx0ID0gW25leHQoKHNjb3JlIGZvciBrZXksIHNjb3JlIGluIHJlY29yZHMgaWYga2V5ID09IHEpLCBOb25lKSBmb3IgcSBpbiB2YWx1ZVsncXVlcmllcyddXVxuZGljdF9yZXN1bHQgPSBbaW5kZXguZ2V0KHEpIGZvciBxIGluIHZhbHVlWydxdWVyaWVzJ11dXG5hc3NlcnQgbGlzdF9yZXN1bHQgPT0gZGljdF9yZXN1bHRcbnJlc3VsdCA9IHsnc2FtZSc6IFRydWUsICdyZXN1bHRzJzogZGljdF9yZXN1bHQsICdyb3dzJzogbGVuKHJlY29yZHMpfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoi57uT5p6cIiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW5wdXQiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImxvZ2ljIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsic2FtZSI6dHJ1ZSwicmVzdWx0cyI6WzMwLDEwMDAsMTk5OTAsbnVsbF0sInJvd3MiOjIwMDB9fX0sInZlcmlmaWVkIjp0cnVlfQ==
# FlowPy source sha256: 5aad5315c50d408d3b4549e343184a37f6375ae956502b68ca7ede0d3fb4d41a
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': {'count': 2000, 'queries': [3, 100, 1999, 2500]}}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    records = [(i, i * 10) for i in range(value['count'])]
    index = dict(records)
    list_result = [next((score for key, score in records if key == q), None) for q in value['queries']]
    dict_result = [index.get(q) for q in value['queries']]
    assert list_result == dict_result
    result = {'same': True, 'results': dict_result, 'rows': len(records)}
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
