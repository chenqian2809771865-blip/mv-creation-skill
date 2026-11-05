# 下雨了 · 像素 MV 工程（0:00–2:28）

- 逻辑画布 640×360，最近邻整数放大：×4 = 2560×1440（母版），×6 = 3840×2160（抖音上传版）。
- 分镜唯一数据源：`code/story.py`（26 镜，镜号/时间/歌词/画面/触发点），`python3 code/story.py` 生成 storyboard.md/csv。
- 时间轴：`assets/timing.json`（拍点、逐字歌词时间、前奏音点、结束 148.0s）。
- 音频：包里不带歌曲。用原曲 FLAC 重新切：
  `ffmpeg -i 下雨了.flac -t 148.0 -af "afade=t=out:st=145.3:d=2.7" -c:a pcm_s16le assets/audio_cut.wav`
- 出片：`python3 code/final.py`（2K+4K 同时编码）；单镜检查：`python3 code/csheet.py out.png 时间1 时间2 ...`；全片抽帧：`python3 code/fullsheet.py 0 148 2.45 out.png`；报错扫描：`python3 code/sweep.py`。
- 模块：core（网格/遮罩/阶梯光）、fx（雨/水花/涟漪/玻璃雾与水珠/倒影）、chars+sprite（他：礼帽长大衣；她：波波头黄伞；按目标尺寸直接画）、bust（她的近景）、street（整条街矢量场景，night/moon/memory 三种光）、skyline（城市俯景与两扇窗）、scn_window（他的窗）、scn_her（她的房间/书桌）、cloud（小云与暖色思念雨滴）、writing（雾上按真实笔顺写字）、shot_intro / shots_v1 / shots_c1 / shots_c2（镜头函数，按镜号分派）。
- 抖音友好：无整帧抖动和颗粒；粒子 12fps 步进；光晕为分阶平涂；镜头运动取整数像素。
