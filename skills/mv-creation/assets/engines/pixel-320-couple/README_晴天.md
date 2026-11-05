# 《晴天》管弦乐版 像素 MV 工程（全片 0–119.2 s）

- 画布 320×180，最近邻 ×8 输出 2560×1440 / 24fps；成片时间 = 音频时间（音频 119.2 s，纯器乐，117.4 起淡出）
- 拍网格：约 139.7 BPM（体感 70），一小节 3.43 s，每 4 小节一记镲：17.41 / 31.2 / 45.0 / 58.7 / 72.4 / 86.2 / 100.0 / 113.8；逐拍时间在 `audio/beats.json`
- 歌词不做卡拉 OK，写成画面里的字：现在 = 黑板 / 黑板报（粉笔，闪电照亮），回忆 = 纸条、素描本、地上的粉笔字、起雾的窗；逐字随演唱写出
- 逐句时间 `audio/lyrics.json`（用户确认：32 s = 示例歌词内容，86 s = 示例歌词；其余按扒谱的旋律起点对齐），段落对照 `audio/lyrics_map.json`，SRT 在 `晴天_歌词.srt`
- 引擎沿用《半岛铁盒》工程：`px.py chars.py scenes.py ui.py ui_tiny.py props.py`（像素校园男女主、雨、伞）
- 新增：`scenes_qt.py`（电视 / 天气预报屏、停电教室、暴风雨校园、屋檐 + 班级黑板报、校门 + 公告黑板报），`scenes_full.py`（教室前方黑板、纸条特写、雾玻璃窗、谱架、手、彩虹）、`lyr.py`（粉笔 / 铅笔 / 手指写字）、`shots_open.py`（O1–O5 + S01）、`shots_full.py`（S02–S31）、`story.py`（36 镜分镜数据 + 实测事件 EV）
- 渲染：把音频放到 `audio/song.wav`（44.1 kHz 立体声），`python3 code/make_full.py out.mp4 2`（10 秒分段、可续渲）；单帧预览 `python3 code/stills.py out.png t1 t2 ...`
- 3:4 封面：`python3 code/tools/cover.py 成品.png 预览.png`（240×320 网格 ×6 = 1440×1920）
- 字体：Unifont 15.0.01（npm `@fontpkg/unifont`）与 Fusion Pixel 12px（npm `@vp-tw/cjk-web-fonts-fusion-pixel-font`，woff2 转 ttf + cmap.json），路径在 `px.py`
