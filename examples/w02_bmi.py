# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoiQk1JIOiuoeeul+WZqCIsIndlZWsiOjIsImRlc2NyaXB0aW9uIjoi5Y+Y6YeP44CB5pWw5YC86L+Q566X44CB5a2X5YW46L6T5YWl5LiO6L6555WM5qCh6aqM77yb5L2T6YeNIGtnIC8g6Lqr6auYIG3jgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImlucHV0IiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiLovpPlhaXmlbDmja4iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6eyJ3ZWlnaHQiOjcwLCJoZWlnaHQiOjEuNzV9fX0seyJpZCI6ImxvZ2ljIiwidHlwZSI6IlB5dGhvbiIsInRpdGxlIjoiUHl0aG9uIOWkhOeQhiIsIngiOjM1MCwieSI6ODAsImNvbmZpZyI6eyJjb2RlIjoid2VpZ2h0LCBoZWlnaHQgPSBmbG9hdCh2YWx1ZVsnd2VpZ2h0J10pLCBmbG9hdCh2YWx1ZVsnaGVpZ2h0J10pXG5pZiB3ZWlnaHQgPD0gMCBvciBoZWlnaHQgPD0gMDpcbiAgICByYWlzZSBWYWx1ZUVycm9yKCfkvZPph43lkozouqvpq5jlv4XpobvlpKfkuo4gMCcpXG5ibWkgPSB3ZWlnaHQgLyBoZWlnaHQgKiogMlxuY2F0ZWdvcnkgPSAn5YGP55imJyBpZiBibWkgPCAxOC41IGVsc2UgJ+ato+W4uCcgaWYgYm1pIDwgMjQgZWxzZSAn6LaF6YeNJyBpZiBibWkgPCAyOCBlbHNlICfogqXog5YnXG5yZXN1bHQgPSB7J2JtaSc6IHJvdW5kKGJtaSwgMiksICdjYXRlZ29yeSc6IGNhdGVnb3J5fSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoi57uT5p6cIiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW5wdXQiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImxvZ2ljIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsiYm1pIjoyMi44NiwiY2F0ZWdvcnkiOiLmraPluLgifX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: 54a791fe85bdb4ffb5056f3ec1a0ba964d5e64ceffad78f8a6737260d885c697
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': {'weight': 70, 'height': 1.75}}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    weight, height = float(value['weight']), float(value['height'])
    if weight <= 0 or height <= 0:
        raise ValueError('体重和身高必须大于 0')
    bmi = weight / height ** 2
    category = '偏瘦' if bmi < 18.5 else '正常' if bmi < 24 else '超重' if bmi < 28 else '肥胖'
    result = {'bmi': round(bmi, 2), 'category': category}
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
