"""FlowPy graph validation and readable, standalone Python generation."""
import ast
import base64
import hashlib
import json
import re

# Data types are also the connection contract used by the editor.
SPECS = {
    'ImportModule': ({}, {'value': 'any'}),
    'Module': ({}, {'value': 'any'}),
    'Item': ({}, {'value': 'any', 'index': 'number', 'acc': 'list'}),
    'LoadText': ({}, {'text': 'str'}),
    'Constant': ({}, {'value': 'any'}),
    'RegexMatch': ({'text': 'str', 'pattern': 'str'}, {'ok': 'bool', 'groups': 'dict', 'matches': 'list', 'span': 'list'}),
    'RegexFindall': ({'text': 'str', 'pattern': 'str'}, {'matches': 'list', 'ok': 'bool'}),
    'RegexSub': ({'text': 'str', 'pattern': 'str', 'repl': 'any'}, {'text': 'str'}),
    'RegexSplit': ({'text': 'str', 'pattern': 'str'}, {'parts': 'list'}),
    'RegexSwitch': ({'text': 'str'}, {'case': 'any', 'groups': 'dict', 'ok': 'bool'}),
    'Get': ({'value': 'any'}, {'value': 'any'}),
    'If': ({'condition': 'bool', 'value': 'any'}, {'true': 'bool', 'false': 'bool', 'value': 'any'}),
    'Switch': ({'value': 'any'}, {'case': 'any', 'matched': 'bool', 'default': 'bool', 'value': 'any'}),
    'Map': ({'items': 'list', 'function': 'any'}, {'items': 'list', 'count': 'number'}),
    'Filter': ({'items': 'list', 'function': 'any'}, {'items': 'list', 'count': 'number'}),
    'Loop': ({'items': 'list', 'function': 'any'}, {'items': 'list', 'count': 'number'}),
    'Python': ({'value': 'any', 'items': 'list', 'text': 'str', 'index': 'number', 'acc': 'list'}, {'value': 'any'}),
    'Function': ({'value': 'any'}, {'function': 'any'}),
    'Lambda': ({'value': 'any'}, {'function': 'any'}),
    'Call': ({'function': 'any', 'args': 'list', 'kwargs': 'dict', 'value': 'any'}, {'value': 'any'}),
    'Assert': ({'value': 'any', 'expected': 'any'}, {'passed': 'bool', 'value': 'any'}),
    'Output': ({'value': 'any'}, {'value': 'any'}),
}
FLAGS = {'IGNORECASE', 'MULTILINE', 'DOTALL', 'VERBOSE'}


class GraphError(ValueError):
    pass


def node_spec(node):
    inputs, outputs = SPECS[node['type']]
    if node['type'] == 'Switch':
        cases = node.get('config', {}).get('cases', [])
        if not isinstance(cases, list) or len(cases) > 30:
            raise GraphError('Switch cases 必须是最多 30 项的列表。')
        outputs = dict(outputs, **{'case_%s' % i: 'bool' for i in range(len(cases))})
    return inputs, outputs


