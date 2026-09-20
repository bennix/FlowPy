# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5Z+656GAIHBhbmRhc++8muihqOagvOa4hea0l+S4juetm+mAiSIsIndlZWsiOjExLCJkZXNjcmlwdGlvbiI6IkRhdGFGcmFtZeOAgWRyb3BuYeOAgWFzdHlwZeOAgeW4g+WwlOetm+mAieOAgeWIl+mAieaLqeS4jiB0b19kaWN077yb5peg6aKd5aSW5pWw5o2u5qGG5p6244CCIiwic3RkaW4iOiIiLCJub2RlcyI6W3siaWQiOiJpbnB1dCIsInR5cGUiOiJDb25zdGFudCIsInRpdGxlIjoi6L6T5YWl5pWw5o2uIiwieCI6MzAsInkiOjgwLCJjb25maWciOnsidmFsdWUiOlt7Im5hbWUiOiJBbGljZSIsInNjb3JlIjoiODUifSx7Im5hbWUiOiJCb2IiLCJzY29yZSI6bnVsbH0seyJuYW1lIjoiQ2hlbiIsInNjb3JlIjoiNTkifSx7Im5hbWUiOiJEb3JhIiwic2NvcmUiOiI5MiJ9XX19LHsiaWQiOiJsb2dpYyIsInR5cGUiOiJQeXRob24iLCJ0aXRsZSI6IlB5dGhvbiDlpITnkIYiLCJ4IjozNTAsInkiOjgwLCJjb25maWciOnsiY29kZSI6ImltcG9ydCBwYW5kYXMgYXMgcGRcbmZyYW1lID0gcGQuRGF0YUZyYW1lKHZhbHVlKVxuZnJhbWUgPSBmcmFtZS5kcm9wbmEoc3Vic2V0PVsnc2NvcmUnXSkuY29weSgpXG5mcmFtZVsnc2NvcmUnXSA9IGZyYW1lWydzY29yZSddLmFzdHlwZShpbnQpXG5wYXNzZWQgPSBmcmFtZS5sb2NbZnJhbWVbJ3Njb3JlJ10gPj0gNjAsIFsnbmFtZScsJ3Njb3JlJ11dLnNvcnRfdmFsdWVzKCdzY29yZScsYXNjZW5kaW5nPUZhbHNlKVxucmVzdWx0ID0geydyZWNvcmRzJzogcGFzc2VkLnRvX2RpY3Qob3JpZW50PSdyZWNvcmRzJyksICdjb3VudCc6IGxlbihwYXNzZWQpLCAnYXZlcmFnZSc6IGZsb2F0KHBhc3NlZFsnc2NvcmUnXS5tZWFuKCkpfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoi57uT5p6cIiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW5wdXQiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImxvZ2ljIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsicmVjb3JkcyI6W3sibmFtZSI6IkRvcmEiLCJzY29yZSI6OTJ9LHsibmFtZSI6IkFsaWNlIiwic2NvcmUiOjg1fV0sImNvdW50IjoyLCJhdmVyYWdlIjo4OC41fX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: 31f00518ef6194d63b6909a9df9a12cb7fea92a4707c6dec2c4cd35a5b69e4b9
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': [{'name': 'Alice', 'score': '85'}, {'name': 'Bob', 'score': None}, {'name': 'Chen', 'score': '59'}, {'name': 'Dora', 'score': '92'}]}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    import pandas as pd
    frame = pd.DataFrame(value)
    frame = frame.dropna(subset=['score']).copy()
    frame['score'] = frame['score'].astype(int)
    passed = frame.loc[frame['score'] >= 60, ['name','score']].sort_values('score',ascending=False)
    result = {'records': passed.to_dict(orient='records'), 'count': len(passed), 'average': float(passed['score'].mean())}
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
