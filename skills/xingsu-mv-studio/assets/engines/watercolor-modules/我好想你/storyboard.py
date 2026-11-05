# storyboard.py: the single source of truth for 《我好想你》(苏打绿) MV — 疑心病 Clawd couple, watercolour, NO beat grid.
# Full song from the first non-zero sample (S0 = 3399 samples), 329.14 s. Slow live-band ballad (~76 BPM felt, drifts up to 0.3 s
# off any constant grid), so shots are cut on sections, phrases and lyric lines; beat_track times are used only for the section hits.
# Times: seconds of the clip. L(i) = first syllable of lyric line i (data/lyrics.json), K(k) = tracked beat k (data/beats.json).
# Run: python3 code/storyboard.py  -> data/storyboard.json + data/shots.json + out/我好想你_MV_分镜表.csv
import json, os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, '..')
BJ = json.load(open(os.path.join(R, 'data', 'beats.json')))
B = BJ['beats']
LY = json.load(open(os.path.join(R, 'data', 'lyrics.json'), encoding='utf-8'))
DUR = 329.135
SONG = '我好想你'


def L(i, off=0.0):
    return LY[i][0] + off


def K(k):
    return B[k]


# section hits (measured): intro piano 4 bars | band K32 | band stops K64 (a held chord rings) | piano back 30.8 | voice L0
# interlude band K334 (bars every 8 k) | verse 2 from L18 | outro band K738 | ring-out 317.80 | silence ~325
RING = 317.80
STYLE = ('水彩手绘 + 沸腾墨线，纸张颗粒，Clawd 方块角色（他：陶土橙；她：粉色、头顶白色小花），慢歌叙事，不卡节拍网格，'
         '镜头跟段落和歌句走，16:9 横构图，无窗布景。主题：分开以后两个人都每天写一张「想你」的纸条藏进铁盒，谁也不说。')

