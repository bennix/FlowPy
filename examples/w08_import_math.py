# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5qih5Z2X5a+85YWl5LiO5Ye95pWw5bGe5oCnIiwid2VlayI6OCwiZGVzY3JpcHRpb24iOiJJbXBvcnRNb2R1bGUg5a+85YWlIG1hdGguc3FydO+8m+WHveaVsOW8leeUqOmAmui/h+i/nue6v+S8oOe7mSBDYWxs44CCIiwic3RkaW4iOiIiLCJub2RlcyI6W3siaWQiOiJpbXBvcnQiLCJ0eXBlIjoiSW1wb3J0TW9kdWxlIiwidGl0bGUiOiJJbXBvcnRNb2R1bGUiLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJtb2R1bGUiOiJtYXRoIiwiYXR0cmlidXRlIjoic3FydCJ9fSx7ImlkIjoiY2FsbCIsInR5cGUiOiJDYWxsIiwidGl0bGUiOiJDYWxsIiwieCI6MzUwLCJ5Ijo4MCwiY29uZmlnIjp7ImFyZ3MiOls4MV19fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoiT3V0cHV0IiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW1wb3J0Iiwib3V0IjoidmFsdWUiLCJ0YXJnZXQiOiJjYWxsIiwiaW4iOiJmdW5jdGlvbiJ9LHsic291cmNlIjoiY2FsbCIsIm91dCI6InZhbHVlIiwidGFyZ2V0Ijoib3V0IiwiaW4iOiJ2YWx1ZSJ9XSwiY2hlY2tzIjp7Im91dCI6eyJ2YWx1ZSI6OS4wfX0sInZlcmlmaWVkIjp0cnVlfQ==
# FlowPy source sha256: 4f6d267a40d44dee68ad5da5f1f816c8ad8f46560585edfb24d2342072f9f93d
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_import(inputs):
    # ImportModule
    import importlib
    value = importlib.import_module('math')
    for part in ['sqrt']:
        if part:
            value = getattr(value, part)
    return {'value': value}


def node_call(inputs):
    # Call
    function = inputs.get('function')
    if not callable(function):
        raise TypeError('请连接函数定义、Lambda 或可调用对象')
    args = inputs.get('args', [81])
    kwargs = inputs.get('kwargs', {})
    if not isinstance(args, list) or not isinstance(kwargs, dict):
        raise TypeError('args 必须是 list，kwargs 必须是 dict')
    if 'value' in inputs:
        args = [inputs['value'], *args]
    result = function(*args, **kwargs)
    if inspect.isawaitable(result):
        result = asyncio.run(_await_result(result))
    return {'value': result}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'import'
        if True:
            results['import'] = node_import({})
        else:
            results['import'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'import', 'status': 'skipped' if results['import'] is None else 'completed'})
            else:
                trace['import'] = results['import']
        current_node = 'call'
        if results['import'] is not None:
            results['call'] = node_call({'function': results['import']['value']})
        else:
            results['call'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'call', 'status': 'skipped' if results['call'] is None else 'completed'})
            else:
                trace['call'] = results['call']
        current_node = 'out'
        if results['call'] is not None:
            results['out'] = node_out({'value': results['call']['value']})
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