def validate(graph, depth=0):
    if depth > 8:
        raise GraphError('子图嵌套不能超过 8 层。')
    if not isinstance(graph, dict):
        raise GraphError('工作流必须是 JSON 对象。')
    if not isinstance(graph.get('stdin', ''), str):
        raise GraphError('stdin 必须是字符串，每行对应一次 input()。')
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise GraphError('nodes 和 edges 必须是列表。')
    if not nodes:
        raise GraphError('画布为空，请先添加节点。')
    if len(nodes) > 200 or len(edges) > 1000:
        raise GraphError('最多支持 200 个节点、1000 条连接。')
    by_id = {}
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get('config', {}), dict):
            raise GraphError('节点及其 config 必须是对象。')
        nid = node.get('id', '')
        if not isinstance(nid, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,63}', nid) or nid in by_id:
            raise GraphError('节点 ID 不合法或重复。')
        if not isinstance(node.get('type'), str) or node.get('type') not in SPECS:
            raise GraphError('未知节点类型：' + str(node.get('type')))
        node_spec(node)
        body = node.get('config', {}).get('body')
        if body is not None and node['type'] in ('Map', 'Filter', 'Loop'):
            validate(body, depth + 1)
            if len([n for n in body['nodes'] if n['type'] == 'Output']) != 1:
                raise GraphError('子图必须恰好有一个 Output 节点。')
        by_id[nid] = node
    incoming = {nid: {} for nid in by_id}
    degree = {nid: 0 for nid in by_id}
    children = {nid: [] for nid in by_id}
    for edge in edges:
        if not isinstance(edge, dict) or any(not isinstance(edge.get(key), str) for key in ('source', 'target', 'out', 'in')):
            raise GraphError('连接必须包含字符串 source、target、out、in。')
        src, dst = edge.get('source'), edge.get('target')
        if src not in by_id or dst not in by_id:
            raise GraphError('连接指向不存在的节点。')
        out, inp = edge.get('out'), edge.get('in')
        outputs = node_spec(by_id[src])[1]
        inputs = dict(node_spec(by_id[dst])[0], gate='bool')
        if out not in outputs or inp not in inputs:
            raise GraphError('连接端口不存在。')
        if inp in incoming[dst]:
            raise GraphError('每个输入端口只能连接一个输出。')
        if outputs[out] != 'any' and inputs[inp] != 'any' and outputs[out] != inputs[inp]:
            raise GraphError('端口类型不兼容：%s → %s' % (outputs[out], inputs[inp]))
        incoming[dst][inp] = edge
        degree[dst] += 1
        children[src].append(dst)
    ready = [nid for nid in by_id if degree[nid] == 0]
    order = []
    while ready:
        nid = ready.pop(0)
        order.append(nid)
        for child in children[nid]:
            degree[child] -= 1
            if degree[child] == 0:
                ready.append(child)
    if len(order) != len(nodes):
        raise GraphError('不允许环形连接；重复操作请使用 Map / Loop 的内部循环。')
    return by_id, incoming, order


