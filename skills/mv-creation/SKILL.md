---
name: "mv-creation"
description: "根据歌曲制作或修改动画 MV、歌词视频和动画短片：像素风、Clawd 水彩手绘、像素校园男女主等；拆解单款或多款参考片、故事分镜、节拍卡点、歌词逐字对齐（纯器乐版把歌词写成画面里的字），导出 2K 抖音上传母版（横屏 16:9 或竖屏 2:3）、SRT/VTT，附 3:4 和 4:3 标题关键帧与发布简介。仅制作字幕或只出故事分镜时也适用。抖音竖屏科普、知识短片用对应的专门技能。"
---

# 动画 MV 与歌词字幕

> 仅适用于 Claude 桌面版 / 云端会话；其他环境直接写本地文件。以下涉及 device_*、get_device_info、SendUserFile、stagedPath、xfer.sh 的传输与设备说明仅在该环境生效。


按用户的歌曲、角色和画风完成作品。优先级：用户当次的话 > 本文件 > `references/notes/` > references 和引擎文件。引擎、角色、方法复用，故事和镜头每首重新设计。

**细则分层**：01–08 细则已随仓库收录在 `references/notes/`，直接读取，不需要设备拷贝。别处提到的「3.1 / 4.3 / 4.6 节」分别见 02 / 03 / 05。文档中的 `references/`、`assets/`、`scripts/` 均以本技能目录为基准；`<工程目录>` 中的数据和输出由运行时准备，不属于随附文件。读取失败时说明缺失项，不凭记忆补。

**本地工作目录**：以下命令从工程目录运行。先将技能 `scripts/` 复制到工程的 `scripts/`（同时复制技能根 `config.json` 与所需引擎的 `<工程目录>/code/`、占位 `<工程目录>/data/` 或 `assets/`、`<工程目录>/fonts/`），再运行相对路径命令。输出目录由用户指定，默认 `./MV作品/<歌名>_MV/`。片头署名读取技能根 `config.json` 的 `SIGNATURE`；值为空或仍为「★你的署名」时先询问用户，可用环境变量 `MV_SIGNATURE` 覆盖。移植签名模块时一并复制同目录的配置助手（源文件 `scripts/mv_config.py`）。

## 按需读取

| 情况 | 读 |
|---|---|
| 慢歌（一小节 > 2.4 秒），分镜前 | `references/notes/02_慢歌剧情.md`（必读） |
| 写或改水彩镜头代码前 | `references/notes/03_写镜头代码.md`（必读） |
| 竖屏 2:3，开工前 | `references/notes/05_竖屏2x3.md`（必读） |
| 拍表 / 歌词对齐异常（二次剪辑、变速拼接、现场录音、倍速、双层人声、附唱、识别率低、补字） | `references/notes/01_拍点与歌词.md` |
| 开头片名、署名 | `references/notes/04_片名署名实现.md` |
| 子任务审片、旧作只改开头、写回桌面、暂停 | `references/notes/06_审片出片交付细节.md` |
| 可复用的道具、布景、戏服、角色模块 | `references/notes/07_道具与戏服.md` |
| references 或引擎说明与本文件冲突 | `references/notes/08_作废更正.md` |
| 固定角色（像素校园男女主、Clawd 男女主、小酒窝、人类 Q 版） | references/cast.md（校园男女主水彩版见 07） |
| 前奏开场（画内标题器物、聊天 / 界面序幕） | references/openings.md |
| 卡点、鼓点、断鼓段 | references/beat-sync.md |
| 歌词对齐、纯器乐版、卡拉 OK | references/music-lyrics.md |
| 选引擎、分段渲染、续渲 | 4.1 节、assets/engines/README.md 与所用引擎 README、references/rendering.md |
| 像素 320 / 640、字体 | references/styles.md |
| Clawd 函数接口 | references/characters.md（表情以 `clawd.EMO` 为准） |
| 有参考片，或成片“碎”“拖”“平” | references/reference-video.md、references/multi-reference.md |
| 交付命令、云端限制、实测速度 | 第 5 节、06、references/delivery.md、references/env-notes.md |
| 学到新做法或坑 | 第 5 节末条 |

## 硬规则（用户明确要求过）

