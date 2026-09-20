# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5qCH5YeG5bqT77ya5o+Q5Y+W6YKu566x5LiO5omL5py65Y+3Iiwid2VlayI6OCwiZGVzY3JpcHRpb24iOiLku4XlgZrmlofmnKzmir3lj5bvvJrkuKTkuKrmraPliJnovpPlh7rliJfooajvvIzlho3nlLEgUHl0aG9uIOWQiOW5tue7k+aehOWMlue7k+aenOOAgiIsInN0ZGluIjoiIiwibm9kZXMiOlt7ImlkIjoidGV4dCIsInR5cGUiOiJMb2FkVGV4dCIsInRpdGxlIjoiTG9hZFRleHQiLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ0ZXh0Ijoi6IGU57O7IGFsaWNlQGV4YW1wbGUuY29tIC8gYm9iQHRlc3Qub3Jn77yb5omL5py6IDEzODAwMTM4MDAw44CBMTM5MTIzNDU2NzjjgIIifX0seyJpZCI6ImVtYWlscyIsInR5cGUiOiJSZWdleEZpbmRhbGwiLCJ0aXRsZSI6IlJlZ2V4RmluZGFsbCIsIngiOjM0MCwieSI6ODAsImNvbmZpZyI6eyJwYXR0ZXJuIjoiW0EtWmEtejAtOS5fJSstXStAW0EtWmEtejAtOS4tXStcXC5bQS1aYS16XXsyLH0ifX0seyJpZCI6InBob25lcyIsInR5cGUiOiJSZWdleEZpbmRhbGwiLCJ0aXRsZSI6IlJlZ2V4RmluZGFsbCIsIngiOjM0MCwieSI6MzcwLCJjb25maWciOnsicGF0dGVybiI6Iig/PCFcXGQpMVszLTldXFxkezl9KD8hXFxkKSJ9fSx7ImlkIjoiY29tYmluZSIsInR5cGUiOiJQeXRob24iLCJ0aXRsZSI6IlB5dGhvbiIsIngiOjY4MCwieSI6ODAsImNvbmZpZyI6eyJjb2RlIjoicmVzdWx0ID0ge1wiZW1haWxzXCI6IHZhbHVlLCBcInBob25lc1wiOiBpdGVtc30ifX0seyJpZCI6Im91dCIsInR5cGUiOiJPdXRwdXQiLCJ0aXRsZSI6Ik91dHB1dCIsIngiOjEwMjAsInkiOjgwLCJjb25maWciOnt9fV0sImVkZ2VzIjpbeyJzb3VyY2UiOiJ0ZXh0Iiwib3V0IjoidGV4dCIsInRhcmdldCI6ImVtYWlscyIsImluIjoidGV4dCJ9LHsic291cmNlIjoidGV4dCIsIm91dCI6InRleHQiLCJ0YXJnZXQiOiJwaG9uZXMiLCJpbiI6InRleHQifSx7InNvdXJjZSI6ImVtYWlscyIsIm91dCI6Im1hdGNoZXMiLCJ0YXJnZXQiOiJjb21iaW5lIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoicGhvbmVzIiwib3V0IjoibWF0Y2hlcyIsInRhcmdldCI6ImNvbWJpbmUiLCJpbiI6Iml0ZW1zIn0seyJzb3VyY2UiOiJjb21iaW5lIiwib3V0IjoidmFsdWUiLCJ0YXJnZXQiOiJvdXQiLCJpbiI6InZhbHVlIn1dLCJjaGVja3MiOnsib3V0Ijp7InZhbHVlIjp7ImVtYWlscyI6WyJhbGljZUBleGFtcGxlLmNvbSIsImJvYkB0ZXN0Lm9yZyJdLCJwaG9uZXMiOlsiMTM4MDAxMzgwMDAiLCIxMzkxMjM0NTY3OCJdfX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: afe421722fe1a510b22e0d2557bbcc17f88ab9be181a6a003cceefcdfa3da941
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_text(inputs):
    # LoadText
    return {'text': '联系 alice@example.com / bob@test.org；手机 13800138000、13912345678。'}


def node_emails(inputs):
    # RegexFindall
    text = inputs.get('text', '')
    flags = 0
    pattern = inputs.get('pattern', '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}')
    matches = re.findall(pattern, text, flags)
    return {'matches': matches, 'ok': bool(matches)}


def node_phones(inputs):
    # RegexFindall
    text = inputs.get('text', '')
    flags = 0
    pattern = inputs.get('pattern', '(?<!\\d)1[3-9]\\d{9}(?!\\d)')
    matches = re.findall(pattern, text, flags)
    return {'matches': matches, 'ok': bool(matches)}


def node_combine(inputs):
    # Python
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    result = {"emails": value, "phones": items}
    return {'value': result}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'text'
        if True:
            results['text'] = node_text({})
        else:
            results['text'] = None
        if trace is not None:
            trace['text'] = results['text']
        current_node = 'emails'
        if results['text'] is not None:
            results['emails'] = node_emails({'text': results['text']['text']})
        else:
            results['emails'] = None
        if trace is not None:
            trace['emails'] = results['emails']
        current_node = 'phones'
        if results['text'] is not None:
            results['phones'] = node_phones({'text': results['text']['text']})
        else:
            results['phones'] = None
        if trace is not None:
            trace['phones'] = results['phones']
        current_node = 'combine'
        if results['emails'] is not None and results['phones'] is not None:
            results['combine'] = node_combine({'value': results['emails']['matches'], 'items': results['phones']['matches']})
        else:
            results['combine'] = None
        if trace is not None:
            trace['combine'] = results['combine']
        current_node = 'out'
        if results['combine'] is not None:
            results['out'] = node_out({'value': results['combine']['value']})
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
