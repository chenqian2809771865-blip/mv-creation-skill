# 白兰花 · 像素 MV 工程（0:00–1:38，做到副歌结束）

- 引擎：《下雨了》640×360 高清像素引擎（core/sprite/fx 原样沿用），×4 = 2K 母版，×6 = 4K 抖音上传版。
- 人物：《小酒窝》男女主按 640 网格重画成 Q 版 SB 矢量精灵 `code/chibi.py`（他：格纹礼帽/格纹马甲/条纹领结；她：回忆=长发红蝴蝶结粉背带裙，cut=波波头+蝴蝶结，now=波波头深红唇梅色外套）。光照 `LIGHT`（night/lamp/warm/dusk/neon/corner/cold…）乘色+单侧轮廓光；`over=` 换色做路人。
- 场景：`sh_street.py` 午夜上海街（石库门弄堂口 安和里/理发/咖啡/舞厅/午夜场影院 钟+翻牌招牌+跑马灯/海报墙/公交站/南货店），招牌每帧叠加（翻牌锁定 flips、翻回空白 blank、灯泡 chase、lights 熄灭扫）；`scn_lane.py` 弄堂立面（此房出租）；`scn_rooms.py` 咖啡馆/理发店镜子/舞厅/餐桌/卧室。
- 分镜唯一数据源 `code/story.py`（29 镜）；时间轴 `assets/timing.json`（军鼓拟合的拍/小节、逐字歌词、全停）。
- 音频不在包里：`ffmpeg -i 白兰花.flac -t 98.0 -af "afade=t=out:st=96.0:d=2.0" -c:a pcm_s16le assets/audio_cut.wav`
- 出片：`code/run_final.sh`（2K、4K 各一个进程各一个编码器；8GB 内存下两个 4K slow 编码器会 OOM）→ 再用 ffmpeg 混入音轨 AAC 320k。
- 检查：`python3 code/csheet.py out.png t1 t2 …`、`python3 code/fullsheet.py 0 98 1.75 out.png`、`python3 code/sweep.py`；封面 `python3 code/cover.py`。
- 特写不画手、不画眼睛：电影票（S04）、手机（S06）、口红（S13）、白兰花（S22）都只拍道具；`code/hands.py` 留作备用，没有镜头在用。
- 招牌 `marquee_overlay` 左右对称：灯泡等距对位，亮灭从中轴展开，文字居中，按缩放选字号（放不下画短横）。