SHOTS = [
    # ---------------------------------------------------------------- intro ① piano: A1 title device
    dict(id='S01', t0=0.0, tr='—', sec='前奏① 钢琴', scene='夜里的书桌，只有台灯一圈暖光，桌上一张黄色便利贴',
         action='笔自己写出「我好想你」（片名，最后一笔落在第二句钢琴 K16），署名在旁边淡入；K24 镜头退一级，纸条折好落进桌边的铁盒——盒里已经塞满一模一样的折纸',
         camera='近景 → 退一级', tone='深蓝夜 + 台灯暖黄'),
    # ---------------------------------------------------------------- intro ② band: memory flash, half a bar each
    dict(id='S02', t0=K(32), tr='flash', sec='前奏② 乐队', scene='铁盒特写', action='乐队砸进来，盒盖弹开，折纸像烟花一样涌出来、一张张展开',
         camera='中近景，纸片扑向镜头', tone='暖金'),
    dict(id='S03', t0=K(36), tr='cut', sec='回忆快闪', scene='他的房间（回忆：明亮饱和）', action='两人一起挂串灯，她踩在小凳上，灯一串串亮起',
         camera='中景', tone='暖黄'),
    dict(id='S04', t0=K(40), tr='cut', sec='回忆快闪', scene='床上', action='枕头仗，羽毛飞起来，两人笑倒', camera='中景', tone='暖粉'),
    dict(id='S05', t0=K(44), tr='cut', sec='回忆快闪', scene='书桌边', action='两只马克杯碰杯，冒出爱心热气', camera='中景', tone='暖橙'),
    dict(id='S06', t0=K(48), tr='cut', sec='回忆快闪', scene='书桌', action='她把头上的小白花插进他的杯子里，他脸红', camera='中景', tone='暖粉'),
    dict(id='S07', t0=K(52), tr='cut', sec='回忆快闪', scene='照片墙前', action='两人举起拍立得自拍，闪光，照片吐出来', camera='中景', tone='暖白'),
    dict(id='S08', t0=K(56), tr='cut', sec='回忆快闪', scene='串灯下', action='慢慢跳舞转圈，小爱心飘起', camera='中景', tone='金粉'),
    dict(id='S09', t0=K(60), tr='cut', sec='回忆快闪 · 离开', scene='门口', action='她拖着行李站在门口，回头看一眼，伸手按灯——K64 乐队急停的那一下「啪」',
         camera='中景', tone='暖 → 黑'),
    # ---------------------------------------------------------------- intro ③ ring-out + piano: the dark room
    dict(id='S10', t0=K(64), tr='cut', sec='前奏③ 余音', scene='全黑', action='只剩门口那一幕的残影，跟着低音和弦的衰减慢慢褪色、淡没',
         camera='定', tone='黑 + 灰蓝残影'),
    dict(id='S11', t0=30.80, tr='dissolve', sec='前奏③ 钢琴', scene='现在：黑暗里的房间，小夜灯',
         action='慢慢看清：门口她的拖鞋、杯子里干掉的小白花、两个枕头；镜头缓推到墙上的开关，他站在开关旁（剪影）；37.8 吸气',
         camera='缓横移 + 推', tone='深蓝'),
    # ---------------------------------------------------------------- verse 1 (him)
    dict(id='S12', t0=L(0), tr='cut', sec='主歌1 · 示例歌', lyric=0, scene='整间房（亮灯）', action='「开」字上灯亮：很大的房间，很小的他；他环顾四周',
         camera='大全景，缓拉', tone='暖白但空'),
    dict(id='S13', t0=L(1, -.3), tr='dissolve', sec='主歌1 · 示例歌词 占位文字', lyric=1, scene='床',
         action='他坐在床边，旁边她的粉色枕头整整齐齐；他从枕边捡起她的发夹，握在手里', camera='中景，横移到床', tone='暖白偏冷'),
    dict(id='S14', t0=L(2, -.35), tr='cut', sec='主歌1 · 示例歌 词占位文字', lyric=2, scene='开关旁',
         action='「关」字灯灭；他又按开、又关——亮着暗着，房间都一样空', camera='中景', tone='暖白 ↔ 深蓝'),
    dict(id='S15', t0=L(3, -.25), tr='dissolve', sec='主歌1 · 示例歌词 占位文字', lyric=3, scene='夜里的床边',
         action='他捧着一颗贴着创可贴的裂心，转身想递给旁边——旁边是空的；心暗下去，他把它抱回怀里', camera='中近景', tone='深蓝 + 一点红'),
    dict(id='S16', t0=L(4, -.3), tr='dissolve', sec='主歌1 · 示例歌词占位文', lyric=4, scene='书桌一角：挂历、挂钟、铁盒',
         action='挂历一页页飞走、钟针飞转、昼夜交替；铁盒里的纸条一天天堆高', camera='定', tone='昼夜闪换'),
    dict(id='S17', t0=L(5, -.25), tr='dissolve', sec='主歌1 · 示例歌词占', lyric=5, scene='书桌前', action='他的头顶慢慢长出白发，戴上圆眼镜，仍在写纸条',
         camera='中近景', tone='暖灯'),
    dict(id='S18', t0=L(6, -.3), tr='wipe', sec='主歌1 · 示例歌词占 位文字示例歌', lyric=6, scene='黄昏的商店街（无橱窗）',
         action='她拖着行李越走越远；他手里一只写着「快乐」的黄气球，绳子一松，气球飘走', camera='中景', tone='黄昏紫粉'),
    dict(id='S19', t0=L(7, -.25), tr='dissolve', sec='主歌1 · 示例歌词占', lyric=7, scene='照片墙特写', action='拍立得里两个人一张张褪色成空白',
         camera='近景，缓移', tone='褪色'),
    dict(id='S20', t0=L(8, -.25), tr='dissolve', sec='主歌1 · 示例歌词占', lyric=8, scene='夜里的床', action='他睡着，梦泡里是她在笑；泡泡「啵」地破了',
         camera='中景', tone='深蓝'),
    dict(id='S21', t0=L(9, -.25), tr='dissolve', sec='主歌1 · 示例歌词占位文字示', lyric=9, scene='夜里的山坡大树下',
         action='他胸前那颗红心变灰、变成气球，慢慢飘远成星星；他面无表情', camera='全景，跟升', tone='深蓝星空'),
    # ---------------------------------------------------------------- chorus 1 (him)
    dict(id='S22', t0=L(10, -.35), tr='dissolve', sec='副歌1 · 示例歌词', lyric=10, scene='书桌（侧坐）', action='他坐在桌边，台灯下又写一张纸条',
         camera='中景', tone='台灯暖黄'),
    dict(id='S23', t0=3.3 + L(10, -.35), tr='cut', sec='副歌1 · 示例歌', lyric=10, scene='桌面俯拍', action='纸条上写「想你」，折好，塞进已经满出来的铁盒',
         camera='俯拍道具特写', tone='暖黄'),
    dict(id='S24', t0=L(11, -.3), tr='cut', sec='副歌1 · 示例歌词占', lyric=11, scene='床边', action='他把铁盒推进床底，拍平床单，站起来挤出一个笑',
         camera='中景', tone='暖白'),
    dict(id='S25', t0=L(12, -.3), tr='dissolve', sec='副歌1 · 示例歌词占位文', lyric=12, scene='夜里的山坡大树下',
         action='他站在木箱上踮着脚望远方，一颗星星眨了眨，变成一朵小白花的形状', camera='全景', tone='深蓝 + 星光'),
    dict(id='S26', t0=L(13, -.3), tr='dissolve', sec='副歌1 · 示例歌词占位文', lyric=13, scene='房间（暗）', action='一圈拍立得绕着他转，像旋转木马',
         camera='中景，缓推', tone='暗蓝 + 照片暖光'),
    dict(id='S27', t0=L(14, -.3), tr='dissolve', sec='副歌1 · 示例歌词占位文', lyric=14, scene='靠着床坐在地上', action='半身近景，闭着眼，泪光滑下来，滴在手里的纸条上晕开',
         camera='半身近景', tone='深蓝'),
    dict(id='S28', t0=L(15, -.3), tr='wipe', sec='副歌1 · 示例歌词占位文', lyric=15, scene='白天的商店街', action='他戴着墨镜吹着口哨走过人群，墨镜下面悄悄滑下一滴泪',
         camera='跟拍横移', tone='明亮'),
    dict(id='S29', t0=L(16, -.3), tr='dissolve', sec='副歌1 · 示例歌词 占位文', lyric=16, scene='夜里的床边，手机', action='手机屏幕「呼叫 她…」，响了两下他就按掉',
         camera='中景 + 手机', tone='深蓝 + 屏幕光'),
    dict(id='S30', t0=L(17, -.3), tr='cut', sec='副歌1 · 示例歌词占', lyric=17, scene='照片墙前', action='他把一张「我很好！」便利贴贴在两人的合照上，点点头',
         camera='中景', tone='暖白'),
    # ---------------------------------------------------------------- interlude: the backstory (band, 2 bars per shot)
    dict(id='S31', t0=K(334), tr='flash', sec='间奏 · 回忆', scene='雨天的商店街', action='第一次见面：下雨，她把伞分给他一半',
         camera='中景', tone='饱和暖'),
    dict(id='S32', t0=K(350), tr='wipe', sec='间奏 · 回忆', scene='晴天山坡大树下野餐', action='她把头上的小白花别到他头上，两人笑',
         camera='中景', tone='明亮绿'),
    dict(id='S33', t0=K(366), tr='wipe', sec='间奏 · 裂痕', scene='烛光餐厅', action='她一个人等，挂钟从 8 点转到 11 点，蜡烛烧短；他才赶到，满头汗',
         camera='中景', tone='暖 → 冷'),
    dict(id='S34', t0=K(382), tr='cut', sec='间奏 · 争吵', scene='他的房间', action='她戴回侦探帽、举着放大镜（疑心病），他也冒火；两人头顶的乌云打雷',
         camera='中景', tone='灰紫'),
    dict(id='S35', t0=K(398), tr='cut', sec='间奏 · 离开', scene='门口', action='她收好行李，他背过身；她回头一眼，关上门——房间暗下来',
         camera='中景', tone='冷'),
    # ---------------------------------------------------------------- verse 2 (her, mirrored room)
    dict(id='S36', t0=K(414), tr='cut', sec='主歌2 · 示例歌词占位', lyric=18, scene='她的房间（他房间的镜像，粉色）',
         action='「开」字上灯亮：她的房间一样大、一样空', camera='大全景', tone='暖粉但空'),
    dict(id='S37', t0=L(19, -.3), tr='dissolve', sec='主歌2 · 示例歌词 占位文字', lyric=19, scene='她的床', action='她坐在床边，抱着一只橙色的他的玩偶',
         camera='中景', tone='粉'),
    dict(id='S38', t0=L(20, -.35), tr='cut', sec='主歌2 · 示例歌', lyric=20, scene='她的开关', action='她也一开一关，一样空', camera='中景', tone='粉 ↔ 深蓝'),
    dict(id='S39', t0=L(21, -.25), tr='dissolve', sec='主歌2 · 示例歌词', lyric=21, scene='夜里她的床边', action='她的裂心也无处可递', camera='中近景', tone='深蓝'),
    dict(id='S40', t0=L(22, -.3), tr='dissolve', sec='主歌2 · 示例歌词占位文', lyric=22, scene='她的挂历和铁盒', action='一样的时间飞逝；她的桌角也有一个铁盒',
         camera='定', tone='昼夜闪换'),
    dict(id='S41', t0=L(23, -.25), tr='dissolve', sec='主歌2 · 示例歌词占', lyric=23, scene='她的书桌', action='她也长出白发，戴上眼镜', camera='中近景', tone='暖灯'),
    dict(id='S42', t0=L(24, -.3), tr='wipe', sec='主歌2 · 示例歌词占', lyric=24, scene='下雨的商店街（初遇的地方）',
         action='她一个人撑着伞，伞习惯性地偏向旁边空着的那一半', camera='中景', tone='雨夜蓝'),
    dict(id='S43', t0=L(25, -.25), tr='dissolve', sec='主歌2 · 示例歌词占', lyric=25, scene='她的照片墙', action='照片一张张褪色', camera='近景', tone='褪色'),
    dict(id='S44', t0=L(26, -.25), tr='dissolve', sec='主歌2 · 示例歌词占', lyric=26, scene='她的床', action='梦里是他，泡泡破了', camera='中景', tone='深蓝'),
    dict(id='S45', t0=L(27, -.25), tr='dissolve', sec='主歌2 · 示例歌词占', lyric=27, scene='山坡大树下', action='她的心也变灰飘走', camera='全景', tone='深蓝'),
    # ---------------------------------------------------------------- chorus 2: the twist + split screens
    dict(id='S46', t0=L(28, -.35), tr='dissolve', sec='副歌2 · 示例歌词占位文', lyric=28, scene='她的书桌',
         action='她也在台灯下写一张粉色纸条「想你」——镜头退开：她也有一个塞满纸条的铁盒', camera='中景 → 退一级', tone='暖黄 + 粉'),
    dict(id='S47', t0=L(29, -.3), tr='cut', sec='副歌2 · 示例歌词占', lyric=29, scene='她的床边', action='她也把铁盒推进床底，挤出一个笑', camera='中景', tone='暖白'),
    dict(id='S48', t0=L(30, -.3), tr='wipe', sec='副歌2 · 示例歌词占位文', lyric=30, scene='分屏：两座山坡', action='左他右她，同时踮着脚望向同一颗星',
         camera='分屏', tone='深蓝'),
    dict(id='S49', t0=L(31, -.3), tr='dissolve', sec='副歌2 · 示例歌词占位文', lyric=31, scene='她的房间', action='照片绕着她转', camera='中景', tone='暗粉'),
    dict(id='S50', t0=L(32, -.3), tr='wipe', sec='副歌2 · 示例歌词占位文', lyric=32, scene='分屏', action='两个人都合眼落泪', camera='分屏半身', tone='深蓝'),
    dict(id='S51', t0=L(33, -.3), tr='wipe', sec='副歌2 · 示例歌词占位文', lyric=33, scene='白天的商店街',
         action='两人都戴着墨镜，从两头走来，擦肩而过谁也没回头；走过之后两人同时停了一下', camera='横移', tone='明亮'),
    dict(id='S52', t0=L(34, -.3), tr='wipe', sec='副歌2 · 示例歌词', lyric=34, scene='分屏：两部手机',
         action='他拨给她「呼叫 她…」，她那边亮起「他 来电」；她刚要接，他先挂了——「未接来电」', camera='分屏', tone='深蓝 + 屏幕光'),
    dict(id='S53', t0=L(35, -.3), tr='cut', sec='副歌2 · 示例歌词占', lyric=35, scene='分屏：两面照片墙', action='两人同时把「我很好！」贴在合照上', camera='分屏',
         tone='暖白'),
    dict(id='S54', t0=L(36, -.3), tr='dissolve', sec='副歌2 · 示例歌词', lyric=36, scene='分屏：两张书桌', action='同一时间，两盏台灯下，两人都在写纸条',
         camera='分屏', tone='台灯暖黄'),
    dict(id='S55', t0=L(37, -.3), tr='cut', sec='副歌2 · 示例歌词占', lyric=37, scene='分屏：两张床', action='两人同时把铁盒推进床底', camera='分屏', tone='暖白'),
    dict(id='S56', t0=L(38, -.3), tr='dissolve', sec='副歌2 · 示例歌词', lyric=38, scene='分屏：夜里躺在床上',
         action='两人侧躺，隔着分屏线面对面，像隔着一堵墙', camera='分屏', tone='深蓝'),
    dict(id='S57', t0=L(39, -.3), tr='dissolve', sec='副歌2 · 示例歌词占', lyric=39, scene='分屏：床底的铁盒', action='两人捂着心口闭眼；床底的两个铁盒微微发光',
         camera='分屏', tone='深蓝 + 暖光'),
    # ---------------------------------------------------------------- outro band: the notes fly and meet
    dict(id='S58', t0=K(738), tr='flash', sec='尾奏 · 乐队', scene='分屏：两个铁盒', action='两个铁盒同时弹开，纸条涌出来', camera='分屏', tone='暖金'),
    dict(id='S59', t0=K(746), tr='cut', sec='尾奏', scene='夜空、山坡', action='黄色和粉色两股纸条从两边飞过夜空', camera='大全景', tone='深蓝 + 黄粉'),
    dict(id='S60', t0=K(762), tr='dissolve', sec='尾奏', scene='夜空', action='两股纸条在中间汇合，旋成一颗大心，回忆照片在里面闪', camera='大全景，缓推',
         tone='深蓝 + 暖'),
    dict(id='S61', t0=K(778), tr='dissolve', sec='尾奏', scene='夜空、山坡', action='大心散开，纸条像雪一样慢慢落下', camera='全景，下摇', tone='深蓝'),
    dict(id='S62', t0=K(794), tr='cut', sec='尾奏', scene='夜空', action='跟着一张粉色纸条飘下来', camera='跟拍', tone='深蓝 + 粉'),
    dict(id='S63', t0=RING, tr='dissolve', sec='余音', scene='他的房间（暗）', action='粉色纸条从上面飘落到他的书桌上，他看见了', camera='中景', tone='深蓝'),
    dict(id='S64', t0=321.6, tr='cut', sec='余音', scene='桌面俯拍', action='纸条展开：她的字「我也是」+ 一颗小心', camera='道具特写', tone='粉'),
    dict(id='S65', t0=324.4, tr='dissolve', sec='结尾', scene='他的书桌', action='他捧着纸条，脸红地笑了；台灯「咔」地亮起，串灯也亮了；淡到全黑',
         camera='中近景', tone='暖'),
]


