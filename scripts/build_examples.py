"""Build and verify the teaching examples before preserving JSON + Python pairs."""
import json
from pathlib import Path
import sys
import textwrap

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine import export_python
from server import execute


def code(source):
    return textwrap.dedent(source).strip()


def n(id, type, config=None, x=30, y=80, title=None):
    return {'id': id, 'type': type, 'title': title or type, 'x': x, 'y': y, 'config': config or {}}


def e(source, out, target, input):
    return {'source': source, 'out': out, 'target': target, 'in': input}


EXAMPLES = []


def save(slug, week, name, description, nodes, edges, expected, stdin=''):
    g = {'version': 1, 'name': name, 'week': week, 'description': description, 'stdin': stdin, 'nodes': nodes, 'edges': edges, 'checks': {'out': {'value': expected}}, 'verified': True}
    result = execute(g)
    if not result['ok']:
        raise RuntimeError('%s: %s' % (slug, result))
    if result['results']['out'] != g['checks']['out']:
        raise AssertionError('%s: %r != %r' % (slug, result['results']['out'], g['checks']['out']))
    (ROOT/'examples'/(slug+'.json')).write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'examples'/(slug+'.py')).write_text(export_python(g))
    EXAMPLES.append({'file':slug,'week':week,'name':name,'nodes':len(nodes),'status':'passed'})
    print('PASS',slug)


def linear(slug, week, name, description, value, program, expected):
    save(slug,week,name,description,[n('input','Constant',{'value':value},title='输入数据'),n('logic','Python',{'code':code(program)},350,title='Python 处理'),n('out','Output',{},700,title='结果')],[e('input','value','logic','value'),e('logic','value','out','value')],expected)