1. **不拍身体局部特写，全身入画要露脚。** 手指、眼睛特写改拍道具（票头、印章、手机界面）、环境、光影或画内文字；歌词写到“眼里”“手里”用半身近景加泪光，或只拍道具。只有坐车斗船舱、躺床盖被才用 `noLegs`；不藏在柜台桌子后面（改站旁边）；坐着、坐地上都给座面（`sets2.seat()`）；挡腿的吊篮换秋千座（`dx.bambooCopter(..., basket='swing')`）。窗户故事需要时可入画、可做装置（对窗、隔窗打灯语），用不上时优先无窗布景；画内文字写在黑板、纸条、招牌上，不用雾玻璃写字。
2. **角色、画风按约定选，用户另指定为准**（references/cast.md）。「默认男女主」「疑心病男女主」= Clawd 男女主（戏服按歌另定，不默认戴侦探帽）；像素校园男女主可选，按歌选角（像素只有 320 版，选 640 按 references/cast.md 重画；水彩用《罗生门》包 `assets/engines/watercolor-modules/罗生门/couple.py`）；「人物复用小酒窝」= 小酒窝男女主。像素 320 还是 640 没说就问；没指定角色按歌选，不自动套 Clawd。
3. **歌词以用户文本为准**，不凭记忆补；时间按实际演唱校准，不沿用 LRC。
4. **视频编码只走 `scripts/master.py` 或 `scripts/mvrun.py`**（固定 BT.709）。水彩直接接 mvrun，像素补适配器（4.1）；引擎自带的 `final*`、`make_*`、`run_*.sh`、`assets/engines/watercolor-clawd/code/preview.py` 不用。剪音频、`-c copy` 不受限。
5. **只出 2K，画幅二选一**：横屏 2560×1440 或竖屏 2:3 1440×2160，不出 4K、9:16、3:4 正片；没说就问（附一句：横屏电脑上看最好；2:3 竖刷满宽、约占屏高 67%，横屏约 25%）。聊天窗口只发 720p 预览（2:3 为 720×1080）；母版写到用户指定的输出目录（默认 `./MV作品/<歌名>_MV/`），写不了（没授权、断线、拼不回分片）就留云端告知、能写时再传，不发进聊天。「母版发我」指指定输出目录中的原件；用户说直接存桌面时连预览也不发。
6. **每次成片附** 3:4（1440×1920）和 4:3（1920×1440）标题关键帧 + 可整段复制的发布简介；封面、标题、话题不写角色叫法，小标签只写画风（「原创水彩手绘 MV」）。
7. **默认一口气做完**：预览自查通过就直接渲 2K、写到用户指定的输出目录、一次交付；只有用户说「先给我看」「等我确认」才停在预览。开工缺的必要信息（音频、区间、角色、画幅、320/640）照常问；取了哪种理解、ASR 不一致处、纯器乐段落推测、旧作改动清单写进消息，接着做不等回复。
8. **开头片名 + 可配置署名（读 `config.json` 的 SIGNATURE；没设置就问用户），只停约一个小节**（快歌约 1.5 秒、慢歌约 3 秒）。无常驻水印；结尾不再出片名和歌手名（回扣器物时写别的字或空白）；关键帧不加水印。实现、实测值和代码见 04。**同屏只有一个片名**：

   | 开场 | 片名 | 署名 |
   |---|---|---|
   | 普通开场 | 屏幕层片名卡，第一拍弹入 | 和片名卡一起 |
   | A1 画内标题器物 | 器物上的字就是片名，不加片名卡 | 器物片名完整那一拍出现、贴在片名旁，器物镜头下摇或切走前淡完 |
   | 第一帧就是手机界面 / 取景框 | 界面旁空位的小标签，第一拍弹入 | 标签下方 |
   | B/C 界面序幕 | references/openings.md 的标题卡（前奏中段强拍；C 式“开关”梗以最后的正式标题为准） | 片名下方，同时出现 |

   - 无前奏时「第一拍」= 第一句人声（落在弱起拍或 B[0] 在片头前时 `K_TITLE` 取 k1）。A1 器物片名完整后至少再停 1.2 秒；片名那一拍不放别的大事件。
   - 署名 50 号（画布高约 4.6%，≥ 38；2:3 见 05），片名明显更大。水彩用 `assets/engines/watercolor-modules/可不可以给我你的微信/opening.py` 的 `signature()`（文楷，缺 `<工程目录>/fonts/LXGWWenKai-Regular.ttf` 会静默空白，用 `python3 scripts/get_fonts.py fonts --wenkai`）；像素 640 Unifont 16、320 Fusion Pixel 12（片名下方单独一行），不透明、1 像素深色描边。
   - 画在屏幕层，可跨开头切镜（A1 除外）；不压脸和界面按钮、不进歌词条、不放右下角（平台 Logo），和第一小节的大字、大梗、顶部旁白错开。跨切镜或甩镜遇脸、界面就提前淡出（至少露 1.2 秒，公式见 04）。
   - 一小节 ≤ 2.4 秒算快歌：快歌落点拍前 0.04 秒弹入（0.22 秒），慢歌拍前 0.1 秒起 0.4 秒淡入。在落点后能露满 1.2 秒的第一条小节线前淡完（快 0.22 秒、慢 0.4 秒，像素在小节线那帧切掉），露出超过 4 秒就提前半小节。不写死「0–2 秒」。
