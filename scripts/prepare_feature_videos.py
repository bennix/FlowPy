"""Create the three feature-video plans and their Microsoft Edge TTS narration."""
import asyncio
import json
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / "videos"


def node(node_id, kind, x, y, title, config):
    return {"id": node_id, "type": kind, "x": x, "y": y, "title": title, "config": config}


BASE_GRAPH = {
    "name": "运行路径示例",
    "description": "常量 → Python 逻辑 → 输出",
    "nodes": [
        node("score", "Constant", 60, 160, "成绩数据", {"value": {"score": 88}}),
        node("grade", "Python", 410, 160, "计算等级", {"code": 'score = value["score"]\nresult = {"passed": score >= 60, "grade": "A" if score >= 85 else "B"}'}),
        node("output", "Output", 780, 160, "输出结果", {"value": ""}),
    ],
    "edges": [
        {"source": "score", "out": "value", "target": "grade", "in": "value"},
        {"source": "grade", "out": "value", "target": "output", "in": "value"},
    ],
}

plans = [
    {
        "slug": "feature_execution_trace", "name": "运行路径：节点与连线高亮", "group": "features",
        "graph": BASE_GRAPH,
        "expected": {"score": {"value": {"score": 88}}, "grade": {"value": {"passed": True, "grade": "A"}}, "output": {"value": {"passed": True, "grade": "A"}}},
        "steps": [
            {"action": "start", "text": "这一节演示运行路径高亮。画布现在完全为空，没有节点，也没有连线。我们从零搭建一个成绩判断流程。"},
            {"action": "node", "node": BASE_GRAPH["nodes"][0], "text": "先添加 Constant 节点，输入包含成绩八十八分的结构化数据。"},
            {"action": "node", "node": BASE_GRAPH["nodes"][1], "text": "添加 Python 节点，把及格判断和等级规则收在一处，避免把复杂逻辑拆成碎节点。"},
            {"action": "edge", "edge": BASE_GRAPH["edges"][0], "text": "连接成绩数据到 Python 节点的 value 输入端口。数据流只负责传递数据。"},
            {"action": "node", "node": BASE_GRAPH["nodes"][2], "text": "添加 Output 节点，用于展示工作流的最终结果。"},
            {"action": "edge", "edge": BASE_GRAPH["edges"][1], "text": "连接计算等级的输出到结果节点，完整数据路径已经清晰可见。"},
            {"action": "run", "text": "运行工作流。界面会根据真实执行轨迹依次高亮节点和经过的连线。"},
            {"action": "result", "text": "结果显示 passed 为 true，grade 为 A。高亮回放让当前执行到了哪里一目了然。"},
        ],
    },
    {
        "slug": "feature_edge_preview", "name": "局部调试：连线中间数据预览", "group": "features",
        "graph": BASE_GRAPH,
        "expected": {"score": {"value": {"score": 88}}, "grade": {"value": {"passed": True, "grade": "A"}}, "output": {"value": {"passed": True, "grade": "A"}}},
        "steps": [
            {"action": "start", "text": "这一节演示连线上的中间数据预览。这里是全新的空白画布，我们再次从零开始搭建。"},
            {"action": "node", "node": BASE_GRAPH["nodes"][0], "text": "添加 Constant 节点，并填入成绩数据。"},
            {"action": "node", "node": BASE_GRAPH["nodes"][1], "text": "添加 Python 节点，计算是否及格以及对应等级。"},
            {"action": "edge", "edge": BASE_GRAPH["edges"][0], "text": "先连接原始成绩到处理节点。"},
            {"action": "node", "node": BASE_GRAPH["nodes"][2], "text": "添加 Output 节点。"},
            {"action": "edge", "edge": BASE_GRAPH["edges"][1], "text": "再连接处理结果到输出节点。"},
            {"action": "run", "text": "运行这张图，得到真实的节点输出快照。"},
            {"action": "wire-preview", "text": "点击第一根连线。右侧显示 value 端口实际传递的 JSON 数据，不必猜测中间值。"},
            {"action": "result", "text": "这种局部预览适合逐段定位数据问题，且不会改变工作流本身。"},
        ],
    },
    {
        "slug": "feature_extensions", "name": "扩展生态：第三方库与模块导入", "group": "features",
        "graph": {
            "name": "模块调用示例", "description": "导入 math.sqrt → 调用 → 输出",
            "nodes": [node("math", "ImportModule", 60, 160, "导入 math.sqrt", {"module": "math", "attribute": "sqrt"}), node("call", "Call", 410, 160, "计算平方根", {"args": [81], "kwargs": {}}), node("output", "Output", 780, 160, "输出结果", {"value": ""})],
            "edges": [{"source": "math", "out": "value", "target": "call", "in": "function"}, {"source": "call", "out": "value", "target": "output", "in": "value"}],
        },
        "expected": {"math": {"value": "<callable>"}, "call": {"value": 9.0}, "output": {"value": 9.0}},
        "steps": [
            {"action": "start", "text": "这一节介绍扩展生态与模块导入。画布仍然从零节点、零连线开始。"},
            {"action": "packages", "text": "先打开扩展库目录。这里列出受控的 pandas、requests、numpy 等包，以及它们当前的安装状态。"},
            {"action": "node", "node": {"id": "math", "type": "ImportModule", "x": 60, "y": 160, "title": "导入 math.sqrt", "config": {"module": "math", "attribute": "sqrt"}}, "text": "添加 ImportModule 节点。先使用标准库 math 的 sqrt 函数，第三方包安装后也可以按相同方式导入。"},
            {"action": "node", "node": {"id": "call", "type": "Call", "x": 410, "y": 160, "title": "计算平方根", "config": {"args": [81], "kwargs": {}}}, "text": "添加 Call 节点，准备以八十一作为参数调用函数。"},
            {"action": "edge", "edge": {"source": "math", "out": "value", "target": "call", "in": "function"}, "text": "连接导入的函数到 Call 的 function 端口。"},
            {"action": "node", "node": {"id": "output", "type": "Output", "x": 780, "y": 160, "title": "输出结果", "config": {"value": ""}}, "text": "添加 Output 节点，用来查看调用结果。"},
            {"action": "edge", "edge": {"source": "call", "out": "value", "target": "output", "in": "value"}, "text": "连接 Call 的 value 输出到结果节点。"},
            {"action": "run", "text": "运行工作流，验证模块函数已经被正确导入和调用。"},
            {"action": "result", "text": "输出九点零。扩展库面板负责受控安装，ImportModule 和 Python 节点负责在图中使用模块能力。"},
        ],
    },
]


async def make_audio():
    for plan in plans:
        folder = VIDEOS / "audio" / plan["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        for index, step in enumerate(plan["steps"]):
            path = folder / f"{index:02}.mp3"
            if not path.exists():
                await edge_tts.Communicate(step["text"], "zh-CN-XiaoxiaoNeural", rate="-5%").save(str(path))


if __name__ == "__main__":
    (VIDEOS / "feature-plans.json").write_text(json.dumps(plans, ensure_ascii=False, indent=2))
    asyncio.run(make_audio())
    print("Prepared", len(plans), "feature plans")
