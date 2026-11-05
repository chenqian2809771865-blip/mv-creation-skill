# 《半岛铁盒》像素 MV 工程（原曲 0:00–2:18.6，做到第一段副歌结束）

- 画布 320×180，最近邻 ×8 输出 2560×1440 / 24fps；成片时间 = 原曲时间（原曲开头无静音）
- 拍网格：64.6 BPM（八分音符 0.4644 s），小节首拍 bar(k) = 48.735 + 3.7152k；鼓组 47.34 进入，副歌首拍 74.742
- 前奏 8.87–15.1 是书店对白的占位示例（已替换原曲文字），画面里做成他发给她的 0:06 语音 +“转文字”；15.25–16.85 全停 = 熄屏 → 锁屏
- `code/story.py`：分镜数据（镜号、时间、歌词、画面、转场、实现函数），storyboard.csv/md 由它生成
- `code/chars.py`：像素校园男女主（沿用《枫》工程，新增书包 `bag=True` 和“？”表情）
- `code/scenes.py` 背景/雨/伞/灰尘，`code/props.py` 书、铁盒（生锈/积灰）、糖果罐、拍立得，`code/ui.py` 聊天/语音转文字/锁屏/标题/卡拉OK
- `code/shots_intro.py` / `shots_verse.py` / `shots_chorus.py`：各镜头；`code/render.py`：frame(t)，画面整体比音频提前 2 帧
- 字体：Unifont 15.0.01（npm `@fontpkg/unifont`）与 Fusion Pixel 12px（npm `@vp-tw/cjk-web-fonts-fusion-pixel-font`，woff2 转 ttf），路径在 `px.py`
- 渲染：把原曲放到 `audio/song.flac`，运行 `python3 code/make_video.py 2`（按 10 秒分段，可续渲）
- 3:4 标题关键帧：`python3 code/tools/cover.py 成品.png 预览.png`（240×320 网格 ×6 = 1440×1920）
- 审片：`python3 code/tools/contact.py T0 T1 STEP out.png [列数]`，单帧：`python3 code/tools/frames.py out.png t1 t2 ...`
- `audio/lyrics_chars.json`：按分离人声（UVR Voc_FT）+ SenseVoice 校准的逐字时间；`半岛铁盒_歌词.srt` 同一时间轴
