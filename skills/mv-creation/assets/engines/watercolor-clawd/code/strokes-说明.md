# 笔顺示例数据说明

本目录的 `strokes.json` 是 [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) 的 `graphics.txt` 派生数据，适用 Arphic Public License（文鼎公众授权书）。完整许可与上游归属见仓库根目录 `THIRD_PARTY_LICENSES.txt`。

2026-11-05 使用本技能的 `scripts/build_strokes.py` 重新提取，仅保留公开占位歌词及实际手写片名所需的 16 个字符。`strokes-字符.txt` 列出额外的片名字，不包含歌词。未改变上游字形的笔画路径或中线坐标。

`_license`、`_modification` 保存数据来源与修改声明；引擎仍按单个汉字取值，不影响现有的字符查询接口。更换用户自己的歌词后，需要重新生成此文件。

从 `skills/mv-creation/` 目录执行：

```bash
python3 scripts/build_strokes.py assets/engines/watercolor-clawd/data/lyrics.json assets/engines/watercolor-clawd/code/strokes-字符.txt --out assets/engines/watercolor-clawd/code/strokes.json --graphics graphics.txt
```

`graphics.txt` 可从上游下载到工作目录；不要提交完整上游数据。也可省略 `--graphics` 让脚本使用其下载缓存。不要加 `--merge`，否则会保留旧歌需要的字符。脚本重建后可依照本文件补回 `_license` 和 `_modification` 来源与日期声明。
