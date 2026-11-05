# 320 像素引擎 · 像素校园男女主（《晴天》《半岛铁盒》）

周杰伦的歌默认用这对主角。引擎来自《半岛铁盒》，《晴天》沿用后又补了几处。本目录以《晴天》的完整工程为主体，另附《半岛铁盒》的 B 式开头作为范例。

- 画布 320×180，最近邻 ×8 输出 2560×1440 / 24fps。
- `render.frame(t)` 返回 uint8 RGB，已经是 2560×1440。
- 出片：`python3 code/make_full.py out.mp4 2`，10 秒分段、可续渲，编码已改为 BT.709 + High@5.1。
- 字体：`python3 <技能>/scripts/get_fonts.py fonts --unifont --fp12`。也可以用环境变量 `MV_FONT_DIR` 指向已有的字体目录。

## 引擎模块（`code/`）

- `px.py`：网格、平涂、描边、像素文字。Unifont 16px 做正文，Fusion Pixel 12px 做小标签。
- `chars.py`：校园男女主，side/front/back 三个视角，姿势 stand/walk/sit/floor，近景半身，`bag=True` 书包，“？”表情。设定见技能 `references/cast.md`。
- 场景与界面：
  - `scenes.py`：背景、雨、伞、灰尘
  - `props.py`：书、铁盒、糖果罐、拍立得
  - `ui.py` / `ui_tiny.py`：聊天、语音转文字、锁屏、标题、卡拉 OK
- 《晴天》新增：
  - `scenes_qt.py`：电视天气预报屏、停电教室、暴风雨校园、黑板报
  - `scenes_full.py`：黑板、纸条、雾玻璃、谱架
  - `lyr.py`：纯器乐版的画内歌词，粉笔、铅笔、手指写字
  - 镜头：`shots_open.py`（O1–O5 + S01，A1 变体开场）、`shots_full.py`、`story.py`（36 镜分镜数据 + 实测事件）
- `tools/`：
  - `cover.py`：240×320 网格 ×6 = 1440×1920 封面
  - `contact.py` / `frames.py` / `sheet.py`：审片
  - `verify.py`：解码后与 `frame(t)` 比对

## 数据与范例

- `audio/beats.json`、`audio/lyrics.json`、`audio/lyrics_map.json`：《晴天》的时间数据。音频不在包内，放到 `audio/song.wav`。
- `examples/bandao/`：《半岛铁盒》的分镜与镜头，含 B 式开头——书店对白做成语音条 +“转文字”、全停时熄屏 → 锁屏。用法：在工程副本里把这些 `.py` 覆盖到 `code/`，再把 `examples/bandao/audio/*.json` 覆盖到 `audio/`（已实测可渲出）。

## 换歌

1. 只重写 `story.py` 和镜头文件，时间数据放进 `audio/`。
2. 识别特征不变；故事、场景、季节服装每首重新设计。