def build():
    linear('w02_bmi',2,'BMI 计算器','变量、数值运算、字典输入与边界校验；体重 kg / 身高 m。',{'weight':70,'height':1.75},'''
        weight, height = float(value['weight']), float(value['height'])
        if weight <= 0 or height <= 0:
            raise ValueError('体重和身高必须大于 0')
        bmi = weight / height ** 2
        category = '偏瘦' if bmi < 18.5 else '正常' if bmi < 24 else '超重' if bmi < 28 else '肥胖'
        result = {'bmi': round(bmi, 2), 'category': category}
    ''',{'bmi':22.86,'category':'正常'})
    save('w02_interactive',2,'交互式 BMI / input()','使用逐行标准输入重现交互；导出后可在终端实际输入。',[n('interactive','Python',{'code':code('''
        weight = float(input('体重(kg)：'))
        height = float(input('身高(m)：'))
        if weight <= 0 or height <= 0:
            raise ValueError('体重和身高必须为正数')
        result = round(weight / height ** 2, 2)
        print(f'BMI = {result}')
    ''')},title='输入与表达式'),n('out','Output',{},380)],[e('interactive','value','out','value')],22.86,'70\n1.75\n')
    linear('w02_types_operators',2,'基础类型与运算符','int / float / str / bool、算术、比较与逻辑运算。',{'a':17,'b':5},'''
        a, b = value['a'], value['b']
        result = {'sum': a+b, 'quotient': a//b, 'remainder': a%b,
                  'power': b**2, 'comparison': a>b and b>0,
                  'text': f'{a}/{b}', 'conversion': int('42')}
    ''',{'sum':22,'quotient':3,'remainder':2,'power':25,'comparison':True,'text':'17/5','conversion':42})
    linear('w03_ai_debug_log',3,'AI 调试日志：三次失败与修正','重现语法错误、幻觉函数与逻辑错误，验证修正后的结果。',None,r'''
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
    ''',[{'failure':'SyntaxError','fixed_result':3,'verified':True},{'failure':'AttributeError','fixed_result':16,'verified':True},{'failure':'AssertionError','fixed_result':22.86,'verified':True}])
    fn=code('''
        def safe_divide(pair):
            try:
                a, b = map(float, pair)
                return {'ok': True, 'value': a / b}
            except (ValueError, TypeError, ZeroDivisionError) as exc:
                print(type(exc).__name__, pair)
                return {'ok': False, 'error': type(exc).__name__}
    ''')
    save('w04_exceptions_logs',4,'异常捕获与打印调试','对正常输入、除零和无效数字逐项测试，异常不会中断整个批次。',[n('pairs','Constant',{'value':[[12,3],[1,0],['bad',2]]}),n('function','Function',{'name':'safe_divide','code':fn},340,330),n('map','Map',{},340),n('out','Output',{},700)],[e('pairs','value','map','items'),e('function','function','map','function'),e('map','items','out','value')],[{'ok':True,'value':4.0},{'ok':False,'error':'ZeroDivisionError'},{'ok':False,'error':'ValueError'}])
    save('w05_guess_number',5,'猜数字游戏：难度与循环','easy / normal / hard；固定随机种子可重复测试，input() 输入猜测。',[n('game','Python',{'code':code('''
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
    ''')},title='猜数字逻辑'),n('out','Output',{},390)],[e('game','value','out','value')],{'difficulty':'normal','won':True,'attempts':3,'target':21},'normal\n10\n30\n21\n')
    save('w05_loop_early_exit',5,'循环中的 continue / break','Loop 显式持有 item、index、acc；忽略空行并遇 END 停止。',[n('rows','Constant',{'value':['10','','20','END','999']}),n('loop','Loop',{'code':'if item == "END":\n    break\nif not item:\n    continue\nresult = int(item)'},350),n('out','Output',{},700)],[e('rows','value','loop','items'),e('loop','items','out','value')],[10,20])
    linear('w06_gradebook_list',6,'学生成绩管理：列表与元组','新增、修改、删除、排序与聚合；元组保留不可变记录。',[['Alice',85],['Bob',59],['Chen',92]],'''
        students = [list(row) for row in value]
        students.append(['Dora', 78])
        for row in students:
            if row[0] == 'Bob': row[1] = 65
        students = [row for row in students if row[0] != 'Dora']
        ranked = sorted((tuple(row) for row in students), key=lambda row: row[1], reverse=True)
        result = {'ranked': ranked, 'average': round(sum(row[1] for row in ranked)/len(ranked), 2), 'passed': sum(score >= 60 for _, score in ranked)}
    ''',{'ranked':[['Chen',92],['Alice',85],['Bob',65]],'average':80.67,'passed':3})
    linear('w07_gradebook_dict',7,'学生成绩管理：字典与集合','字典增删改查、集合交并差以及重复值消除。',{'Alice':85,'Bob':59,'Chen':92},'''
        scores = dict(value)
        scores.update(Bob=65, Dora=78)
        del scores['Dora']
        passed = {name for name, score in scores.items() if score >= 60}
        registered = {'Alice', 'Bob', 'Chen', 'Dora'}
        result = {'scores': scores, 'passed': sorted(passed), 'missing': sorted(registered-set(scores)), 'shared': sorted(passed & registered), 'unique_scores': sorted(set(scores.values()))}
    ''',{'scores':{'Alice':85,'Bob':65,'Chen':92},'passed':['Alice','Bob','Chen'],'missing':['Dora'],'shared':['Alice','Bob','Chen'],'unique_scores':[65,85,92]})
    linear('w07_lookup_comparison',7,'列表和字典的查找对比','同一批查询比较线性查找与字典查找，断言结果一致；不把耗时当正确性。',{'count':2000,'queries':[3,100,1999,2500]},'''
        records = [(i, i * 10) for i in range(value['count'])]
        index = dict(records)
        list_result = [next((score for key, score in records if key == q), None) for q in value['queries']]
        dict_result = [index.get(q) for q in value['queries']]
        assert list_result == dict_result
        result = {'same': True, 'results': dict_result, 'rows': len(records)}
    ''',{'same':True,'results':[30,1000,19990,None],'rows':2000})
    linear('w08_lottery',8,'标准库：双色球号码','random.Random 固定种子、sample 无重复抽样、排序与区间断言。',{'seed':42},'''
        import random
        rng = random.Random(value['seed'])
        red = sorted(rng.sample(range(1, 34), 6))
        blue = rng.randint(1, 16)
        assert len(set(red)) == 6 and all(1 <= n <= 33 for n in red)
        assert 1 <= blue <= 16
        result = {'red': red, 'blue': blue}
    ''',{'red':[2,8,9,24,29,33],'blue':5})
    save('w08_contacts_regex',8,'标准库：提取邮箱与手机号','仅做文本抽取：两个正则输出列表，再由 Python 合并结构化结果。',[n('text','LoadText',{'text':'联系 alice@example.com / bob@test.org；手机 13800138000、13912345678。'}),n('emails','RegexFindall',{'pattern':r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'},340),n('phones','RegexFindall',{'pattern':r'(?<!\d)1[3-9]\d{9}(?!\d)'},340,370),n('combine','Python',{'code':'result = {"emails": value, "phones": items}'},680),n('out','Output',{},1020)],[e('text','text','emails','text'),e('text','text','phones','text'),e('emails','matches','combine','value'),e('phones','matches','combine','items'),e('combine','value','out','value')],{'emails':['alice@example.com','bob@test.org'],'phones':['13800138000','13912345678']})
    linear('w08_loan',8,'标准库：等额本息月供','函数、math.pow 与零利率分支；年利率使用小数，例如 0.045。',{'principal':100000,'annual_rate':0.045,'months':360},'''
        import math
        principal, annual_rate, months = value['principal'], value['annual_rate'], value['months']
        if principal <= 0 or annual_rate < 0 or months <= 0 or int(months) != months:
            raise ValueError('贷款本金、利率或期数无效')
        rate = annual_rate / 12
        payment = principal / months if rate == 0 else principal * rate * math.pow(1 + rate, months) / (math.pow(1 + rate, months) - 1)
        result = {'monthly_payment': round(payment, 2), 'months': months}
    ''',{'monthly_payment':506.69,'months':360})
    save('w08_import_math',8,'模块导入与函数属性','ImportModule 导入 math.sqrt；函数引用通过连线传给 Call。',[n('import','ImportModule',{'module':'math','attribute':'sqrt'}),n('call','Call',{'args':[81]},350),n('out','Output',{},700)],[e('import','value','call','function'),e('call','value','out','value')],9.0)
    save('w08_string_constants',8,'标准库：string 与可重复随机字符串','string.ascii_letters / digits；教学用随机标识符，不作为密码。',[n('logic','Python',{'code':code('''
        import string
        import random
        rng = random.Random(12)
        alphabet = string.ascii_letters + string.digits
        token = ''.join(rng.choice(alphabet) for _ in range(12))
        result = {'length': len(token), 'valid': all(c in alphabet for c in token)}
    ''')}),n('out','Output',{},380)],[e('logic','value','out','value')],{'length':12,'valid':True})
    salary=code('''
        def salary(base, /, *bonuses, tax_rate=0.1, allowance=0, **metadata):
            if base < 0 or not 0 <= tax_rate <= 1:
                raise ValueError('薪资或税率无效')
            gross = base + sum(bonuses) + allowance
            return {'gross': round(gross, 2), 'net': round(gross * (1-tax_rate), 2), 'employee': metadata.get('employee', 'anonymous')}
    ''')
    save('w09_salary_functions',9,'薪资计算器：完整函数签名','位置限定参数、*bonuses、默认值、关键字参数和 **metadata。',[n('salary','Function',{'name':'salary','code':salary}),n('args','Constant',{'value':[10000,1000,500]},30,380),n('call','Call',{'kwargs':{'tax_rate':0.1,'allowance':200,'employee':'Alice'}},400),n('out','Output',{},760)],[e('salary','function','call','function'),e('args','value','call','args'),e('call','value','out','value')],{'gross':11700,'net':10530.0,'employee':'Alice'})
    save('w09_lambda_higher_order',9,'Lambda 与高阶 map / filter','匿名函数作为一等值；Map 变换成绩，Filter 按谓词筛选。',[n('scores','Constant',{'value':[45,59,60,85,98]}),n('add','Lambda',{'params':'score','expression':'min(score + 5, 100)'},30,370),n('map','Map',{},350),n('passing','Lambda',{'params':'score','expression':'score >= 60'},350,370),n('filter','Filter',{},680),n('out','Output',{},1010)],[e('scores','value','map','items'),e('add','function','map','function'),e('map','items','filter','items'),e('passing','function','filter','function'),e('filter','items','out','value')],[64,65,90,100])
    module_source=code('''
        def validate_scores(records):
            if not records or any(not 0 <= score <= 100 for score in records.values()):
                raise ValueError('成绩必须在 0 到 100 之间，且记录不为空')
            return dict(records)

        def summarize(records):
            scores = validate_scores(records)
            return {'count': len(scores), 'average': round(sum(scores.values())/len(scores),2), 'top': max(scores,key=scores.get)}
    ''')
    save('w10_modular_gradebook',10,'模块化重构：成绩管理','Module 定义独立命名空间 → Get 提取 summarize → Call 传入成绩。',[n('module','Module',{'name':'gradebook','code':module_source}),n('get','Get',{'path':'summarize'},350),n('call','Call',{'args':[{'Alice':85,'Bob':65,'Chen':92}]},680),n('out','Output',{},1010)],[e('module','value','get','value'),e('get','value','call','function'),e('call','value','out','value')],{'count':3,'average':80.67,'top':'Chen'})
    body={'version':1,'name':'验证单条学生记录','nodes':[n('item','Item',{'value':{'name':'Alice','score':85}}),n('check','Python',{'code':'if not isinstance(value, dict):\n    raise TypeError("记录必须是 dict")\nresult = {"name": value["name"], "passed": value["score"] >= 60}'},340),n('out','Output',{},680)],'edges':[e('item','value','check','value'),e('check','value','out','value')]}
    save('w10_nested_subgraph',10,'模块化重构：可视化子图','主画布只保留列表与 Map；进入 Map 子图编辑单条记录的处理。',[n('records','Constant',{'value':[{'name':'Alice','score':85},{'name':'Bob','score':59}]}),n('map','Map',{'body':body},350),n('out','Output',{},700)],[e('records','value','map','items'),e('map','items','out','value')],[{'name':'Alice','passed':True},{'name':'Bob','passed':False}])
    linear('w11_csv_json_roundtrip',11,'文件读写：CSV 与 JSON','用 tempfile 在临时目录真实写入并读回 Unicode CSV/JSON，验证内容一致。',[{'name':'小明','score':85},{'name':'小红','score':92}],'''
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
    ''',{'rows':[{'name':'小明','score':85},{'name':'小红','score':92}],'roundtrip':True})
    linear('w11_survey_collection',11,'问卷收集：校验、去重与保存','有效记录写入 artifacts/survey.csv 与 survey.json；保留错误报告。',[{'name':'Alice','age':'20','rating':'5'},{'name':'Bob','age':'-2','rating':'4'},{'name':'Chen','age':'22','rating':'3'},{'name':'Alice','age':'20','rating':'5'}],'''
        import csv, json
        from pathlib import Path
        accepted, errors, seen = [], [], set()
        for index, row in enumerate(value):
            try:
                name = row['name'].strip()
                age, rating = int(row['age']), int(row['rating'])
                if not name or not 0 < age < 130 or not 1 <= rating <= 5:
                    raise ValueError('字段超出有效范围')
                if name in seen:
                    raise ValueError('重复提交')
                seen.add(name)
                accepted.append({'name':name,'age':age,'rating':rating})
            except (ValueError, KeyError, TypeError) as exc:
                errors.append({'row':index+1,'error':str(exc)})
        output = Path('artifacts')
        output.mkdir(exist_ok=True)
        with (output/'survey.csv').open('w',newline='',encoding='utf-8') as file:
            writer = csv.DictWriter(file,fieldnames=['name','age','rating'])
            writer.writeheader()
            writer.writerows(accepted)
        (output/'survey.json').write_text(json.dumps(accepted,ensure_ascii=False,indent=2),encoding='utf-8')
        result = {'accepted':len(accepted),'rejected':len(errors),'records':accepted,'errors':errors}
    ''',{'accepted':2,'rejected':2,'records':[{'name':'Alice','age':20,'rating':5},{'name':'Chen','age':22,'rating':3}],'errors':[{'row':2,'error':'字段超出有效范围'},{'row':4,'error':'重复提交'}]})
    linear('w11_basic_pandas',11,'基础 pandas：表格清洗与筛选','DataFrame、dropna、astype、布尔筛选、列选择与 to_dict；无额外数据框架。',[{'name':'Alice','score':'85'},{'name':'Bob','score':None},{'name':'Chen','score':'59'},{'name':'Dora','score':'92'}],'''
        import pandas as pd
        frame = pd.DataFrame(value)
        frame = frame.dropna(subset=['score']).copy()
        frame['score'] = frame['score'].astype(int)
        passed = frame.loc[frame['score'] >= 60, ['name','score']].sort_values('score',ascending=False)
        result = {'records': passed.to_dict(orient='records'), 'count': len(passed), 'average': float(passed['score'].mean())}
    ''',{'records':[{'name':'Dora','score':92},{'name':'Alice','score':85}],'count':2,'average':88.5})
    report = {'examples': EXAMPLES, 'passed': len(EXAMPLES)}
    (ROOT/'examples'/'verification-report.md').write_text('# 已验证的课程流程\n\n所有流程均通过真实 Python 子进程执行，并与预期结果比较。每个流程保存 JSON 图与独立 Python 源码。\n\n| 周次 | 示例 | 状态 |\n|---|---|---|\n'+'\n'.join('| W%s | [%s](%s.json) | 通过 |' % (r['week'],r['name'],r['file']) for r in EXAMPLES)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    build()