def _body(node):
    t, c = node['type'], node.get('config', {})
    flags = c.get('flags', [])
    if not isinstance(flags, list) or any(f not in FLAGS for f in flags):
        raise GraphError('不支持的正则 flags。')
    flag_expr = ' | '.join('re.' + f for f in flags) or '0'
    pat = "inputs.get('pattern', %r)" % c.get('pattern', '')
    text = "inputs.get('text', %r)" % c.get('text', '')
    if t == 'ImportModule':
        return ['import importlib', f"value = importlib.import_module({c.get('module', 'math')!r})", f"for part in {c.get('attribute', '').split('.')!r}:", '    if part:', '        value = getattr(value, part)', "return {'value': value}"]
    if t == 'Module':
        return ['import types, sys', f"module = types.ModuleType({c.get('name', 'gradebook')!r})", "sys.modules[module.__name__] = module", f"exec(compile({c.get('code', '')!r}, '<module>', 'exec'), module.__dict__)", "return {'value': module}"]
    if t == 'Item':
        return ["return {'value': inputs.get('value', %r), 'index': inputs.get('index', 0), 'acc': inputs.get('acc', [])}" % c.get('value', 'ORD-123456')]
    if t == 'LoadText':
        return ["return {'text': %r}" % c.get('text', '')]
    if t == 'Constant':
        return ["return {'value': %r}" % c.get('value', '')]
    if t.startswith('Regex'):
        lines = [f'text = {text}', f'flags = {flag_expr}']
        if t == 'RegexSwitch':
            rules = c.get('rules', [])
            if not isinstance(rules, list) or any(not isinstance(r, dict) or 'pattern' not in r or 'case' not in r for r in rules):
                raise GraphError('规则必须是含 pattern 和 case 的对象列表。')
            return lines + [f'for rule in {rules!r}:', "    match = re.search(rule['pattern'], text, flags)", '    if match:', "        return {'case': rule['case'], 'groups': match.groupdict(), 'ok': True}", "return {'case': None, 'groups': {}, 'ok': False}"]
        lines.append(f'pattern = {pat}')
        if t == 'RegexMatch':
            return lines + ['match = re.search(pattern, text, flags)', "return {'ok': match is not None, 'groups': match.groupdict() if match else {},", "        'matches': [match.group(0)] if match else [], 'span': list(match.span()) if match else None}"]
        if t == 'RegexFindall':
            return lines + ['matches = re.findall(pattern, text, flags)', "return {'matches': matches, 'ok': bool(matches)}"]
        if t == 'RegexSub':
            return lines + ["repl = inputs.get('repl', %r)" % c.get('repl', ''), "return {'text': re.sub(pattern, repl, text, flags=flags)}"]
        return lines + ["return {'parts': re.split(pattern, text, flags=flags)}"]
    if t == 'Get':
        return ["value = inputs.get('value')", f"for key in {c.get('path', '').split('.')!r}:", "    if key:", "        value = value[int(key)] if isinstance(value, (list, tuple)) else value[key] if isinstance(value, dict) else getattr(value, key)", "return {'value': value}"]
    if t == 'If':
        return ["condition = inputs.get('condition', %r)" % c.get('condition', False), "if not isinstance(condition, bool):", "    raise TypeError('If 的 condition 必须是 bool')", "if condition:", "    return {'true': True, 'false': False, 'value': inputs.get('value')}", "return {'true': False, 'false': True, 'value': inputs.get('value')}"]
    if t == 'Switch':
        cases = c.get('cases', [])
        return ["value = inputs.get('value')", f"cases = {cases!r}", "selected = next((i for i, case in enumerate(cases) if case == value), None)", "result = {'case': value if selected is not None else None, 'matched': selected is not None, 'default': selected is None, 'value': value}", "for i in range(len(cases)):", "    result[f'case_{i}'] = selected == i", "return result"]
    if t == 'Function':
        name = c.get('name', 'transform')
        if not name.isidentifier() or name.startswith('__'):
            raise GraphError('函数名称必须是合法的 Python 标识符。')
        code = c.get('code', 'def transform(value):\n    return value')
        return ["value = inputs.get('value')"] + code.splitlines() + [f"if not callable({name}):", "    raise TypeError('定义必须输出可调用对象')", f"return {{'function': {name}}}"]
    if t == 'Lambda':
        return ["value = inputs.get('value')", f"function = lambda {c.get('params', 'x')}: {c.get('expression', 'x')}", "return {'function': function}"]
    if t == 'Call':
        return ["function = inputs.get('function')", "if not callable(function):", "    raise TypeError('请连接函数定义、Lambda 或可调用对象')", f"args = inputs.get('args', {c.get('args', [])!r})", f"kwargs = inputs.get('kwargs', {c.get('kwargs', {})!r})", "if not isinstance(args, list) or not isinstance(kwargs, dict):", "    raise TypeError('args 必须是 list，kwargs 必须是 dict')", "if 'value' in inputs:", "    args = [inputs['value'], *args]", "result = function(*args, **kwargs)", "if inspect.isawaitable(result):", "    result = asyncio.run(_await_result(result))", "return {'value': result}"]
    if t in ('Map', 'Filter', 'Loop'):

        code = c.get('code', 'result = item' if t != 'Filter' else 'result = bool(item)')
        # Loop's body may use break / continue, validated in its actual generated context.
        limit = c.get('limit', 1000)
        if not isinstance(limit, int) or not 1 <= limit <= 100000:
            raise GraphError('循环上限必须在 1–100000 之间。')
        subgraph = c.get('body')
        prefix = source_body(subgraph, standalone=False).splitlines() if subgraph else []
        lines = prefix + ["items = inputs.get('items', [])", "if not isinstance(items, list):", "    raise TypeError('列表输入必须是 list')", f'if len(items) > {limit}:', "    raise ValueError('输入列表超过循环上限')", 'acc = []', 'for index, item in enumerate(items):', '    result = None']
        lines += ["    if 'function' in inputs:", "        result = inputs['function'](item)", "        if inspect.isawaitable(result):", "            result = asyncio.run(_await_result(result))", "    else:"]
        if subgraph:
            output_id = next(n['id'] for n in subgraph['nodes'] if n['type'] == 'Output')
            lines += ["        inner = run_graph(context={'value': item, 'index': index, 'acc': list(acc)})", f"        output = inner[{output_id!r}]", "        result = output['value'] if output is not None else None"]
        else:
            lines += ['        ' + line for line in (code.splitlines() or ['pass'])]
        if t == 'Filter':
            lines += ["    if not isinstance(result, bool):", "        raise TypeError('Filter 谓词必须返回 bool')", '    if result:', '        acc.append(item)']
        else:
            lines += ['    acc.append(result)']
        return lines + ["return {'items': acc, 'count': len(acc)}"]
    if t == 'Assert':
        return ["value = inputs.get('value')", f"expected = inputs.get('expected', {c.get('expected', None)!r})", "if value != expected:", "    raise AssertionError(f'预期 {expected!r}，实际 {value!r}')", "return {'passed': True, 'value': value}"]
    if t == 'Python':
        code = c.get('code', 'result = value')
        return ["value = inputs.get('value')", "items = inputs.get('items', [])", "text = inputs.get('text', '')", "index = inputs.get('index', 0)", "acc = inputs.get('acc', [])", 'result = None'] + code.splitlines() + ["return {'value': result}"]
    return ["return {'value': inputs.get('value', %r)}" % c.get('value', None)]


