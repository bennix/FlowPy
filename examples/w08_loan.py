# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5qCH5YeG5bqT77ya562J6aKd5pys5oGv5pyI5L6bIiwid2VlayI6OCwiZGVzY3JpcHRpb24iOiLlh73mlbDjgIFtYXRoLnBvdyDkuI7pm7bliKnnjofliIbmlK/vvJvlubTliKnnjofkvb/nlKjlsI/mlbDvvIzkvovlpoIgMC4wNDXjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImlucHV0IiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiLovpPlhaXmlbDmja4iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6eyJwcmluY2lwYWwiOjEwMDAwMCwiYW5udWFsX3JhdGUiOjAuMDQ1LCJtb250aHMiOjM2MH19fSx7ImlkIjoibG9naWMiLCJ0eXBlIjoiUHl0aG9uIiwidGl0bGUiOiJQeXRob24g5aSE55CGIiwieCI6MzUwLCJ5Ijo4MCwiY29uZmlnIjp7ImNvZGUiOiJpbXBvcnQgbWF0aFxucHJpbmNpcGFsLCBhbm51YWxfcmF0ZSwgbW9udGhzID0gdmFsdWVbJ3ByaW5jaXBhbCddLCB2YWx1ZVsnYW5udWFsX3JhdGUnXSwgdmFsdWVbJ21vbnRocyddXG5pZiBwcmluY2lwYWwgPD0gMCBvciBhbm51YWxfcmF0ZSA8IDAgb3IgbW9udGhzIDw9IDAgb3IgaW50KG1vbnRocykgIT0gbW9udGhzOlxuICAgIHJhaXNlIFZhbHVlRXJyb3IoJ+i0t+asvuacrOmHkeOAgeWIqeeOh+aIluacn+aVsOaXoOaViCcpXG5yYXRlID0gYW5udWFsX3JhdGUgLyAxMlxucGF5bWVudCA9IHByaW5jaXBhbCAvIG1vbnRocyBpZiByYXRlID09IDAgZWxzZSBwcmluY2lwYWwgKiByYXRlICogbWF0aC5wb3coMSArIHJhdGUsIG1vbnRocykgLyAobWF0aC5wb3coMSArIHJhdGUsIG1vbnRocykgLSAxKVxucmVzdWx0ID0geydtb250aGx5X3BheW1lbnQnOiByb3VuZChwYXltZW50LCAyKSwgJ21vbnRocyc6IG1vbnRoc30ifX0seyJpZCI6Im91dCIsInR5cGUiOiJPdXRwdXQiLCJ0aXRsZSI6Iue7k+aenCIsIngiOjcwMCwieSI6ODAsImNvbmZpZyI6e319XSwiZWRnZXMiOlt7InNvdXJjZSI6ImlucHV0Iiwib3V0IjoidmFsdWUiLCJ0YXJnZXQiOiJsb2dpYyIsImluIjoidmFsdWUifSx7InNvdXJjZSI6ImxvZ2ljIiwib3V0IjoidmFsdWUiLCJ0YXJnZXQiOiJvdXQiLCJpbiI6InZhbHVlIn1dLCJjaGVja3MiOnsib3V0Ijp7InZhbHVlIjp7Im1vbnRobHlfcGF5bWVudCI6NTA2LjY5LCJtb250aHMiOjM2MH19fSwidmVyaWZpZWQiOnRydWV9
# FlowPy source sha256: 5aa850bdf1fb6e3ae3a3826c8276e8c64184384b19e8ab13add37c45c0431fed
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': {'principal': 100000, 'annual_rate': 0.045, 'months': 360}}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    import math
    principal, annual_rate, months = value['principal'], value['annual_rate'], value['months']
    if principal <= 0 or annual_rate < 0 or months <= 0 or int(months) != months:
        raise ValueError('贷款本金、利率或期数无效')
    rate = annual_rate / 12
    payment = principal / months if rate == 0 else principal * rate * math.pow(1 + rate, months) / (math.pow(1 + rate, months) - 1)
    result = {'monthly_payment': round(payment, 2), 'months': months}
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
