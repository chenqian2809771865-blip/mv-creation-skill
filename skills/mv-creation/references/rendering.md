# 实现与渲染

先检查可用的 Python、ffmpeg、Node/npm、Chrome/Chromium，不假定存在 GPU 或虚拟机。

## 选实现

| 情况 | 用什么 |
|---|---|
| 有现成引擎对得上画风或角色（Clawd 男女主水彩、像素校园角色、高清像素） | 复制 `assets/engines/<引擎>/` 成新工程，见 `assets/engines/README.md` |
| 新画风：像素 | PIL/numpy，从低分辨率画布整数放大 |
| 新画风：矢量、纸感 | Skia；可以借用 `watercolor-clawd/code/eng.py` 的画布与纹理 |
| 有 GPU 或本地机器，要 p5.brush 原版笔刷 | 随附 p5 模板（下文） |

先渲少量**实际分辨率**的帧，实测耗时再定方案；各环境的参考速度见 references/env-notes.md。

## Python 工程与分段渲染（`scripts/mvrun.py`）

工程结构：

```text
project/
  code/render.py   # FPS、DUR、输出尺寸（OUT_W/OUT_H，没有则用 W/H）；Renderer(cache_dir).frame(t) → uint8 BGRA (H,W,4)
  chunks/          # mvrun 自动建立
```

```bash
python3 scripts/mvrun.py PROJECT                       # 默认：每轮预算 6600 s、2 进程、240 帧一段、master 档
python3 scripts/mvrun.py PROJECT 6600 2 240 --shots shots.json --audio song.wav --out final.mp4
python3 scripts/mvrun.py PROJECT 600 2 48 10 20 --profile preview   # 只渲 10–20 秒的预览段
python3 scripts/mvrun.py PROJECT --redo 31.5 36.2 --shots shots.json  # 返修：删掉覆盖该区间的段再补渲
python3 scripts/mvrun.py PROJECT --status                             # 进度与 worker 是否还活着
```

- **编码档位**：参数全部来自 `scripts/master.py`。master 档出的分段就是最终编码；preview 档的分段放在单独的 `chunks_preview/`，不会混进母版。
- **`--shots`**：传入镜头起点（秒）的 JSON 列表。分段边界会落在镜头起点上，返修时只需重渲涉及的镜头。长镜头按 CHUNK 帧再切。
- **`--scale N`**：像素引擎输出逻辑网格，由 ffmpeg 做最近邻 ×N 放大。
- **后台运行与续跑**：作为后台任务跑，到点前不再开新段；重复运行直到输出 `ALL DONE`。给了 `--audio/--out` 时，跑完会自动拼接、配音并执行 `master.py check`。
- **计划冲突保护**：分段计划变了（CHUNK 或镜头表不同），mvrun 会拒绝混用旧段。要么删掉旧段，要么沿用旧计划。
- **渲染途中别改镜头文件**：镜头模块是按镜号懒加载的。画面改动后用 `--redo` 清理受影响的段，转场交叠的部分也要算进去。

帧只由 t 决定，随机数固定种子，续渲不依赖上一帧。拿到成片先核对总帧数等于 round(时长×fps)；`master.py check` 会做这项检查。

## 笔刷角色 p5 模板（有 GPU 时）

```bash
python3 scripts/new_project.py /path/to/project [--install] [--demo]
cd /path/to/project && npm ci
node render.mjs --sheet=0.2,1,2 --cols=3 --w=480 --out=out/check/keyframes.jpg
node render.mjs --strip=1.8:2.2 --out=out/check/motion.jpg
node render.mjs --stills=1,5 --out=out/check/stills    # 测成片尺寸的真实耗时
node render.mjs --frames --workers=2
node render.mjs --encode --audio=assets/song.m4a --out=out/video.mp4
```

- **配置与场景**：
  - `src/config.js`：全片 `duration`、动作参考 `bpm`、重拍偏移 `offset`、可选的 `audio`。
  - `src/scenes/`：一个场景一个文件，用 IIFE 隔离，`shots([[开始秒, fn], ...])` 注册，`fn(t, lt, dur)`；记得在 `studio.html` 里加载。
- **画布**：模板原生 1920×1080。像素风要从自己的低分辨率画布整数放大。
- **编码与环境**：
  - `--frames` 和 `--encode` 用相同的 `--fps`（默认 24）。
  - Chrome 不在默认路径时，加 `--chrome=/path`。
  - GPU 不可用时试 `--soft-gl`，但云端通常慢到不可行，这时改用水彩 Skia 引擎。
  - `--encode` 出片后，用 `master.py` 重编或检查色彩标记。
- **字体**：`studio.html` 从 Google Fonts 加载字体。离线时会多等约 40 秒，并静默回退到系统字体。出成片前看一帧确认字体，必要时改成本地 `@font-face`。
- **改动后的缓存**：
  - `--frames` 会跳过已有帧，改镜头后要清理对应的旧帧。
  - 只换音频时重新混流即可，不用重画。
  - 模板的 `--clip --range=a:b` 会同时截取对应的音频区间。
- **Clawd 接口**：见 references/characters.md。

## 通用

- **动作**：保留预备、缓动和跟随动作；走路位移要和步频、步幅匹配，不打滑。
- **审片**：先出联系表，按段看构图和一致性；再连续播放，看动作、转场和音画关系。只有静帧，不能证明动画已经达标。
