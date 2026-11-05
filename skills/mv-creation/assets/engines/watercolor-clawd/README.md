# 水彩 Clawd 引擎（Skia）

p5 模板（painted-animation）的 Skia 移植：逻辑画布 1920×1080，输出尺寸由环境变量 `MV_OUT` 决定（默认 2560x1440，4K 上传版 3840x2160；纸纹颗粒按 2K 生成再放大，颗粒大小不变）。需要 `pip install --break-system-packages skia-python numpy pillow`。

## 文件与版本

- `eng.py`：画布、`paint`/`inkLine`（水彩填色 + 沸腾墨线）、glow、iris、纸纹颗粒、文字。墨线端帽用单独的 `drawCircle`（旧版把端帽加进同一路径，短墨线会镂空成“烟头”）。`BOIL = 12` 适合快歌，抒情歌改 8（《后来》《最甜情歌》用 8）。
- `clawd.py`：`clawd()`、`feel`/`emotions`、`move`/`turn`、帽子、`him()`/`her()`。取《失眠》版：`emotions()` 过渡时保留角色自定义的 col/dk/lt（旧版会闪回原色）。
- `props.py`：放射光、云、气泡、印章字、秤、跷跷板、伞、秒表、横幅、舞台、山坡等。取《会不会》版：大字弹出提前约 1 帧，落拍那一帧已经可见。
- `sets.py` / `sets2.py` / `hl.py` / `hanzi.py`：《后来》系列场景与戏服——正面书桌房间（她的、他的互为镜像）、丰富日记桌面、长椅 `parkBench` + `seat()`、世界坐标喷壶、山顶大树、商店街、校园、按真实笔顺写字 `inkWrite`（`code/strokes.json`，换歌用 `scripts/build_strokes.py` 重建）。
- 道具库，按歌选用。彼此有同名函数，不要同时 `from x import *`：
  - `props_bingbian.py`：《病变》《会不会》用。闹钟、相框、床、小熊、衣柜、窗帘、信封、番茄、大问号、闪电、病变墨渍、雨。
  - `props_chuanshao.py`：《串烧》用。苹果、火苗、手机通知卡、体温计、聚光灯、水晶球、软木板拍立得、深海、望远镜遮罩、苹果树。
  - `props_zuitian.py`：《最甜情歌》用。手机播放卡、测谎仪、公交站大钟、娃娃机、线索墙、指认室、冲浪板、丘比特箭、过山车、花车、红本子。
  - `sets_huibuhui.py`：《会不会》用。银杏、雏菊摘花瓣、玻璃瓶、信号灯、秋天窗景、银杏大道、雨夜路口、VHS 倒带。
  - `sm.py`：《失眠》用。毛线团、乱团 tangle、针织片、围巾、七段数码闹钟、卧室、礼物盒、纸板立牌、头顶小乌云、逐扇熄灯的公寓立面、烟圈、烟聚成的他。
- `ayu.py` / `items.py`：《新地球》的人类 Q 版角色阿屿（2.3 头身；正/侧/背，走/跑/坐，含酒窝表情；帽子、漂流瓶），可作为人类角色的起点。
- `fonts/ZCOOLKuaiLe-Regular.ttf`（OFL）随包。`hl.wtext` 用的 LXGW 文楷要另取：`python3 scripts/get_fonts.py fonts --wenkai`；缺了不报错，只是那部分字不显示。

## 起点工程：《失眠》（29.66 秒，16 镜，DJ 版节拍卡点）

- `data/beats.json`：实测拍表。`data/lyrics.json`：`[开始, 结束, 文本, 逐字时间]`。
- `code/storyboard.py`：分镜唯一数据源，镜头按拍号 k 写，生成 `data/storyboard.json`。
- `code/common.py`：拍号工具（`B[k]`、`kt`、`pk`、`after`、`bump` 每拍轻推，`isDown` 定小节相位）。
- `code/story.py`：镜头函数。
- `code/render.py`：`Renderer().frame(t)` 返回 BGRA，按帧末采样；转场 cut/pop/wipe/iris/flash；卡拉 OK 提前 2 帧。
- `code/cover.py`：3:4 封面。`code/sheet.py`：联系表。`code/preview.py`：快速预览。`code/beatstrip.py`：逐拍三帧核对。

## 换一首歌

1. 复制本目录为 `<歌名>_MV工程/`，把剪好的音频放到 `assets/song_clip.wav`（音频不入包）。
2. 准备数据：
   - `scripts/beat_track.py` → `data/beats.json`
   - `scripts/align_lyrics.py` → `data/lyrics.json`
   - 需要手写字时：`scripts/build_strokes.py data/lyrics.json --out code/strokes.json --merge`
3. 改写内容：
   - 重写 `storyboard.py`（镜头、拍号、断鼓段）、`story.py`，以及本歌的道具模块（照 `sm.py` 的写法）。
   - `common.py` 里 `isDown` 的相位改成本歌的 `downbeat_phase`。
4. 审片：
   - 联系表：`MV_OUT=960x540 python3 code/sheet.py out/check/s.png 2 9 17`
   - 快速预览：`python3 code/preview.py 1280x720 0 240 out/prev.mp4`
5. 出片：
   - 4K 母版：`MV_OUT=3840x2160 python3 <技能>/scripts/mvrun.py . --profile master --shots <镜头起点.json> --audio assets/song_clip.wav --out out/<歌名>_4K.mp4`
   - 2K 存档：用 `master.py down` 从 4K 缩出。
6. 封面：`python3 code/cover.py`。
