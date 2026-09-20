# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5b6q546v5Lit55qEIGNvbnRpbnVlIC8gYnJlYWsiLCJ3ZWVrIjo1LCJkZXNjcmlwdGlvbiI6Ikxvb3Ag5pi+5byP5oyB5pyJIGl0ZW3jgIFpbmRleOOAgWFjY++8m+W/veeVpeepuuihjOW5tumBhyBFTkQg5YGc5q2i44CCIiwic3RkaW4iOiIiLCJub2RlcyI6W3siaWQiOiJyb3dzIiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiJDb25zdGFudCIsIngiOjMwLCJ5Ijo4MCwiY29uZmlnIjp7InZhbHVlIjpbIjEwIiwiIiwiMjAiLCJFTkQiLCI5OTkiXX19LHsiaWQiOiJsb29wIiwidHlwZSI6Ikxvb3AiLCJ0aXRsZSI6Ikxvb3AiLCJ4IjozNTAsInkiOjgwLCJjb25maWciOnsiY29kZSI6ImlmIGl0ZW0gPT0gXCJFTkRcIjpcbiAgICBicmVha1xuaWYgbm90IGl0ZW06XG4gICAgY29udGludWVcbnJlc3VsdCA9IGludChpdGVtKSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoiT3V0cHV0IiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoicm93cyIsIm91dCI6InZhbHVlIiwidGFyZ2V0IjoibG9vcCIsImluIjoiaXRlbXMifSx7InNvdXJjZSI6Imxvb3AiLCJvdXQiOiJpdGVtcyIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOlsxMCwyMF19fSwidmVyaWZpZWQiOnRydWV9
# FlowPy source sha256: 855b52d858dccf83a55b62ecfdf616d0987474db55f4341cf5f448d7d781ed1f
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_rows(inputs):
    # Constant
    return {'value': ['10', '', '20', 'END', '999']}


def node_loop(inputs):
    # Loop
    items = inputs.get('items', [])
    if not isinstance(items, list):
        raise TypeError('列表输入必须是 list')
    if len(items) > 1000:
        raise ValueError('输入列表超过循环上限')
    acc = []
    for index, item in enumerate(items):
        result = None
        if 'function' in inputs:
            result = inputs['function'](item)
            if inspect.isawaitable(result):
                result = asyncio.run(_await_result(result))
        else:
            if item == "END":
                break
            if not item:
                continue
            result = int(item)
        acc.append(result)
    return {'items': acc, 'count': len(acc)}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'rows'
        if True:
            results['rows'] = node_rows({})
        else:
            results['rows'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'rows', 'status': 'skipped' if results['rows'] is None else 'completed'})
            else:
                trace['rows'] = results['rows']
        current_node = 'loop'
        if results['rows'] is not None:
            results['loop'] = node_loop({'items': results['rows']['value']})
        else:
            results['loop'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'loop', 'status': 'skipped' if results['loop'] is None else 'completed'})
            else:
                trace['loop'] = results['loop']
        current_node = 'out'
        if results['loop'] is not None:
            results['out'] = node_out({'value': results['loop']['items']})
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
