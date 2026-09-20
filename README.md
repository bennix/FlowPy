# FlowPy · 通用 Python 节点工作台

本地 Python 可视化编辑、执行和测试环境。数据流负责变换，控制流负责路由，复杂逻辑保留在 Python 节点里。前端使用原生 HTML/CSS/JavaScript，后端使用 Python 标准库；只有基础 pandas 示例需要可选的 pandas。

## 启动

当前工作目录已经配置 `.venv` 和 pandas：

```sh
./start.sh
```

浏览器打开 http://127.0.0.1:8765 。自定义端口使用 `./start.sh --port 8766`。

新环境配置：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python server.py
```

核心环境兼容 Python 3.9+。当前完整测试使用 Python 3.12.13；不使用 pandas 时无需安装任何包。

## 编辑与运行

- 点击节点库添加节点；拖动节点标题移动；拖动画布背景平移，滚轮缩放。
- 点击输出端口，再点击输入端口建立连接。输入只能有一个来源，新连接替换原连接。禁止循环依赖，按拓扑顺序执行。
- 选中连线或节点后按 Delete 删除。支持撤销、重做、自动排列、缩放和适应画布。
- 右侧编辑参数。已连线的输入优先于默认参数。Constant 使用 JSON，可输入字符串、数值、布尔值、列表或字典。
- `⌘/Ctrl + Enter` 运行；`⌘/Ctrl + Z` 撤销；`⌘/Ctrl + Shift + Z` 重做；`⌘/Ctrl + S` 下载图 JSON。
- 运行结果显示节点输出、分支跳过状态、错误节点和耗时；“终端日志”显示 print 与 stderr。
- “输入”按钮为 `input()` 提供逐行测试数据，输入不足会报告 EOFError。
- Assert 节点比较实际输出和预期值，失败时给出明确错误。
- 图自动保存到浏览器本机存储；导出 JSON 或 Python 可以永久保存、迁移或分享。

## 节点与语义

| 层 | 节点 | 用法 |
|---|---|---|
| 输入 | Constant、LoadText、Item | 常量、文本、子图当前项 |
| Python | Python、Function、Lambda、Call | 逻辑块、函数定义、匿名函数、调用 |
| 模块 | ImportModule、Module、Get | 导入标准模块或 pandas、自定义模块、提取属性与函数 |
| 控制 | If、Switch、Map、Filter、Loop | 布尔路由、多出口选择、列表映射、过滤、显式循环 |
| 正则 | RegexMatch、RegexFindall、RegexSub、RegexSplit、RegexSwitch | 纯字符串变换与规则分类 |
| 输出与测试 | Output、Assert | 显示结果、预期值断言 |

**gate** 是可选布尔控制输入，只有 True 执行；False 会跳过节点，跳过会向下游传播。没有 gate 的节点正常执行。普通 `value=None` 不是“跳过”。独立分支按照依赖顺序执行，没有隐藏的共享循环游标。

**Switch** 从 cases 顺序选择第一个相等值，产生 `case_0`、`case_1` 等独立布尔端口，以及 `default`。RegexSwitch 只产生分类数据，路由交给 Switch。

**Python 节点**可以使用 `inputs`、`value`、`items`、`text`、`index`、`acc` 和 `re`，将输出写入 `result`。可直接 import 标准库或当前解释器已安装的 pandas。模块、函数、生成器和 DataFrame 在节点之间按原始 Python 对象传递，不会先序列化为 JSON；只有结果面板会生成展示快照。

**Function** 保留原生 def / async def 语法，支持默认参数、位置限定 `/`、关键字限定 `*`、`*args`、`**kwargs`、闭包、递归、装饰器。输出函数名称对应节点里的可调用对象。

**Call** 执行 `function(*args, **kwargs)`。如果连接 value，会把它放到 args 之前。异步返回值会等待完成。Python 节点也可输出绑定方法、partial 或带 `__call__` 的对象。Lambda 可接入 Call、Map、Filter 和 RegexSub 的 repl。

**Map / Filter / Loop** 可进入可视化子画布：Item 提供当前 value、index、acc，唯一 Output 返回单项结果。Filter 子图必须返回 bool。执行优先级为已连接函数回调 → 子图 → 节点内 Python 逻辑。循环上限默认 1000，最多 100000；Loop 的 Python 逻辑支持 break / continue。子图编辑可返回上层，支持嵌套，最多 8 层。

## Python 与图互转

“Python 代码”显示可读源码，导出后可独立执行，不依赖 FlowPy：

```sh
.venv/bin/python examples/w09_salary_functions.py
```

导出源码包含图元数据与源码摘要，未修改的导出文件重新导入可还原节点、连线、参数和布局，包括嵌套子图。支持 Windows CRLF 换行。

任意 Python 文件，或正文已经修改的导出文件，会完整保留为一个 Python 逻辑节点，不猜测拆分。导入代码使用共享模块命名空间，内部函数可以访问 import 与全局变量。需要图输出时赋值给 `result`；print 输出进入日志。当前不提供任意 Python AST 与细粒度节点之间的自动双向重构。

## 已验证课程范例

界面“示例”收录 22 个 Week 2–11 课程流程，另有 4 个入门流程。课程流程在 `examples/` 中保存为成对的 `.json` 与 `.py` 文件：

| 周次 | 范例 |
|---|---|
| W2 | BMI、input() 交互 BMI、基础类型与运算符 |
| W3 | 三次 AI 代码失败、原因与修正验证日志 |
| W4 | 异常捕获、批量调试、打印日志 |
| W5 | 分难度猜数字、continue / break |
| W6 | 列表与元组版成绩管理 |
| W7 | 字典与集合版成绩管理、列表/字典查找对比 |
| W8 | 双色球、邮箱手机提取、月供计算、math 导入、string |
| W9 | 薪资计算完整参数签名、Lambda 与 map/filter |
| W10 | 成绩管理模块化、可视化嵌套子图 |
| W11 | CSV/JSON 文件往返、问卷校验与保存、基础 pandas |

问卷范例会写入项目 `artifacts/survey.csv` 与 `artifacts/survey.json`。CSV/JSON 往返测试使用临时目录。双色球与猜数字使用固定随机种子，便于复现。

## 验证

```sh
.venv/bin/python scripts/verify.py
```

完整运行测试，生成 `reports/test-report.md` 和 `reports/test-results.json`。课程示例逐个验证真实 Python 执行、预期输出、代码往返、源码一致性以及独立目录运行。

重新构建示例：

```sh
.venv/bin/python scripts/build_examples.py
```

脚本只有在执行成功且输出符合预期时才保存对应流程。

## 执行边界

服务只监听 127.0.0.1，执行接口检查同源与 Host。每次运行使用独立 Python 子进程，超过 10 秒终止；输出有大小限制。Python 节点使用本机用户权限，**不是安全沙箱，只应运行可信代码**。当前支持节点结果、日志、异常和断言调试；不提供 Python 源码行级断点调试。浏览器交互输入使用预先填写的测试数据，导出的 Python 支持真实终端交互。

## 从空画布开始的中文演示

`videos/index.html` 汇总 26 个独立 MP4，每个例子从零节点、零连线开始，通过界面逐步添加、编辑、连接并运行。使用 Microsoft Edge TTS 中文配音；每段解说完毕后才开始下一步操作。详细制作与验证说明见 `videos/README.md`。

## 项目主页与教程

在线主页：https://bennix.github.io/FlowPy/

仓库根目录的 `index.html`、`landing.css`、`landing.js` 构成静态 Landing Page，包含全部 26 个可筛选、可播放的教程。视频文件直接随仓库保存，不依赖外部视频平台。GitHub Actions 自动发布到 GitHub Pages，并运行 Python 测试。

本地预览主页（与编辑器端口独立）：

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

然后打开 http://127.0.0.1:8766 。主页仅展示介绍与教程；编辑器使用 `./start.sh` 启动。

源代码、课程流程、测试、成品视频、配音、字幕与制作脚本均保存在仓库。原始屏幕录制、重复的中间视频切片、本机编译工具及虚拟环境不纳入 Git；重新录制需 macOS 与对应界面自动化工具。