def sungIn(a, b):
    s = ''
    for st, en, txt, ts in LY:
        cs = [c for c in txt if c != ' ']
        for c, tc in zip(cs, ts):
            if a - .1 <= tc < b - .1:
                s += c
    return s


def build():
    out = []
    for i, s in enumerate(SHOTS):
        a = s['t0']
        b = SHOTS[i + 1]['t0'] if i + 1 < len(SHOTS) else DUR
        assert b > a + .5, (s['id'], a, b)
        d = dict(s)
        d.update(start=round(a, 3), end=round(b, 3), dur=round(b - a, 3), sung=sungIn(a, b),
                 prompt=STYLE + s['scene'] + '。' + s['action'] + '。')
        out.append(d)
    sb = dict(song=SONG, artist='苏打绿', dur=DUR, bpm=round(BJ['bpm'], 2), beats=B, ring=RING, shots=out)
    json.dump(sb, open(os.path.join(R, 'data', 'storyboard.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump([d['start'] for d in out], open(os.path.join(R, 'data', 'shots.json'), 'w'))
    os.makedirs(os.path.join(R, 'out'), exist_ok=True)
    with open(os.path.join(R, 'out', f'{SONG}_MV_分镜表.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['镜号', '段落', '起', '止', '时长', '唱到', '画面', '动作', '镜头', '转场', '色调', '生成提示词'])
        for d in out:
            w.writerow([d['id'], d['sec'], f"{d['start']:.2f}", f"{d['end']:.2f}", f"{d['dur']:.2f}", d['sung'], d['scene'], d['action'],
                        d['camera'], d['tr'], d['tone'], d['prompt']])
    return sb


if __name__ == '__main__':
    sb = build()
    import statistics
    ds = [d['dur'] for d in sb['shots']]
    print(len(ds), 'shots; median %.2f s, min %.2f, max %.2f' % (statistics.median(ds), min(ds), max(ds)))
    for d in sb['shots']:
        print(d['id'], f"{d['start']:7.2f} {d['dur']:5.2f} {d['tr']:8s} {d['sung']}")
