# 组件来源


## 随附组件

- **p5 角色模板与粗估拍脚本**：`assets/painted-character/` 与 `scripts/beat_grid.py` 取自 [tuzhechen2005/opus-video-skills](https://github.com/tuzhechen2005/opus-video-skills) 的 painted-animation 技能。
  - 角色模板的上游是 John Heibel 的 [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase)，创作方法参考 [PDoomVideo](https://github.com/JohnHeibel/PDoomVideo)。
  - 分发时保留模板的 `LICENSE` 和根目录 `THIRD_PARTY_LICENSES.txt` 里的 MIT 声明。
  - 模板保留了 Clawd 的名称与实现。MIT 声明只针对随附的软件与文档，不能表述为 Anthropic 对这个形象的额外授权。
- **`assets/engines/`**：用户自己的 MV 工程，于 2026-10-29 从桌面整理而来。各文件取自哪一版，见各引擎目录下的 README。
- **用户原版「mv制作」技能中的脚本**：
  - `lyrics_to_subtitles.py`、`mvrun.py`、`hanzi.py` 源自这套技能。
  - `mvrun.py` 已改为从 `master.py` 取编码参数，并支持按镜头分段、返修和查看状态。
  - `hanzi.py` 改为首次用到时才读取数据。
- **从用户工程中验证过的流程整理成的脚本**：
  - `beat_track.py` 源自 `beats_refine.py`。
  - `align_lyrics.py` 源自 `sep.py`、`align.py`、`asr_multi.py`、`prep_audio.py`。
  - `master.py` 源自各工程的 `master.py`。
  - `xfer.sh` 是传输分片流程的脚本化。

## 运行时按需下载（不随包）

- **UVR `UVR-MDX-NET-Voc_FT.onnx`**：来自 GitHub releases `TRvlvr/model_repo`，用于人声分离。
- **sherpa-onnx SenseVoice**：模型 `sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17`，来自 GitHub releases `k2-fsa/sherpa-onnx` 的 asr-models，用于逐字识别。
- **[Make Me a Hanzi](https://github.com/skishore/makemeahanzi)**：`graphics.txt`，Arphic Public License，用于笔顺数据（`build_strokes.py`）。随工程分发笔画数据时要保留其许可。
- **字体**（用 `get_fonts.py` 获取）：
  - GNU Unifont：npm `@fontpkg/unifont`
  - Fusion Pixel 12px：npm `@vp-tw/cjk-web-fonts-fusion-pixel-font`，SIL OFL 1.1
  - LXGW 文楷：GitHub `lxgw/LxgwWenKai`，OFL
  - ZCOOL 快乐体（Google Fonts，OFL）随水彩引擎附带。
- **p5.js、p5.brush、puppeteer-core**：由模板的 `package-lock.json` 锁定版本，安装时获取。

## 公开整理版补充（2026-11-05）

- 01–08 原编号细则已放入 `references/notes/`；工程代码来源、直接引用与本地依赖见 `assets/engines/watercolor-modules/README.md` 和 `assets/engines/pixel-modules/README.md`。
- 所有歌曲歌词、代码中的歌词片段及原曲对白替换成中文占位文本；逐字时间数组和原有数值保持不变，不能代替实际歌曲的重新对齐。
- ZCOOL KuaiLe 字体与 [Google Fonts 上游文件](https://github.com/google/fonts/tree/main/ofl/zcoolkuaile) 字节一致；随附 SIL Open Font License 1.1 全文在仓库根 `THIRD_PARTY_LICENSES.txt`。
- `strokes.json` 是 [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) 的 `graphics.txt` 的派生子集，使用 Arphic Public License；重建日期、方式与需要的字符见相邻说明。许可中英全文随仓库分发。
- 模型来源：[UVR 模型仓库](https://github.com/TRvlvr/model_repo/releases)、[sherpa-onnx 模型发布页](https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models)。字体来源：[LXGW 文楷](https://github.com/lxgw/LxgwWenKai)、[Unifont](https://www.unifoundry.com/unifont/)、[Fusion Pixel](https://github.com/TakWolf/fusion-pixel-font)。