9. **目录与执行**：先把技能资源复制到独立工程目录，源资源只读；命令用相对路径，长任务前台运行并用 `scripts/mvrun.py --status` 查看状态。文件访问与传输遵守当前工具的权限机制。仅适用于 Claude 桌面版 / 云端会话；其他环境直接写本地文件：先用 `get_device_info` 查看连接，只申请用户指定的必要目录；云端可将技能复制到 `<工作目录>/mvskill` 后使用；不申请删除权限，替换旧文件先改名存到输出目录的 `<工程目录>/旧版/`。

## 1. 确定任务

- 只问影响开工的缺项（音频、区间、要字幕时的歌词、画幅、角色、320/640），其余用默认值并说明。默认：原曲完整时长、24fps、2K。
- 用户给结束时间：收在最近的强拍上，音频截到强拍后 0.4–0.5 秒并淡出，故事落点压进最后两小节；mp4 末尾切在下一句开头时，收在前一句尾字的重拍上，说明短了多少。
- 只做字幕、改成片就直接进对应步骤；只讨论方案先讨论；方向不明确就自己定一个直接做，开头说明理解。「节拍网络卡点」= 节拍网格卡点（恒定网格 + 每拍一事件）。
- 只要故事和分镜：先做第 2 步，交付故事概念、情绪走向和分镜表（镜号、时间码、歌词、画面、动作、运镜、转场；Docs + 含生成提示词的 CSV + 校准后的 SRT）；分镜写成数据文件，之后直接做时沿用。
- 只给了带画面的 mp4、没说参考：只当 BGM 抽音轨，画面不参考，开头说明。说「参考」才按参考片处理：标清参考与目标的版本、歌词、区间，黑边和抖音界面不算画幅；只要分析就交拆解与建议。

## 2. 听音乐、对歌词（分镜之前）

- 片段时间 = 原曲时间 − 起点，从第一个非零样本切起；结尾数字静音后又响一截是 DAW 录屏接缝，切在静音处。
- 拍点：`scripts/beat_track.py` 出拍表，找断鼓空档做定格、换场。恒速版拟合恒定网格，会漂的才逐拍插值；小节首拍不在 k % 4 == 0 就整体平移拍号（B[0] 可为负）；慢歌常被测成倍速，体感拍取偶数 k，小节相位按副歌进来那一拍定，不照搬 `downbeat_phase`。异常读 01。
- 歌词：`scripts/align_lyrics.py` 逐字对齐；ASR 与用户文本不一致处列给用户、按实际演唱改，同音误识别保留用户文本；用户歌词里没有的人声不加字幕；识别为空走纯器乐流程（references/music-lyrics.md）。LRC 时间一律重新校准。

## 3. 故事、开场与角色

