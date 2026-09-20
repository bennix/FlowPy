# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoiTGFtYmRhIOS4jumrmOmYtiBtYXAgLyBmaWx0ZXIiLCJ3ZWVrIjo5LCJkZXNjcmlwdGlvbiI6IuWMv+WQjeWHveaVsOS9nOS4uuS4gOetieWAvO+8m01hcCDlj5jmjaLmiJDnu6nvvIxGaWx0ZXIg5oyJ6LCT6K+N562b6YCJ44CCIiwic3RkaW4iOiIiLCJub2RlcyI6W3siaWQiOiJzY29yZXMiLCJ0eXBlIjoiQ29uc3RhbnQiLCJ0aXRsZSI6IkNvbnN0YW50IiwieCI6MzAsInkiOjgwLCJjb25maWciOnsidmFsdWUiOls0NSw1OSw2MCw4NSw5OF19fSx7ImlkIjoiYWRkIiwidHlwZSI6IkxhbWJkYSIsInRpdGxlIjoiTGFtYmRhIiwieCI6MzAsInkiOjM3MCwiY29uZmlnIjp7InBhcmFtcyI6InNjb3JlIiwiZXhwcmVzc2lvbiI6Im1pbihzY29yZSArIDUsIDEwMCkifX0seyJpZCI6Im1hcCIsInR5cGUiOiJNYXAiLCJ0aXRsZSI6Ik1hcCIsIngiOjM1MCwieSI6ODAsImNvbmZpZyI6e319LHsiaWQiOiJwYXNzaW5nIiwidHlwZSI6IkxhbWJkYSIsInRpdGxlIjoiTGFtYmRhIiwieCI6MzUwLCJ5IjozNzAsImNvbmZpZyI6eyJwYXJhbXMiOiJzY29yZSIsImV4cHJlc3Npb24iOiJzY29yZSA+PSA2MCJ9fSx7ImlkIjoiZmlsdGVyIiwidHlwZSI6IkZpbHRlciIsInRpdGxlIjoiRmlsdGVyIiwieCI6NjgwLCJ5Ijo4MCwiY29uZmlnIjp7fX0seyJpZCI6Im91dCIsInR5cGUiOiJPdXRwdXQiLCJ0aXRsZSI6Ik91dHB1dCIsIngiOjEwMTAsInkiOjgwLCJjb25maWciOnt9fV0sImVkZ2VzIjpbeyJzb3VyY2UiOiJzY29yZXMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im1hcCIsImluIjoiaXRlbXMifSx7InNvdXJjZSI6ImFkZCIsIm91dCI6ImZ1bmN0aW9uIiwidGFyZ2V0IjoibWFwIiwiaW4iOiJmdW5jdGlvbiJ9LHsic291cmNlIjoibWFwIiwib3V0IjoiaXRlbXMiLCJ0YXJnZXQiOiJmaWx0ZXIiLCJpbiI6Iml0ZW1zIn0seyJzb3VyY2UiOiJwYXNzaW5nIiwib3V0IjoiZnVuY3Rpb24iLCJ0YXJnZXQiOiJmaWx0ZXIiLCJpbiI6ImZ1bmN0aW9uIn0seyJzb3VyY2UiOiJmaWx0ZXIiLCJvdXQiOiJpdGVtcyIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOls2NCw2NSw5MCwxMDBdfX0sInZlcmlmaWVkIjp0cnVlfQ==
# FlowPy source sha256: 5fabc02f4a7e54d37952b7dbf33032ec2338031bfd87f2044438209248a1a079
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_scores(inputs):
    # Constant
    return {'value': [45, 59, 60, 85, 98]}


def node_add(inputs):
    # Lambda
    value = inputs.get('value')
    function = lambda score: min(score + 5, 100)
    return {'function': function}


def node_passing(inputs):
    # Lambda
    value = inputs.get('value')
    function = lambda score: score >= 60
    return {'function': function}


def node_map(inputs):
    # Map
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
            result = item
        acc.append(result)
    return {'items': acc, 'count': len(acc)}


def node_filter(inputs):
    # Filter
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
            result = bool(item)
        if not isinstance(result, bool):
            raise TypeError('Filter 谓词必须返回 bool')
        if result:
            acc.append(item)
    return {'items': acc, 'count': len(acc)}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'scores'
        if True:
            results['scores'] = node_scores({})
        else:
            results['scores'] = None
        if trace is not None:
            trace['scores'] = results['scores']
        current_node = 'add'
        if True:
            results['add'] = node_add({})
        else:
            results['add'] = None
        if trace is not None:
            trace['add'] = results['add']
        current_node = 'passing'
        if True:
            results['passing'] = node_passing({})
        else:
            results['passing'] = None
        if trace is not None:
            trace['passing'] = results['passing']
        current_node = 'map'
        if results['scores'] is not None and results['add'] is not None:
            results['map'] = node_map({'items': results['scores']['value'], 'function': results['add']['function']})
        else:
            results['map'] = None
        if trace is not None:
            trace['map'] = results['map']
        current_node = 'filter'
        if results['map'] is not None and results['passing'] is not None:
            results['filter'] = node_filter({'items': results['map']['items'], 'function': results['passing']['function']})
        else:
            results['filter'] = None
        if trace is not None:
            trace['filter'] = results['filter']
        current_node = 'out'
        if results['filter'] is not None:
            results['out'] = node_out({'value': results['filter']['items']})
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
