# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi54yc5pWw5a2X5ri45oiP77ya6Zq+5bqm5LiO5b6q546vIiwid2VlayI6NSwiZGVzY3JpcHRpb24iOiJlYXN5IC8gbm9ybWFsIC8gaGFyZO+8m+WbuuWumumaj+acuuenjeWtkOWPr+mHjeWkjea1i+ivle+8jGlucHV0KCkg6L6T5YWl54yc5rWL44CCIiwic3RkaW4iOiJub3JtYWxcbjEwXG4zMFxuMjFcbiIsIm5vZGVzIjpbeyJpZCI6ImdhbWUiLCJ0eXBlIjoiUHl0aG9uIiwidGl0bGUiOiLnjJzmlbDlrZfpgLvovpEiLCJ4IjozMCwieSI6ODAsImNvbmZpZyI6eyJjb2RlIjoiaW1wb3J0IHJhbmRvbVxubGV2ZWxzID0geydlYXN5JzogKDIwLCA2KSwgJ25vcm1hbCc6ICg1MCwgNSksICdoYXJkJzogKDEwMCwgMyl9XG5sZXZlbCA9IGlucHV0KCfpmr7luqYgZWFzeS9ub3JtYWwvaGFyZO+8micpLnN0cmlwKClcbmlmIGxldmVsIG5vdCBpbiBsZXZlbHM6XG4gICAgcmFpc2UgVmFsdWVFcnJvcign5LiN5pSv5oyB55qE6Zq+5bqmJylcbnVwcGVyLCBtYXhfYXR0ZW1wdHMgPSBsZXZlbHNbbGV2ZWxdXG50YXJnZXQgPSByYW5kb20uUmFuZG9tKDcpLnJhbmRpbnQoMSwgdXBwZXIpXG5ndWVzc2VzLCB3b24gPSBbXSwgRmFsc2VcbmZvciBhdHRlbXB0IGluIHJhbmdlKG1heF9hdHRlbXB0cyk6XG4gICAgZ3Vlc3MgPSBpbnQoaW5wdXQoZifnrKwge2F0dGVtcHQgKyAxfSDmrKHnjJzmtYvvvJonKSlcbiAgICBndWVzc2VzLmFwcGVuZChndWVzcylcbiAgICBpZiBndWVzcyA9PSB0YXJnZXQ6XG4gICAgICAgIHdvbiA9IFRydWVcbiAgICAgICAgcHJpbnQoJ+eMnOWvueS6hu+8gScpXG4gICAgICAgIGJyZWFrXG4gICAgcHJpbnQoJ+WkquWwjycgaWYgZ3Vlc3MgPCB0YXJnZXQgZWxzZSAn5aSq5aSnJylcbnJlc3VsdCA9IHsnZGlmZmljdWx0eSc6IGxldmVsLCAnd29uJzogd29uLCAnYXR0ZW1wdHMnOiBsZW4oZ3Vlc3NlcyksICd0YXJnZXQnOiB0YXJnZXR9In19LHsiaWQiOiJvdXQiLCJ0eXBlIjoiT3V0cHV0IiwidGl0bGUiOiJPdXRwdXQiLCJ4IjozOTAsInkiOjgwLCJjb25maWciOnt9fV0sImVkZ2VzIjpbeyJzb3VyY2UiOiJnYW1lIiwib3V0IjoidmFsdWUiLCJ0YXJnZXQiOiJvdXQiLCJpbiI6InZhbHVlIn1dLCJjaGVja3MiOnsib3V0Ijp7InZhbHVlIjp7ImRpZmZpY3VsdHkiOiJub3JtYWwiLCJ3b24iOnRydWUsImF0dGVtcHRzIjozLCJ0YXJnZXQiOjIxfX19LCJ2ZXJpZmllZCI6dHJ1ZX0=
# FlowPy source sha256: 027edfda91be549aba34e63b4988bbfbd3d6ec87ea0d95b383bcf02ba0e782ad
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_game(inputs):
    # 猜数字逻辑
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    import random
    levels = {'easy': (20, 6), 'normal': (50, 5), 'hard': (100, 3)}
    level = input('难度 easy/normal/hard：').strip()
    if level not in levels:
        raise ValueError('不支持的难度')
    upper, max_attempts = levels[level]
    target = random.Random(7).randint(1, upper)
    guesses, won = [], False
    for attempt in range(max_attempts):
        guess = int(input(f'第 {attempt + 1} 次猜测：'))
        guesses.append(guess)
        if guess == target:
            won = True
            print('猜对了！')
            break
        print('太小' if guess < target else '太大')
    result = {'difficulty': level, 'won': won, 'attempts': len(guesses), 'target': target}
    return {'value': result}


def node_out(inputs):
    # Output
    return {'value': inputs.get('value', None)}


def run_graph(trace=None, context=None):
    results = {}
    current_node = None
    try:
        current_node = 'game'
        if True:
            results['game'] = node_game({})
        else:
            results['game'] = None
        if trace is not None:
            if isinstance(trace, list):
                trace.append({'node': 'game', 'status': 'skipped' if results['game'] is None else 'completed'})
            else:
                trace['game'] = results['game']
        current_node = 'out'
        if results['game'] is not None:
            results['out'] = node_out({'value': results['game']['value']})
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