- 从音乐情绪、段落和歌词意象提炼故事，镜头密度跟歌走。快歌约一小节一镜，每镜换背景、每句一个道具梗，转场混用硬切、弹入、斜擦、圆形遮罩，要求卡点再加每拍一事件。慢歌先写剧情主线（读 02）：钩子问题 + 看得见、能计数的故事装置 + 完整版顶部旁白，一个剧情点约一句歌词，镜头之间有因果，不快切成幻灯片。说唱主歌一句约一小节、镜头切在小节首拍，副歌两小节一镜。拿不准就和参考片对照镜头长度分布。
- 开头在第一个重拍或第一句人声切入正片（references/openings.md），第一帧满画面；无前奏可让第一帧就是画内界面。重复段落镜像，结尾回扣开头。
- **细节密度**：每个场景铺一层生活物件和烟火气（房间的书架、串灯、日历、盆栽；桌面的车票、咖啡渍；街上的店招、亮窗里做饭的人、晾衣、路边摊热气、打伞路人、车灯），开头、中段、结尾用同一套小物呼应。长片后半段不能比开头简陋：复用布景要换机位、光和小剧情。现成工具见 07（《罗生门》`assets/engines/watercolor-modules/罗生门/lsm3.py`）。
- 角色定义集中在一个共享文件，镜头只改姿态、位置、表情；多个 Clawd 只靠配色、服装、配饰区分。已做过的戏服见 07。

## 4. 制作与检查

### 4.1 引擎与权威版本

已收录的工程代码在 `assets/engines/watercolor-modules/`；按来源和功能查`assets/engines/watercolor-modules/README.md`。原工程的音频、歌词、图片、成片和 chunks 不随仓库分发。模块是移植参考，需配合工程自己的拍表、歌词和分镜数据使用。复制引擎成新工程后只重写分镜、镜头和本歌道具（见引擎 README「换歌」）。

- 水彩引擎核心用随附 `assets/engines/watercolor-clawd/code/`。工程的 `<工程目录>/code/render.py` 使用 `assets/engines/watercolor-modules/99/render.py`（慢歌片名分支拷 `assets/engines/watercolor-modules/东西/render.py`，慢歌 A1 看 `assets/engines/watercolor-modules/我好想你/story_a.py`，副行卡拉 OK 拷 `assets/engines/watercolor-modules/苦咖啡·唯一/render.py`，竖屏歌词条拷 `assets/engines/watercolor-modules/罗生门/render.py`，其他版本不用），拷来后按 `references/notes/04_片名署名实现.md`、`references/notes/03_写镜头代码.md` 改 `K_TITLE`、`TO`、`FADE`，工程的开场代码按本歌重写，接口参考 `assets/engines/watercolor-modules/可不可以给我你的微信/opening.py`。
- 片名卡：屏幕层《偷偷拍下你的样子》`assets/engines/watercolor-modules/偷偷拍下你的样子/story_b.py` 的 `titleBanner`、《你瞒我瞒》`assets/engines/watercolor-modules/你瞒我瞒/nm.py` 的 `openingTitle`；界面旁《可不可以给我你的微信》`assets/engines/watercolor-modules/可不可以给我你的微信/opening.py`；界面内`assets/engines/watercolor-modules/偷偷拍下你的样子/story_b.py` 的 `titleTag`。封面：《你瞒我瞒》`assets/engines/watercolor-modules/你瞒我瞒/cover.py`。
- 逐拍帧条：《苦咖啡·唯一》`assets/engines/watercolor-modules/苦咖啡·唯一/beatstrip_lean.py`（拷进工程 `<工程目录>/code/`）。其他版本整片进内存，90 秒以上会 OOM；短片要体感拍或表头带事件可用《你瞒我瞒》`assets/engines/watercolor-modules/你瞒我瞒/beatstrip.py`（参数 `--even --cols 2`）、《偷偷拍》`assets/engines/watercolor-modules/偷偷拍下你的样子/beatstrip960.py`（B[0] 为负加 `--k0 1`）；随附引擎的旧版逐拍帧条脚本不用。
- `<工程目录>/data/shots.json`：工程分镜脚本末尾导出 `[s['start'] for s in shots]`。
- 像素出片：工程副本的渲染器末尾加下面的适配器（《半岛铁盒》自带的会乱码，也换掉），再接 mvrun：320 `--scale 8` / 4，640 `--scale 4` / 2。像素引擎没有 shots.json（`--shots` 可省），拍表歌词按其 README 列的键手转。新画风才自己写（references/rendering.md），p5 模板只在有 GPU 时用。

