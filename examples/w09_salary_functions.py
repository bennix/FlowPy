# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi6Jaq6LWE6K6h566X5Zmo77ya5a6M5pW05Ye95pWw562+5ZCNIiwid2VlayI6OSwiZGVzY3JpcHRpb24iOiLkvY3nva7pmZDlrprlj4LmlbDjgIEqYm9udXNlc+OAgem7mOiupOWAvOOAgeWFs+mUruWtl+WPguaVsOWSjCAqKm1ldGFkYXRh44CCIiwic3RkaW4iOiIiLCJub2RlcyI6W3siaWQiOiJzYWxhcnkiLCJ0eXBlIjoiRnVuY3Rpb24iLCJ0aXRsZSI6IkZ1bmN0aW9uIiwieCI6MzAsInkiOjgwLCJjb25maWciOnsibmFtZSI6InNhbGFyeSIsImNvZGUiOiJkZWYgc2FsYXJ5KGJhc2UsIC8sICpib251c2VzLCB0YXhfcmF0ZT0wLjEsIGFsbG93YW5jZT0wLCAqKm1ldGFkYXRhKTpcbiAgICBpZiBiYXNlIDwgMCBvciBub3QgMCA8PSB0YXhfcmF0ZSA8PSAxOlxuICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCfolqrotYTmiJbnqI7njofml6DmlYgnKVxuICAgIGdyb3NzID0gYmFzZSArIHN1bShib251c2VzKSArIGFsbG93YW5jZVxuICAgIHJldHVybiB7J2dyb3NzJzogcm91bmQoZ3Jvc3MsIDIpLCAnbmV0Jzogcm91bmQoZ3Jvc3MgKiAoMS10YXhfcmF0ZSksIDIpLCAnZW1wbG95ZWUnOiBtZXRhZGF0YS5nZXQoJ2VtcGxveWVlJywgJ2Fub255bW91cycpfSJ9fSx7ImlkIjoiYXJncyIsInR5cGUiOiJDb25zdGFudCIsInRpdGxlIjoiQ29uc3RhbnQiLCJ4IjozMCwieSI6MzgwLCJjb25maWciOnsidmFsdWUiOlsxMDAwMCwxMDAwLDUwMF19fSx7ImlkIjoiY2FsbCIsInR5cGUiOiJDYWxsIiwidGl0bGUiOiJDYWxsIiwieCI6NDAwLCJ5Ijo4MCwiY29uZmlnIjp7Imt3YXJncyI6eyJ0YXhfcmF0ZSI6MC4xLCJhbGxvd2FuY2UiOjIwMCwiZW1wbG95ZWUiOiJBbGljZSJ9fX0seyJpZCI6Im91dCIsInR5cGUiOiJPdXRwdXQiLCJ0aXRsZSI6Ik91dHB1dCIsIngiOjc2MCwieSI6ODAsImNvbmZpZyI6e319XSwiZWRnZXMiOlt7InNvdXJjZSI6InNhbGFyeSIsIm91dCI6ImZ1bmN0aW9uIiwidGFyZ2V0IjoiY2FsbCIsImluIjoiZnVuY3Rpb24ifSx7InNvdXJjZSI6ImFyZ3MiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImNhbGwiLCJpbiI6ImFyZ3MifSx7InNvdXJjZSI6ImNhbGwiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsiZ3Jvc3MiOjExNzAwLCJuZXQiOjEwNTMwLjAsImVtcGxveWVlIjoiQWxpY2UifX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: cafe17126703754145cdae226e37113edb283bb24825c07d91c82c2c525fc6fd
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_salary(inputs):
    # Function
    value = inputs.get('value')
    def salary(base, /, *bonuses, tax_rate=0.1, allowance=0, **metadata):
        if base < 0 or not 0 <= tax_rate <= 1:
            raise ValueError('薪资或税率无效')
        gross = base + sum(bonuses) + allowance
        return {'gross': round(gross, 2), 'net': round(gross * (1-tax_rate), 2), 'employee': metadata.get('employee', 'anonymous')}
    if not callable(salary):
        raise TypeError('定义必须输出可调用对象')
    return {'function': salary}


def node_args(inputs):
    # Constant
    return {'value': [10000, 1000, 500]}


def node_call(inputs):
    # Call
    function = inputs.get('function')
    if not callable(function):
        raise TypeError('请连接函数定义、Lambda 或可调用对象')
    args = inputs.get('args', [])
    kwargs = inputs.get('kwargs', {'tax_rate': 0.1, 'allowance': 200, 'employee': 'Alice'})
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
        current_node = 'salary'
        if True:
            results['salary'] = node_salary({})
        else:
            results['salary'] = None
        if trace is not None:
            trace['salary'] = results['salary']
        current_node = 'args'
        if True:
            results['args'] = node_args({})
        else:
            results['args'] = None
        if trace is not None:
            trace['args'] = results['args']
        current_node = 'call'
        if results['salary'] is not None and results['args'] is not None:
            results['call'] = node_call({'function': results['salary']['function'], 'args': results['args']['value']})
        else:
            results['call'] = None
        if trace is not None:
            trace['call'] = results['call']
        current_node = 'out'
        if results['call'] is not None:
            results['out'] = node_out({'value': results['call']['value']})
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
