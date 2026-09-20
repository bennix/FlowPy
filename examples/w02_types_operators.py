# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5Z+656GA57G75Z6L5LiO6L+Q566X56ymIiwid2VlayI6MiwiZGVzY3JpcHRpb24iOiJpbnQgLyBmbG9hdCAvIHN0ciAvIGJvb2zjgIHnrpfmnK/jgIHmr5TovoPkuI7pgLvovpHov5DnrpfjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImlucHV0IiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiLovpPlhaXmlbDmja4iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6eyJhIjoxNywiYiI6NX19fSx7ImlkIjoibG9naWMiLCJ0eXBlIjoiUHl0aG9uIiwidGl0bGUiOiJQeXRob24g5aSE55CGIiwieCI6MzUwLCJ5Ijo4MCwiY29uZmlnIjp7ImNvZGUiOiJhLCBiID0gdmFsdWVbJ2EnXSwgdmFsdWVbJ2InXVxucmVzdWx0ID0geydzdW0nOiBhK2IsICdxdW90aWVudCc6IGEvL2IsICdyZW1haW5kZXInOiBhJWIsXG4gICAgICAgICAgJ3Bvd2VyJzogYioqMiwgJ2NvbXBhcmlzb24nOiBhPmIgYW5kIGI+MCxcbiAgICAgICAgICAndGV4dCc6IGYne2F9L3tifScsICdjb252ZXJzaW9uJzogaW50KCc0MicpfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoi57uT5p6cIiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW5wdXQiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImxvZ2ljIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsic3VtIjoyMiwicXVvdGllbnQiOjMsInJlbWFpbmRlciI6MiwicG93ZXIiOjI1LCJjb21wYXJpc29uIjp0cnVlLCJ0ZXh0IjoiMTcvNSIsImNvbnZlcnNpb24iOjQyfX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: a7290b431f37e5e6316a9d8837120fcd7fd843165b9988f5a5701050ac0c1660
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': {'a': 17, 'b': 5}}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    a, b = value['a'], value['b']
    result = {'sum': a+b, 'quotient': a//b, 'remainder': a%b,
              'power': b**2, 'comparison': a>b and b>0,
              'text': f'{a}/{b}', 'conversion': int('42')}
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