```python
class Renderer:
    def __init__(self, cache_dir=None):
        pass

    def frame(self, t):
        a = frame_small(t)          # 640：np.clip(frame(t) + .5, 0, 255).astype(np.uint8)
        return np.dstack([a[..., 2], a[..., 1], a[..., 0], np.full(a.shape[:2], 255, np.uint8)])
```

### 4.2 先测速、单一数据源、先样片

- 先渲几帧测速再定并发；分镜一个数据文件，每帧只由 t 决定，随机数固定种子。
- 先做 15–20 秒样片自验（验收见 references/multi-reference.md，不发给用户等），从 0 渲到最难那段之后的 T1，参数和整片预览一致、分段可复用：`MV_OUT=1280x720 python3 scripts/mvrun.py . 480 2 120 0 T1 --profile preview --shots data/shots.json`。
- 对着音乐看样片：`ls <工作目录> | sed "s/.*/file '&'/" > out/sample.txt`，再 `ffmpeg -f concat -safe 0 -i out/sample.txt -i assets/song_clip.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest out/sample.mp4`。改了代码再跑前 `--redo` 改动区间或清空 `<工程目录>/chunks_preview/`。

### 4.3 写镜头代码（先读 03）

- 小数拍号先 `kt()` 换秒；表情只用 `clawd.EMO` 的 26 个键（写错静默变 neutral）；快乐体缺 ♥ ★ → ✓ ℃ 等，一律画，出片前用 `Font.unicharToGlyph` 扫一遍。
- 手持道具用 `handXY` 取手端、世界坐标画、补手点；两人中心距 ≥ 10.2u。人类 Q 版（`assets/engines/watercolor-modules/罗生门/couple.py`）：侧面手肘朝下、手离肩 3.3–3.9u，前视角手别举到脸旁，抱的东西走 `mid` 层。
- 道具、粒子不进歌词条、不盖脸；光束先画。`cam(t, cx, cy, z)` 把 (cx, cy) 放画面中心，每镜核 `540 + (脚 y − cy)·z < 940`（2:3 见 05）。
- 卡点：转场在拍点帧前做完，事件在拍点帧已可见。手机圆框不停在黑屏。镜头模块按名字 import，不用 `import *`。

### 4.4 逐镜核对

- 960×540 联系表（`MV_OUT=960x540 python3 code/sheet.py …`）每镜 6–10 帧、每格 ≥ 500 宽，含首尾帧和转场中间帧：看脸、穿模、道具朝向、字幕遮挡，有疑问放大单帧，不靠猜。卡点项目整片过帧条：`python3 code/beatstrip_lean.py 预览.mp4 out/strip --per 4`（视频从 0 秒开始）。每个梗问一句「第一眼看得懂吗」。
- 镜头多时交子任务审（清单：第一眼能否看懂、身体卡住、道具连手、主角有脚），分批与复查见 06。成片后从母版抽帧确认遮挡和片名署名。

### 4.5 出片

- 顺序：720p 预览 → 自查（子任务审完、改完）→ 抽查改动处 → 发聊天 → 直接渲 2K 写到用户指定的输出目录。审片期间别开母版。
  - 预览：`MV_OUT=1280x720 python3 scripts/mvrun.py . 480 2 120 --profile preview --shots data/shots.json --audio assets/song_clip.wav --out out/preview_720p.mp4`；超过 25MB 用 `python3 scripts/master.py preview out/preview_720p.mp4 out/preview_chat.mp4` 压。
  - 母版：`MV_OUT=2560x1440 python3 scripts/mvrun.py . 480 2 240 --profile master --shots data/shots.json --audio assets/song_clip.wav --out out/<歌名>_MV_2K.mp4`。像素去掉 `MV_OUT`、加 `--scale`，音频用工程剪好的（320 `<工程目录>/audio/song.wav`，640 `<工程目录>/assets/audio_cut.wav`）；2:3 见 05。
