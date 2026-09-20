# FlowPy graph v1: eyJ2ZXJzaW9uIjoxLCJuYW1lIjoi5paH5Lu26K+75YaZ77yaQ1NWIOS4jiBKU09OIiwid2VlayI6MTEsImRlc2NyaXB0aW9uIjoi55SoIHRlbXBmaWxlIOWcqOS4tOaXtuebruW9leecn+WunuWGmeWFpeW5tuivu+WbniBVbmljb2RlIENTVi9KU09O77yM6aqM6K+B5YaF5a655LiA6Ie044CCIiwic3RkaW4iOiIiLCJub2RlcyI6W3siaWQiOiJpbnB1dCIsInR5cGUiOiJDb25zdGFudCIsInRpdGxlIjoi6L6T5YWl5pWw5o2uIiwieCI6MzAsInkiOjgwLCJjb25maWciOnsidmFsdWUiOlt7Im5hbWUiOiLlsI/mmI4iLCJzY29yZSI6ODV9LHsibmFtZSI6IuWwj+e6oiIsInNjb3JlIjo5Mn1dfX0seyJpZCI6ImxvZ2ljIiwidHlwZSI6IlB5dGhvbiIsInRpdGxlIjoiUHl0aG9uIOWkhOeQhiIsIngiOjM1MCwieSI6ODAsImNvbmZpZyI6eyJjb2RlIjoiaW1wb3J0IGNzdiwganNvbiwgdGVtcGZpbGVcbmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aFxud2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyBmb2xkZXI6XG4gICAgZm9sZGVyID0gUGF0aChmb2xkZXIpXG4gICAgY3N2X3BhdGgsIGpzb25fcGF0aCA9IGZvbGRlci8nc2NvcmVzLmNzdicsIGZvbGRlci8nc2NvcmVzLmpzb24nXG4gICAgd2l0aCBjc3ZfcGF0aC5vcGVuKCd3JywgbmV3bGluZT0nJywgZW5jb2Rpbmc9J3V0Zi04JykgYXMgZmlsZTpcbiAgICAgICAgd3JpdGVyID0gY3N2LkRpY3RXcml0ZXIoZmlsZSwgZmllbGRuYW1lcz1bJ25hbWUnLCdzY29yZSddKVxuICAgICAgICB3cml0ZXIud3JpdGVoZWFkZXIoKVxuICAgICAgICB3cml0ZXIud3JpdGVyb3dzKHZhbHVlKVxuICAgIHdpdGggY3N2X3BhdGgub3BlbihlbmNvZGluZz0ndXRmLTgnLCBuZXdsaW5lPScnKSBhcyBmaWxlOlxuICAgICAgICByb3dzID0gW3snbmFtZSc6IHJvd1snbmFtZSddLCAnc2NvcmUnOiBpbnQocm93WydzY29yZSddKX0gZm9yIHJvdyBpbiBjc3YuRGljdFJlYWRlcihmaWxlKV1cbiAgICBqc29uX3BhdGgud3JpdGVfdGV4dChqc29uLmR1bXBzKHJvd3MsIGVuc3VyZV9hc2NpaT1GYWxzZSksIGVuY29kaW5nPSd1dGYtOCcpXG4gICAgcmVzdG9yZWQgPSBqc29uLmxvYWRzKGpzb25fcGF0aC5yZWFkX3RleHQoZW5jb2Rpbmc9J3V0Zi04JykpXG4gICAgYXNzZXJ0IHJlc3RvcmVkID09IHZhbHVlXG4gICAgcmVzdWx0ID0geydyb3dzJzogcmVzdG9yZWQsICdyb3VuZHRyaXAnOiBUcnVlfSJ9fSx7ImlkIjoib3V0IiwidHlwZSI6Ik91dHB1dCIsInRpdGxlIjoi57uT5p6cIiwieCI6NzAwLCJ5Ijo4MCwiY29uZmlnIjp7fX1dLCJlZGdlcyI6W3sic291cmNlIjoiaW5wdXQiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6ImxvZ2ljIiwiaW4iOiJ2YWx1ZSJ9LHsic291cmNlIjoibG9naWMiLCJvdXQiOiJ2YWx1ZSIsInRhcmdldCI6Im91dCIsImluIjoidmFsdWUifV0sImNoZWNrcyI6eyJvdXQiOnsidmFsdWUiOnsicm93cyI6W3sibmFtZSI6IuWwj+aYjiIsInNjb3JlIjo4NX0seyJuYW1lIjoi5bCP57qiIiwic2NvcmUiOjkyfV0sInJvdW5kdHJpcCI6dHJ1ZX19fSwidmVyaWZpZWQiOnRydWV9
# FlowPy source sha256: 4e1cf6d1dbb164f8a5b3b3884c315d5df518db1bd2ba4533de905a103d5d90c7
import re
import inspect
import asyncio


async def _await_result(value):
    return await value


def node_input(inputs):
    # 输入数据
    return {'value': [{'name': '小明', 'score': 85}, {'name': '小红', 'score': 92}]}


def node_logic(inputs):
    # Python 处理
    value = inputs.get('value')
    items = inputs.get('items', [])
    text = inputs.get('text', '')
    index = inputs.get('index', 0)
    acc = inputs.get('acc', [])
    result = None
    import csv, json, tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        csv_path, json_path = folder/'scores.csv', folder/'scores.json'
        with csv_path.open('w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name','score'])
            writer.writeheader()
            writer.writerows(value)
        with csv_path.open(encoding='utf-8', newline='') as file:
            rows = [{'name': row['name'], 'score': int(row['score'])} for row in csv.DictReader(file)]
        json_path.write_text(json.dumps(rows, ensure_ascii=False), encoding='utf-8')
        restored = json.loads(json_path.read_text(encoding='utf-8'))
        assert restored == value
        result = {'rows': restored, 'roundtrip': True}
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
