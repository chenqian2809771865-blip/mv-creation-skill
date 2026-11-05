# 《失眠》MV 工程（Suki刘舒妤 · 疑心病男女主 · Clawd 水彩手绘 · Skia 引擎 · 节拍卡点）

> 历史工程记录；歌词已替换成占位文字。本文提到的 `code/prep_audio.py`、`code/master.py`、`run_master.sh` 不在源技能 ZIP 中，未补造；当前流程以技能根 `SKILL.md` 为准，音频预处理和出片使用随附 `scripts/` 的现有工具。

片段：用户给的 29.79 秒音频（从「示例歌词内容示例」到「示例歌词内容」），从第一个非零样本 S0 = 0.130 s 切起，29.66 秒，712 帧 @24fps。
实测 127.62 BPM（DJ 版，四拍底鼓），拍表 data/beats.json（HPSS 打击层逐拍 ±35 ms 取峰 + 9 拍滑动拟合，片段时间）；小节首拍 = k3 + 4n。
k19–k34 底鼓和贝斯抽空（断鼓段），k35 = 鼓回来（「示例过」的「过」）。
音频不在包内：把用户的 mp4 抽成 wav 放到 <工程目录>/audio/clip.wav，跑 code/prep_audio.py（切 S0、末尾 0.25 s 淡出 → assets/song_clip.wav）。

- code/eng.py / clawd.py / props.py / sets.py / sets2.py / hl.py   水彩 + 沸腾墨线引擎（沿用《疑心病》《后来》；BOIL 12 fps；emotions() 已修：过渡时保留角色自己的颜色）
- code/sm.py          本片道具与场景：毛线团、毛线乱团 tangle（可避开脸）、针织片 knitPiece（可织字）、围巾 scarfRibbon/scarfHang/scarfBand、
                      七段数码闹钟、床头柜、她的卧室（正面构图：窗在身后、被子在前）、礼物盒、纸板立牌 standee（可翻面）、头顶小乌云、
                      可逐扇熄灯的公寓外立面 facade2（黑窗里的小眼睛）、窗台烟灰缸、烟 smokeCurl/smokeRing、烟聚成的他 smokeHim、夜公园
- code/storyboard.py  分镜唯一数据源（16 镜，镜头用拍号 k 写）→ data/storyboard.json 与 out/失眠_MV_分镜表.csv/.md
- code/story.py       镜头函数 s01–s16（只由 t 决定），每拍一个可见事件；code/common.py 拍号工具（bump 每拍轻推，断鼓段减半）
- code/render.py      转场（pop/wipe/iris/flash/dissolve）、卡拉 OK（快乐体，逐字变粉，提前 2 帧）、结尾 0.2 s 淡黑
- code/master.py + run_master.sh  上传母版（CRF 14、slow、-tune animation、BT.709、锁 level 5.1 ref=4）：run_master.sh 2560x1440 m2k / 3840x2160 m4k
- code/preview.py 快速预览；code/sheet.py 按时间出联系表；code/beatstrip.py 每拍前/拍/后三帧自检
- code/cover.py       3:4 封面（1440×1920，同一套角色和卧室重画）
- data/lyrics.json    校准歌词 [开始, 结束, 文本, 逐字时间]（UVR 分离人声 + SenseVoice 多窗识别，文字用用户 LRC）
- fonts/              ZCOOL 快乐体、霞鹜文楷（均 OFL）
