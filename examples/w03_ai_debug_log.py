# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoiQUkg6LCD6K+V5pel5b+X77ya5LiJ5qyh5aSx6LSl5LiO5L+u5q2jIiwid2VlayI6MywiZGVzY3JpcHRpb24iOiLph43njrDor63ms5XplJnor6/jgIHlubvop4nlh73mlbDkuI7pgLvovpHplJnor6/vvIzpqozor4Hkv67mraPlkI7nmoTnu5PmnpzjgIIiLCJzdGRpbiI6IiIsIm5vZGVzIjpbeyJpZCI6ImlucHV0IiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiLovpPlhaXmlbDmja4iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6bnVsbH19LHsiaWQiOiJsb2dpYyIsInR5cGUiOiJQeXRob24iLCJ0aXRsZSI6IlB5dGhvbiDlpITnkIYiLCJ4IjozNTAsInkiOjgwLCJjb25maWciOnsiY29kZSI6ImNhc2VzID0gW1xuICAgIHsna2luZCc6J1N5bnRheEVycm9yJywgJ2JhZCc6J3Jlc3VsdCA9ICgxICsnLCAnZml4ZWQnOidyZXN1bHQgPSAxICsgMicsICdleHBlY3RlZCc6M30sXG4gICAgeydraW5kJzonQXR0cmlidXRlRXJyb3InLCAnYmFkJzonaW1wb3J0IG1hdGhcXG5yZXN1bHQgPSBtYXRoLnNxdWFyZSg0KScsICdmaXhlZCc6J3Jlc3VsdCA9IDQgKiogMicsICdleHBlY3RlZCc6MTZ9LFxuICAgIHsna2luZCc6J0Fzc2VydGlvbkVycm9yJywgJ2JhZCc6J3Jlc3VsdCA9IDcwIC8gMS43NScsICdmaXhlZCc6J3Jlc3VsdCA9IHJvdW5kKDcwIC8gMS43NSAqKiAyLCAyKScsICdleHBlY3RlZCc6MjIuODZ9LFxuXVxubG9ncyA9IFtdXG5mb3IgY2FzZSBpbiBjYXNlczpcbiAgICB0cnk6XG4gICAgICAgIG5hbWVzcGFjZSA9IHt9XG4gICAgICAgIGV4ZWMoY29tcGlsZShjYXNlWydiYWQnXSwgJzxBSSBwcm9wb3NhbD4nLCAnZXhlYycpLCBuYW1lc3BhY2UpXG4gICAgICAgIGFzc2VydCBuYW1lc3BhY2VbJ3Jlc3VsdCddID09IGNhc2VbJ2V4cGVjdGVkJ10sICflhazlvI/plJnor68nXG4gICAgZXhjZXB0IChTeW50YXhFcnJvciwgQXR0cmlidXRlRXJyb3IsIEFzc2VydGlvbkVycm9yKSBhcyBleGM6XG4gICAgICAgIGRldGVjdGVkID0gdHlwZShleGMpLl9fbmFtZV9fXG4gICAgICAgIHByaW50KGYn5Y+R546wIHtkZXRlY3RlZH3vvIzlvIDlp4vpqozor4Hkv67mraMnKVxuICAgIGVsc2U6XG4gICAgICAgIHJhaXNlIEFzc2VydGlvbkVycm9yKCfpooTorr7plJnor6/mnKrooqvlj5HnjrAnKVxuICAgIG5hbWVzcGFjZSA9IHt9XG4gICAgZXhlYyhjb21waWxlKGNhc2VbJ2ZpeGVkJ10sICc8Y29ycmVjdGVkPicsICdleGVjJyksIG5hbWVzcGFjZSlcbiAgICBhc3NlcnQgbmFtZXNwYWNlWydyZXN1bHQnXSA9PSBjYXNlWydleHBlY3RlZCddXG4gICAgbG9ncy5hcHBlbmQoeydmYWlsdXJlJzogZGV0ZWN0ZWQsICdmaXhlZF9yZXN1bHQnOiBuYW1lc3BhY2VbJ3Jlc3VsdCddLCAndmVyaWZpZWQnOiBUcnVlfSlcbnJlc3VsdCA9IGxvZ3MifX0seyJpZCI6Im91dCIsInR5cGUiOiJPdXRwdXQiLCJ0aXRsZSI6Iue7k+aenCIsIngiOjcwMCwieSI6ODAsImNvbmZpZyI6e319XSwiZWRnZXMiOlt7InNvdXJjZSI6ImlucHV0Iiwib3V0IjoidmFsdWUiLCJ0YXJnZXQiOiJsb2dpYyIsImluIjoidmFsdWUifSx7InNvdXJjZSI6ImxvZ2ljIiwib3V0IjoidmFsdWUiLCJ0YXJnZXQiOiJvdXQiLCJpbiI6InZhbHVlIn1dLCJjaGVja3MiOnsib3V0Ijp7InZhbHVlIjpbeyJmYWlsdXJlIjoiU3ludGF4RXJyb3IiLCJmaXhlZF9yZXN1bHQiOjMsInZlcmlmaWVkIjp0cnVlfSx7ImZhaWx1cmUiOiJBdHRyaWJ1dGVFcnJvciIsImZpeGVkX3Jlc3VsdCI6MTYsInZlcmlmaWVkIjp0cnVlfSx7ImZhaWx1cmUiOiJBc3NlcnRpb25FcnJvciIsImZpeGVkX3Jlc3VsdCI6MjIuODYsInZlcmlmaWVkIjp0cnVlfV19fSwidmVyaWZpZWQiOnRydWV9
# FlowPy source sha256: 92540d312bd903c9c685662cad3bd3ad7c0805e73fc1e96e845fa96ee495e331
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': None}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    cases = [
        {'kind':'SyntaxError', 'bad':'result = (1 +', 'fixed':'result = 1 + 2', 'expected':3},
        {'kind':'AttributeError', 'bad':'import math\nresult = math.square(4)', 'fixed':'result = 4 ** 2', 'expected':16},
        {'kind':'AssertionError', 'bad':'result = 70 / 1.75', 'fixed':'result = round(70 / 1.75 ** 2, 2)', 'expected':22.86},
    ]
    logs = []
    for case in cases:
        try:
            namespace = {}
            exec(compile(case['bad'], '<AI proposal>', 'exec'), namespace)
            assert namespace['result'] == case['expected'], '公式错误'
        except (SyntaxError, AttributeError, AssertionError) as exc:
            detected = type(exc).__name__
            print(f'发现 {detected}，开始验证修正')
        else:
            raise AssertionError('预设错误未被发现')
        namespace = {}
        exec(compile(case['fixed'], '<corrected>', 'exec'), namespace)
        assert namespace['result'] == case['expected']
        logs.append({'failure': detected, 'fixed_result': namespace['result'], 'verified': True})
    result = logs
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