def source_body(graph, standalone=True):
    by_id, incoming, order = validate(graph)
    lines = ['import re', 'import inspect', 'import asyncio', '', '', 'async def _await_result(value):', '    return await value', '', '']
    for nid in order:
        node = by_id[nid]
        title = str(node.get('title', node['type'])).replace('\n', ' ').replace('\r', ' ')
        lines += [f'def node_{nid}(inputs):', '    # ' + title]
        lines += ['    ' + line for line in _body(node)]
        lines += ['', '']
    lines += ['def run_graph(trace=None, context=None):', '    results = {}', '    current_node = None', '    try:']
    for nid in order:
        ins = incoming[nid]
        dependencies = list(dict.fromkeys(e['source'] for e in ins.values()))
        conds = [f'results[{dep!r}] is not None' for dep in dependencies]
        lines += [f'        current_node = {nid!r}']
        if 'gate' in ins:
            e = ins['gate']
            gate_value = f"results[{e['source']!r}][{e['out']!r}]"
            ready = ' and '.join(conds) or 'True'
            lines += [f'        if {ready} and not isinstance({gate_value}, bool):', "            raise TypeError('gate 必须是 bool')"]
            conds.append(f"results[{e['source']!r}][{e['out']!r}] is True")
        expr = ', '.join(f"{port!r}: results[{e['source']!r}][{e['out']!r}]" for port, e in ins.items() if port != 'gate')
        if by_id[nid]['type'] == 'Item':
            expr = '**(context or {})'
        lines += [f"        if {' and '.join(conds) or 'True'}:", f'            results[{nid!r}] = node_{nid}({{{expr}}})', '        else:', f'            results[{nid!r}] = None', '        if trace is not None:', '            if isinstance(trace, list):', f"                trace.append({{'node': {nid!r}, 'status': 'skipped' if results[{nid!r}] is None else 'completed'}})", '            else:', f'                trace[{nid!r}] = results[{nid!r}]']
    lines += ['    except Exception as exc:', "        raise RuntimeError(f'节点 {current_node}: {exc}') from exc", '    return results', '', '']
    if standalone:
        lines += ["if __name__ == '__main__':", '    from pprint import pprint', '    pprint(run_graph())', '']
    source = '\n'.join(lines)
    try:
        compile(source, '<graph>', 'exec')
    except SyntaxError as exc:
        raise GraphError('Python 语法错误，第 %s 行：%s' % (exc.lineno, exc.msg)) from exc
    return source


def export_python(graph):
    body = source_body(graph)
    payload = base64.b64encode(json.dumps(graph, ensure_ascii=False, separators=(',', ':')).encode()).decode()
    digest = hashlib.sha256(body.encode()).hexdigest()
    return '# FlowPy graph v1: ' + payload + '\n# FlowPy source sha256: ' + digest + '\n' + body


def import_python(source):
    source = source.replace('\r\n', '\n').replace('\r', '\n')
    try:
        ast.parse(source)
    except SyntaxError as exc:
        raise GraphError('Python 语法错误：' + str(exc)) from exc
    lines = source.splitlines(keepends=True)
    if len(lines) >= 2 and lines[0].startswith('# FlowPy graph v1: ') and lines[1].startswith('# FlowPy source sha256: '):
        body = ''.join(lines[2:])
        digest = lines[1].split(': ', 1)[1].strip()
        if hashlib.sha256(body.encode()).hexdigest() == digest:
            try:
                graph = json.loads(base64.b64decode(lines[0].split(': ', 1)[1]))
                if source_body(graph) == body:
                    return {'graph': graph, 'mode': 'roundtrip', 'message': '已恢复全部节点、连接和画布布局。'}
            except (ValueError, TypeError, KeyError) as exc:
                raise GraphError('图元数据无效：' + str(exc)) from exc
    # Keep arbitrary code intact: exec uses one shared global namespace so functions
    # can refer to imported modules and module-level variables, as in a Python file.
    code = "namespace = {'__name__': '__main__'}\nexec(compile(%r, '<imported.py>', 'exec'), namespace, namespace)\nresult = namespace.get('result')" % source
    graph = {'version': 1, 'name': 'Imported Python', 'nodes': [{'id': 'python1', 'type': 'Python', 'title': '导入的 Python', 'x': 280, 'y': 160, 'config': {'code': code}}], 'edges': []}
    return {'graph': graph, 'mode': 'opaque', 'message': '完整代码已封装为一个 Python 节点。任意源码或修改后的导出源码不会被猜测拆图；使用 result 变量提供节点输出。'}
