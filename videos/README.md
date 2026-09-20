# 从空画布开始的演示视频

打开 `index.html` 查看全部 26 个独立 MP4。每个例子均从零节点、零连线开始，通过真实界面添加节点、编辑参数、连接端口并运行验证。嵌套子图也从空白开始。

配音使用 Microsoft Edge TTS `zh-CN-XiaoxiaoNeural`。视频剪辑按实际音频长度停留，每段解说结束至少 0.4 秒后再开始下一步操作。视频为 1920×1080 H.264/AAC，附中文字幕 SRT。

`manifest.json` 是视频目录，逐片 `.timeline.json` 保存音画时间与运行验证记录。`raw/` 是独立 FlowPy 窗口的原始录制与操作时间戳，`audio/` 是 Edge TTS 配音。

录制使用 macOS ScreenCaptureKit，界面操作通过 CUA 完成；参考计划仅用于逐项填写，不向编辑器注入完成图。函数对象的内存地址每次运行不同，模块化例子核对真实调用的结构化结果。

制作脚本位于 `scripts/prepare_videos.py`、`record_window.swift`、`render_demo.py`。依赖见 `requirements-videos.txt`，另外需要 ffmpeg/ffprobe 和 Swift 编译器。已有录制可用 `.venv/bin/python scripts/render_demo.py <slug>` 重合成；使用 `.venv/bin/python scripts/verify_videos.py` 验证全部媒体并重建目录。