- 返修：`--redo` 区间取在镜头内部（碰边界会连带删邻镜的段，只有 wipe / iris 交叠才扩到邻镜）；镜头表、总时长或每帧都有的叠加层变了就删 `<工程目录>/chunks/` 整片重渲（先确认没有残留进程）；片名署名只局部重渲；旧作只改开头按 06 拼接。
- mvrun 一律前台跑（Bash timeout 600000、预算 480），没出 `ALL DONE` 就原样再发，从断点续。实测 720p 0.17–0.35 秒/帧（场景越密越慢），2K 0.6–1.3 秒/帧/进程。
- 动作保留预备、缓动、跟随；走路位移和步频匹配，不打滑。

### 4.6 竖屏 2:3（先读 05）

母版 1440×2160、预览 720×1080、逻辑画布 1080×1620（`assets/engines/watercolor-clawd/code/eng.py` 读 `MV_CANVAS=1080x1620`）。右侧按钮列占下半屏最右约 15%，作者名压住最下约 11%；歌词条在画高 78–86%、x 80–900；每镜重新摆位，不裁横屏；母版名 `<歌名>_MV_2K_2x3.mp4`，封面照旧 3:4 + 4:3。

## 5. 交付

- 清单：2K 母版（写用户指定的输出目录）、720p 预览、SRT/VTT（`scripts/lyrics_to_subtitles.py`）、3:4 + 4:3 标题关键帧（各自重画不截帧，标题和人物避开底部 1/6；人物 u：3:4 约 21–24，两人并排字少可到 30，4:3 约 26）、发布简介（2 个标题；3–5 行简介，末行写歌名、时间段和「原创××动画 · 非官方 MV」；5–8 个话题）。
- 文件名：`<歌名>_MV_2K.mp4`（2:3 加 `_2x3`）、`_MV.srt` / `.vtt`、`_标题关键帧_3x4.png` / `_4x3.png`、`_MV_分镜表.csv`、`_MV_工程代码.tgz`、`发布简介.txt`；旧作的名字不改。
- 写到用户指定目录：小文件走 stagedPath，母版走 `scripts/xfer.sh` 分片（先读 06）；拼不回就留云端告知，不切成可播放的小段。暂停时按 06 存续做材料。
- 新经验：先记工程 README。快歌只追加四种（用户当面指出的、本文件说错的、全新一类问题、可复用新道具模块）；慢歌、完整版详细追加（剧情反馈、旁白字幕、长片耗时与返修）。用 `cat >>` 写到用户指定输出目录中的 `<输出目录>/_技能更新待合并.md`（标题写歌名、时间、「未提交」），不各自提交技能（多窗口会互相覆盖）。用户说「更新技能」时由一个窗口精简合并：卡片内容进本文件，细则改 `references/notes/`（改前旧文件改名挪进 `<工程目录>/旧版/`）；清空待合并文件前核对 md5，合并期间别的窗口追加的留着，原文改名备份进 `<工程目录>/旧版/`。references、引擎文件改不到，过时说法登记在 08。

## 6. 旧说法

references、引擎 README 与本文件冲突时以本文件为准，逐条见 08。一律作废：4K / ×6 出片和「4K 再缩 2K」；`final*`、`make_*`、`run_*.sh`、`assets/engines/watercolor-clawd/code/preview.py` 出片，预览从母版压出；雾玻璃、窗上写字、写字的手；窗景当默认背景；片尾重出片名；关键帧只出 3:4；没连文件夹时用文件卡片交付或切成可播放段；申请删除权限；后台长跑、每轮预算 6600 秒；段落表先发确认；「发抖音优先 640」；一律不套恒定 BPM；水彩 31 个表情、`dancer`、spin、mix。

## 随附资源

`assets/engines/`（水彩《失眠》、像素 640《下雨了》附《白兰花》、像素 320《晴天》附《半岛铁盒》）、`assets/painted-character/`（p5 模板，MIT，来自 opus-video-skills / ClaudeAnimationBase）、`scripts/`（beat_track（beat_grid 只做粗估）、align_lyrics、lyrics_to_subtitles、master、mvrun、xfer.sh、get_fonts、build_strokes / hanzi、new_project）。仓库内工程模块清单见 `references/notes/07_道具与戏服.md`，来源许可见 references/sources.md。