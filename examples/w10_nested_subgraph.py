# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5qih5Z2X5YyW6YeN5p6E77ya5Y+v6KeG5YyW5a2Q5Zu+Iiwid2VlayI6MTAsImRlc2NyaXB0aW9uIjoi5Li755S75biD5Y+q5L+d55WZ5YiX6KGo5LiOIE1hcO+8m+i/m+WFpSBNYXAg5a2Q5Zu+57yW6L6R5Y2V5p2h6K6w5b2V55qE5aSE55CG44CCIiwic3RkaW4iOiIiLCJub2RlcyI6W3siaWQiOiJyZWNvcmRzIiwidHlwZSI6IkNvbnN0YW50IiwidGl0bGUiOiJDb25zdGFudCIsIngiOjMwLCJ5Ijo4MCwiY29uZmlnIjp7InZhbHVlIjpbeyJuYW1lIjoiQWxpY2UiLCJzY29yZSI6ODV9LHsibmFtZSI6IkJvYiIsInNjb3JlIjo1OX1dfX0seyJpZCI6Im1hcCIsInR5cGUiOiJNYXAiLCJ0aXRsZSI6Ik1hcCIsIngiOjM1MCwieSI6ODAsImNvbmZpZyI6eyJib2R5Ijp7InZlcnNpb24iOjEsIm5hbWUiOiLpqozor4HljZXmnaHlrabnlJ/orrDlvZUiLCJub2RlcyI6W3siaWQiOiJpdGVtIiwidHlwZSI6Ikl0ZW0iLCJ0aXRsZSI6Ikl0ZW0iLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJ2YWx1ZSI6eyJuYW1lIjoiQWxpY2UiLCJzY29yZSI6ODV9fX0seyJpZCI6ImNoZWNrIiwidHlwZSI6IlB5dGhvbiIsInRpdGxlIjoiUHl0aG9uIiwieCI6MzQwLCJ5Ijo4MCwiY29uZmlnIjp7ImNvZGUiOiJpZiBub3QgaXNpbnN0YW5jZSh2YWx1ZSwgZGljdCk6XG4gICAgcmFpc2UgVHlwZUVycm9yKFwi6K6w5b2V5b+F6aG75pivIGRpY3RcIilcbnJlc3VsdCA9IHtcIm5hbWVcIjogdmFsdWVbXCJuYW1lXCJdLCBcInBhc3NlZFwiOiB2YWx1ZVtcInNjb3JlXCJdID49IDYwfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoiT3V0cHV0IiwieCI6NjgwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaXRlbSIsIm91dCI6InZhbHVlIiwidGFyZ2V0IjoiY2hlY2siLCJpbiI6InZhbHVlIn0seyJzb3VyY2UiOiJjaGVjayIsIm91dCI6InZhbHVlIiwidGFyZ2V0Ijoib3V0IiwiaW4iOiJ2YWx1ZSJ9XX19fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoiT3V0cHV0IiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoicmVjb3JkcyIsIm91dCI6InZhbHVlIiwidGFyZ2V0IjoibWFwIiwiaW4iOiJpdGVtcyJ9LHsic291cmNlIjoibWFwIiwib3V0IjoiaXRlbXMiLCJ0YXJnZXQiOiJvdXQiLCJpbiI6InZhbHVlIn1dLCJjaGVja3MiOnsib3V0Ijp7InZhbHVlIjpbeyJuYW1lIjoiQWxpY2UiLCJwYXNzZWQiOnRydWV9LHsibmFtZSI6IkJvYiIsInBhc3NlZCI6ZmFsc2V9XX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: 5fa8478a51456e1ea9e4c2aba4dea5f4e479a5bee333ba714c9021e80fc1106b
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_records(inputs):
    # Constant
    return {'value': [{'name': 'Alice', 'score': 85}, {'name': 'Bob', 'score': 59}]}


def node_map(inputs):
    # Map
    import re
    import inspect
    import asyncio
    
    
    async def _await_result(value):
        return await value
    
    
    def node_item(inputs):
        # Item
        return {'value': inputs.get('value', {'name': 'Alice', 'score': 85}), 'index': inputs.get('index', 0), 'acc': inputs.get('acc', [])}
    
    
    def node_check(inputs):
        # Python
        value = inputs.get('value')
        items = inputs.get('items', [])
        text = inputs.get('text', '')
        index = inputs.get('index', 0)
        acc = inputs.get('acc', [])
        result = None
        if not isinstance(value, dict):
            raise TypeError("记录必须是 dict")
        result = {"name": value["name"], "passed": value["score"] >= 60}
        return {'value': result}
    
    
    def node_out(inputs):
        # Output
        return {'value': inputs.get('value', None)}
    
    
    def run_graph(trace=None, context=None):
        results = {}
        current_node = None
        try:
            current_node = 'item'
            if True:
                results['item'] = node_item({**(context or {})})
            else:
                results['item'] = None
            if trace is not None:
                trace['item'] = results['item']
            current_node = 'check'
            if results['item'] is not None:
                results['check'] = node_check({'value': results['item']['value']})
            else:
                results['check'] = None
            if trace is not None:
                trace['check'] = results['check']
            current_node = 'out'
            if results['check'] is not None:
                results['out'] = node_out({'value': results['check']['value']})
            else:
                results['out'] = None
            if trace is not None:
                trace['out'] = results['out']
        except Exception as exc:
            raise RuntimeError(f'节点 {current_node}: {exc}') from exc
        return results
    
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
            inner = run_graph(context={'value': item, 'index': index, 'acc': list(acc)})
            output = inner['out']
            result = output['value'] if output is not None else None
        acc.append(result)
    return {'items': acc, 'count': len(acc)}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'records'
        if True:
            results['records'] = node_records({})
        else:
            results['records'] = None
        if trace is not None:
            trace['records'] = results['records']
        current_node = 'map'
        if results['records'] is not None:
            results['map'] = node_map({'items': results['records']['value']})
        else:
            results['map'] = None
        if trace is not None:
            trace['map'] = results['map']
        current_node = 'out'
        if results['map'] is not None:
            results['out'] = node_out({'value': results['map']['items']})
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
