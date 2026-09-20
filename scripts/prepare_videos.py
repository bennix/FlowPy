import asyncio
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import textwrap

import edge_tts

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from server import execute


def make_steps(g):
    steps=[{'action':'start','text':f'这一节演示{g["name"]}。现在画布完全为空，没有节点，也没有连线。我们从节点库开始，一步一步搭建，最后运行验证。'}]
    def scope(body,prefix=''):
        added=set()
        for node in body['nodes']:
            t=node['type']; cfg=node.get('config',{})
            explanation={
                'Constant':'在右侧填入本例的数据。常量可以是数字、字符串、列表或字典，使用合法的 JSON 格式。',
                'LoadText':'在右侧输入要处理的原始文本，后续节点通过连线取得字符串。',
                'Python':'把处理逻辑写在这个节点里，输入由连线传入，结果写入 result。这样主画布保持简洁。',
                'Function':'填写函数源码和输出函数名。这里保留 Python 原生参数规则，定义函数和调用函数分开。',
                'Lambda':'填写参数和返回表达式，匿名函数也可以沿着连线传递。',
                'Call':'填写位置参数和关键字参数。调用节点负责把参数传给上游函数。',
                'Map':'这个节点逐项处理列表。具体逻辑可以来自函数回调，也可以放在内部子图。',
                'Filter':'这个节点只负责筛选。谓词返回真时保留当前项，返回假时丢弃。',
                'Loop':'输入循环体代码。使用 item 读取当前项，continue 跳过，break 提前结束。',
                'If':'分支节点只检查布尔值。true 和 false 出口连接到后续节点的 gate。',
                'Output':'这个节点收集最终结果，运行后可以在底部查看。',
                'RegexMatch':'输入正则表达式。匹配节点输出布尔值和分组字典，不负责跳转。',
                'RegexFindall':'输入正则表达式，一次提取所有匹配，输出列表。',
                'Module':'填写模块名称和源码。相关函数放在独立命名空间内，方便复用。',
                'ImportModule':'填写模块名称及属性路径，取得标准库中的函数引用。',
                'Get':'填写要读取的字段或属性路径。这里可以从模块中取得指定函数。',
                'Item':'设置单独测试子图时使用的数据。正式循环时，这里会接收到列表当前项。',
            }.get(t,'在右侧填写本例需要的参数。')
            steps.append({'action':'node','scope':prefix,'node':node,'text':f'添加 {t} 节点。'+explanation})
            if cfg.get('body'):
                steps.append({'action':'enter','scope':prefix,'node_id':node['id'],'text':'进入可视化子图。子画布同样从空白开始，逐个建立单项处理流程。'})
                scope(cfg['body'],prefix+node['id']+'/')
                steps.append({'action':'leave','text':'子图已经连接完成。返回主画布，Map 会对列表中的每条记录执行这个子流程。'})
            added.add(node['id'])
            for edge in body['edges']:
                if edge['target']==node['id'] and edge['source'] in added:
                    source=next(n for n in body['nodes'] if n['id']==edge['source'])
                    steps.append({'action':'edge','scope':prefix,'edge':edge,'text':f'点击 {source["type"]} 的 {edge["out"]} 输出，再点击 {t} 的 {edge["in"]} 输入，建立这条'+('控制连线。只有条件为真，下游才会执行。' if edge['in']=='gate' else '数据连线。下游现在直接使用上游结果。')})
        # Handle edges whose source appears after its target in the stored presentation order.
        positions={n['id']:i for i,n in enumerate(body['nodes'])}
        for edge in body['edges']:
            if positions[edge['source']]>positions[edge['target']]:
                steps.append({'action':'edge','scope':prefix,'edge':edge,'text':f'连接 {edge["out"]} 输出与 {edge["in"]} 输入，让函数或数据进入对应节点。'})
    scope(g)
    if g.get('stdin'):
        steps.append({'action':'stdin','value':g['stdin'],'text':'点击输入，逐行填写交互测试数据。程序每调用一次 input，就读取一行，便于重复验证同一个过程。'})
    steps.append({'action':'run','text':'节点和连线已经搭建完成。现在点击运行工作流，由真实的 Python 执行所有激活节点。'})
    steps.append({'action':'result','text':'运行成功。底部显示每个节点的实际输出，结果已与本例预期值核对。这个例子从空白画布开始，现已完整跑通。'})
    return steps


def prepare():
    app=(ROOT/'web/app.js').read_text()
    prefix=app[:app.index('let graph =')]
    starter=json.loads(subprocess.check_output(['node','-e','const vm=require("vm"); const fs=require("fs"); const code=fs.readFileSync(0,"utf8"); process.stdout.write(vm.runInNewContext(code+";JSON.stringify(examples)"));'],input=prefix,text=True))
    graphs=[]
    for i,g in enumerate(starter):graphs.append((f'00{i+1}_starter',g))
    graphs.extend((p.stem,json.loads(p.read_text())) for p in sorted((ROOT/'examples').glob('*.json')))
    plans=[]
    for slug,g in graphs:
        run=execute(g)
        if not run['ok']:raise RuntimeError((slug,run))
        # Every visible node output is checked after the actual UI-built run.
        expected={key:value for key,value in run['results'].items() if value is None or not any('function'==k for k in value)}
        plans.append({'slug':slug,'name':g['name'],'graph':g,'expected':expected,'steps':make_steps(g)})
    path=ROOT/'web/recording-plans.json';path.write_text(json.dumps(plans,ensure_ascii=False,indent=2))
    (ROOT/'videos/plans.json').write_text(path.read_text())
    return plans


async def generate_audio(plans):
    semaphore=asyncio.Semaphore(3)
    async def one(plan,i,step):
        path=ROOT/'videos/audio'/plan['slug']/f'{i:02}.mp3';path.parent.mkdir(parents=True,exist_ok=True)
        text_path=path.with_suffix('.txt')
        if path.exists() and path.stat().st_size>1000 and text_path.exists() and text_path.read_text()==step['text']:
            return
        async with semaphore:
            for attempt in range(4):
                try:
                    await edge_tts.Communicate(step['text'],voice='zh-CN-XiaoxiaoNeural',rate='-5%').save(str(path))
                    text_path.write_text(step['text'])
                    print('AUDIO',plan['slug'],i,flush=True)
                    return
                except Exception:
                    if attempt==3:raise
                    await asyncio.sleep(2*(attempt+1))
    await asyncio.gather(*(one(plan,i,step) for plan in plans for i,step in enumerate(plan['steps'])))


if __name__=='__main__':
    plans=prepare()
    print('PLANS',len(plans),'STEPS',sum(len(p['steps']) for p in plans),flush=True)
    asyncio.run(generate_audio(plans))
