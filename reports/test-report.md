# FlowPy 验证报告

- Python：3.12.13
- 生成时间（UTC）：2026-09-20T08:23:28.715908+00:00
- 测试：132 项；通过：132 项；失败：0；错误：0；跳过：0
- 参数化子测试：504 组（包含 315 组正则组合和 50 个随机种子）
- 保存的课程流程：22 个，覆盖 Week 2–11
- 每个课程流程验证：子进程执行、预期输出、图与 Python 往返、导出源码一致、独立目录运行
- 总用时：6.731 秒

## 验证范围

| 方向 | 已验证内容 |
|---|---|
| Python 基础 | 类型、运算、BMI 边界、标准输入与输出 |
| 调试 | 语法/逻辑/运行时错误、异常捕获、日志、断言、超时 |
| 控制流 | If 双分支、Switch 独立出口、Map/Filter 子图、break/continue、无环约束 |
| 数据结构 | 列表、元组、字典、集合、成绩管理、查找一致性 |
| 标准模块 | math/random/string/re、贷款计算、号码抽样、邮箱与手机提取 |
| 函数 | def/async def/lambda、默认值、位置/关键字限定、*args/**kwargs、装饰器、闭包、递归、绑定方法、高阶函数 |
| 模块化 | 模块命名空间、模块导入、函数提取、子图与嵌套子图 |
| 文件 | UTF-8 CSV/JSON 真实读写、问卷校验、去重与保存 |
| pandas | DataFrame、dropna、astype、loc、sort_values、to_dict、空结果与非法值 |
| Web API | 导入、导出、运行、示例、非法请求、同源与 Host 检查 |

## 根据测试修复的问题

1. 非法图结构现在返回可理解的 GraphError，而不是泄漏 AttributeError。
2. gate 动态值必须为 bool，避免错误数据静默跳过业务节点。
3. 输出展示支持循环引用、非字符串字典键、集合和 NaN/Infinity，保持合法 JSON；节点之间仍传递原始 Python 对象。
4. 支持返回自定义 awaitable 的函数，修正 asyncio.run 只接受 coroutine 的限制。
5. 导出前使用 compile 校验，提前发现循环外 break/continue 和同步函数内 await。
6. Python 导入统一 CRLF/LF 换行，Windows 保存不会损失无损还原能力。
7. 自定义 Module 注册到当前进程的 sys.modules，使下游原生 import 正常工作。
8. 仅选中节点不再清空运行结果；拖动才修改工作流。

## 当前边界

任意 Python 源码导入为完整 Python 节点；本应用未修改的导出源码可以无损恢复节点与布局。当前调试提供节点结果、终端日志、异常与断言，不提供 Python 源码行级断点调试。input() 在浏览器中使用预先填写的逐行测试输入；导出的 Python 支持终端交互。Python 运行使用本机权限，不是安全沙箱。
