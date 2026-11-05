# 高清像素引擎 640×360（《下雨了》）

旧版 320×180 发抖音后画质差，这套是按抖音转码重做的，用户认可画质。用户说“用《下雨了》的引擎 / 高清像素引擎”时用它。原工程说明见 `README_下雨了.md`。

- **画布与放大**：640×360 逻辑画布，最近邻放大。×4 = 2K 母版，×6 = 4K 抖音上传版，×3 = 1080p。
- **字体**：先运行 `python3 <技能>/scripts/get_fonts.py assets --unifont`，生成 `assets/unifont.ttf`。
- **帧接口**：`render.frame(t)` 返回 640×360 的 **float RGB**，不是 mvrun 要求的 BGRA。所以出片用本工程自带的 `code/final.py`，一遍渲染同时编 2K 和 4K 两路；编码参数已改为 BT.709、锁 High@5.1、ref=4。
  - 148 秒的片子约 10 分钟。
  - 4K 要用文件卡片发送时，画面 crf 17、音轨 128k 才压得进 30MB。
- **抖音画质规则**：
  - 不用整帧抖动、颗粒、逐帧随机噪点；大面积平涂，暗部不压近黑。
  - 粒子按 12fps 步进，至少 2 个逻辑像素，位置只由 t 决定。
  - 光晕用 4–6 阶平涂同心环，放大镜头里强度随缩放递减（否则像靶心）。
  - 镜头只做整数像素平移，推拉靠按新缩放重新光栅。
- **模块**：
  - 场景：`street.py`（整条街，night/moon/memory 三种光，`ow/oh` 出竖版）、`skyline.py`、`scn_window.py`、`scn_her.py`。
  - 特效：`fx.py`（雨、水花、涟漪、倒影、`Glass`/`Drop`）。
  - 角色：`sprite.py`（SB 部件）、`chars.py`（HIM/HER）、`bust.py`（近景）。
  - 其他：`cloud.py`、`writing.py`（按笔顺在雾上写字）。
  - 镜头：`shot_intro.py` / `shots_*.py`。
- **工具**：
  - `csheet.py out.png t1 t2 …`：按时间出单镜联系表。
  - `fullsheet.py 0 148 2.45 out.png`：全片联系表。
  - `sweep.py`：出片前跑，扫描报错。
  - `verify.py`：出片后解码，与 `frame(t)` 比对。
- **坑**：
  - 写字的手要拇指外露、食指在手掌边缘，否则像竖中指。
  - 远处窗灯要画进底图，最后再叠会盖住前景楼。
  - 镜头 x 出界会裁出 0 宽（已夹紧）。
- **范例《白兰花》**（`examples/bailanhua/`，98 秒，29 镜；引擎 core/sprite/fx 与本目录完全一致）：
  - `chibi.py`：小酒窝男女主 640 版。`him()`、`her(style='memory'|'cut'|'now')`；光照 `LIGHT`（night/lamp/warm/dusk/neon/corner/cold…）乘色，加单侧轮廓光；`over=` 换色做路人。
  - `sh_street.py`：午夜上海街（石库门弄堂口、理发店、咖啡馆、舞厅、午夜场影院、海报墙、公交站、南货店）。影院招牌用 `marquee_overlay`（左右对称的灯泡追光、翻牌 `flip_char`、翻回空白、熄灯扫），霓虹用 `neon_overlay`。
  - `scn_lane.py`：弄堂立面。`scn_rooms.py`：咖啡馆、理发店镜子、舞厅、餐桌、卧室。
  - `shots_intro.py`：S01–S05，影院翻牌招牌开场 → 下摇到街面 → 电影票近景 → 午夜招牌熄灭。
  - 用法：在工程副本里把这些 `.py` 覆盖到 `code/`，把 `examples/bailanhua/assets/*.json` 覆盖到 `assets/`（已实测可渲出）。音频：`ffmpeg -i 白兰花.flac -t 98.0 -af "afade=t=out:st=96.0:d=2.0" -c:a pcm_s16le assets/audio_cut.wav`。
- **换歌**：只重写 `story.py`、镜头文件和 `assets/timing.json`。timing.json 的键：`beats`、`downbeats`、`lyrics`、`intro_onsets`、`gap`、`end`。本片人物换歌时另定，用户说沿用才沿用。
