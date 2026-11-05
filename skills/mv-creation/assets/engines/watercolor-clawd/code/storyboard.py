# storyboard.py: the single source of truth for 《失眠》 (Suki刘舒妤) clip MV — 疑心病 Clawd couple, beat-locked.
# Shots are written in measured beat indices k (data/beats.json); bar n starts at k = 3 + 4 (n - 1).
# Run: python3 code/storyboard.py  -> data/storyboard.json + out/失眠_MV_分镜表.csv / .md
import json, os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, '..')
BJ = json.load(open(os.path.join(R, 'data', 'beats.json')))
B = BJ['beats']
DUR = BJ['dur']
LY = json.load(open(os.path.join(R, 'data', 'lyrics.json'), encoding='utf-8'))
BREAK = (19, 35)          # k19..k34: the kick and bass drop out (breakdown); k35 = the drop

STYLE = '水彩手绘，纸张纹理，轻微沸腾的墨线，柔和晕染与水痕边，Clawd 方块角色（他：陶土橙；她：粉色、头顶白色小花），16:9 横构图。'

SHOTS = [
    dict(id='S01', section='前奏拍 · A1 画内标题', k0='START', k1=3, tr='—',
         scene='夜里床头柜特写：靛蓝墙纸，一只电子闹钟亮着「03:00」，毛线篮里粉色毛线团，一截织到一半的粉围巾搭在篮边，围巾上用白线织着「失眠」',
         action='无人物（器物阶段）',
         events=[(0, '台灯咔哒亮起，暖光铺满（「示」）'), (1, '「失」字一针针织出；毛线团一跳'), (2, '「眠」字织出，闹钟冒号闪')],
         camera='特写，缓慢推近', tone='夜 · 靛蓝 + 台灯暖黄'),
    dict(id='S02', section='副歌一 · 示例歌词内', k0=3, k1=7, tr='pop',
         scene='她的卧室（正面构图）：她坐在床上，被子盖到胸前，身后是窗、月亮和城市夜景、串灯、书架（上面放着那顶侦探帽）；右边床头柜上闹钟 03:00',
         action='她（正面）织围巾，毛线越缠越乱，最后整团毛线把她缠住',
         events=[(3, '「示例」字章落地，针一碰「咔」'), (4, '毛线打出第一个圈'), (5, '圈越绕越多，缠上她的小花'), (6, '整团乱线罩住她，她眼睛转圈')],
         camera='中景，每拍轻推', tone='夜 · 靛蓝 + 台灯暖黄'),
    dict(id='S03', section='副歌一 · 你说', k0=7, k1=11, tr='wipe',
         scene='回忆：淡紫放射光背景，飘着几颗小星星；他站在中间',
         action='他（3/4）收到那条粉围巾，举起来看了看，说话',
         events=[(7, '礼物盒弹开，他拎出粉围巾'), (8, '气泡「示例？」'), (9, '他歪头，表情变平'), (10, '气泡「示例一啦」，围巾垂下')],
         camera='中近景', tone='回忆 · 淡紫'),
    dict(id='S04', section='副歌一 · 示例歌词', k0=11, k1=15, tr='pop',
         scene='黄色条纹墙前一台体重秤，旁边站着她',
         action='她把一颗毛线织的大爱心放上秤，指针一路打到底，盖章「示例」',
         events=[(11, '爱心落到秤上（「示」）'), (12, '指针甩到红区'), (13, '红章「示例」砸下（「示例」）'), (14, '爱心泄气变小，她冒汗')],
         camera='中景', tone='明亮漫画色'),
    dict(id='S05', section='间奏 · 示例', k0=15, k1=19, tr='cut',
         scene='雨夜商店街（远景）：店招、遮阳棚、橱窗、路灯、湿地倒影',
         action='她没打伞，拖着长长的毛线往前走，一拍一步；最后一步踩进水坑',
         events=[(15, '走第一步'), (16, '毛线勾住路灯'), (17, '回头一扯（「示例」）'), (18, '水坑溅起，浇她一身')],
         camera='远景横移跟拍', tone='雨夜 · 冷蓝 + 店招暖光'),
    dict(id='S06', section='断鼓段 · 示例', k0=19, k1=23, tr='cut',
         scene='灰蓝竖条纹背景，只有她头顶一朵小乌云在下雨，地上一摊水',
         action='她坐在地上，湿透，身上缠着毛线；小乌云只追着她下',
         events=[(19, '「示例」字章砸下（鼓停）'), (20, '小乌云打个小闪电'), (21, '一滴水从小花上滴下，水面一圈涟漪'), (22, '「啊嚏」')],
         camera='中景，固定', tone='冷灰蓝'),
    dict(id='S07', section='断鼓段 · 示例', k0=23, k1=27, tr='wipe',
         scene='橙黄放射光背景，她坐在越堆越高的围巾山上，头顶挂着长度牌',
         action='她低头猛织，围巾一拍长一截，长度牌一拍翻一次',
         events=[(23, '「示例」字章，长度牌 1 米'), (24, '翻到 10 米'), (25, '翻到 99 米'), (26, '翻到 999 米，围巾山塌一角')],
         camera='中景，缓慢后拉', tone='暖黄漫画色'),
    dict(id='S08', section='断鼓段 · 示例歌词', k0=27, k1=31, tr='pop',
         scene='夜晚公园草地，路灯一盏；一块他的等身纸板立牌（背后有木撑）',
         action='她把 999 米的围巾一圈圈绕到纸板他身上，靠上去；风一吹，纸板翻过去露出空白背面',
         events=[(27, '绕第一圈'), (28, '「示例歌词」字章，绕第二圈'), (29, '她靠上去冒爱心'), (30, '风吹，纸板翻面，只剩背面的木撑')],
         camera='中景', tone='夜 · 深蓝 + 路灯'),
    dict(id='S09', section='断鼓段 · 蓄力', k0=31, k1=35, tr='iris',
         scene='粉色桌面俯视：礼物盒',
         action='围巾叠好放进盒子，一拍一步包好，越推越近',
         events=[(31, '围巾落进盒子'), (32, '盖上盒盖'), (33, '系上丝带（「示例」）'), (34, '贴上标签「给你♥」')],
         camera='俯拍，按拍推近（蓄力）', tone='粉色'),
    dict(id='S10', section='鼓回来 · 示例歌词内', k0=35, k1=39, tr='flash',
         scene='粉色放射光大背景，爱心乱飞',
         action='她（正面）把礼物高高举起，往前递',
         events=[(35, '白闪，她弹进画面举起礼物（鼓回来）'), (36, '爱心炸开（「示例」）'), (37, '她蹦一下'), (38, '再递近一点，眼睛变成爱心')],
         camera='中景，每拍推', tone='高饱和粉'),
    dict(id='S11', section='示例歌词内 · 最后', k0=39, k1=43, tr='wipe',
         scene='夜里公园长椅，路灯、树、远处城市灯火；一条长长的粉围巾同时绕着两个人的脖子',
         action='两人并排坐（3/4 相对），围巾连着两人；他站起来，围巾从他脖子上滑下，他走出画面，她手里只剩空着的一头',
         events=[(39, '两人坐着，围巾连成一道弧'), (40, '弧上冒小爱心（「示例」）'), (41, '他站起，围巾滑落'), (42, '他走出画面，空的一头落在椅子上（「最后」）')],
         camera='中景，固定', tone='夜 · 深蓝 + 路灯暖光'),
    dict(id='S12', section='示例歌词内容', k0=43, k1=47, tr='cut',
         scene='回到她的卧室（与 S02 同一构图），床头柜闹钟放大在右边',
         action='她抱着那条围巾坐在床上，睁着眼；闹钟一拍跳一格',
         events=[(43, '04:00'), (44, '04:30'), (45, '05:00，「失眠」字章'), (46, '05:30')],
         camera='中景', tone='夜 · 靛蓝 + 台灯暖黄'),
    dict(id='S13', section='示例歌词内', k0=47, k1=51, tr='cut',
         scene='公寓楼外立面，满墙窗户，有几扇还亮着；中间是她亮着暖灯的窗，她坐在窗后',
         action='别的窗一拍熄一扇，只剩她的',
         events=[(47, '熄一扇'), (48, '熄一扇'), (49, '熄两扇（「示例」）'), (50, '最后一扇熄灭（「示例一」）')],
         camera='中景，缓慢后拉', tone='深夜 · 深靛'),
    dict(id='S14', section='示例 一句', k0=51, k1=55, tr='cut',
         scene='窗台近景（室内）：窗外黑夜和月亮；窗台上一个烟灰缸，里面一根他留下示例还在冒烟，旁边一个打火机和围巾的一头',
         action='烟一拍升起一圈，越来越多',
         events=[(51, '黑夜里只剩这扇窗的光（「示」）'), (52, '第一缕烟升起'), (53, '烟圈'), (54, '烟越聚越多')],
         camera='近景，缓慢推近', tone='深夜 · 冷蓝 + 烟灰'),
    dict(id='S15', section='示例歌词', k0=55, k1=59, tr='cut',
         scene='同一扇窗：烟在玻璃前聚成他的轮廓',
         action='烟里的他出现、看着她；她（正面，左边）伸手，一碰烟就散成一圈圈',
         events=[(55, '烟聚成他的轮廓（「示例」）'), (56, '烟里的他眨眼'), (57, '她伸手（「示例」）'), (58, '烟散开')],
         camera='近景', tone='深夜 · 冷蓝 + 烟灰'),
    dict(id='S16', section='尾 · 示例歌词', k0=59, k1='END', tr='cut',
         scene='公寓楼外景（S13 同一面墙）：整面楼都黑了，只有她的窗亮着，烟往月亮飘',
         action='她的灯一拍拍暗下去，最后一拍熄灭；黑窗里亮起两个小白点——她还睁着眼',
         events=[(59, '烟飘向月亮'), (60, '月亮被烟遮住一半'), (61, '她的灯闪一下'), (62, '灯灭，黑窗里两个小眼睛眨一下')],
         camera='远景，缓慢后拉，结尾淡黑', tone='深夜'),
]


def kt(k):
    if k == 'START':
        return 0.0
    if k == 'END':
        return DUR
    return B[k]


def barOf(k):
    if k in ('START', 'END'):
        return '—'
    return f'{(k - 3) // 4 + 1}.{(k - 3) % 4 + 1}'


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
    for s in SHOTS:
        a, b = kt(s['k0']), kt(s['k1'])
        d = dict(s)
        d.update(start=round(a, 3), end=round(b, 3), dur=round(b - a, 3), bar0=barOf(s['k0']), sung=sungIn(a, b),
                 events=[dict(k=k, t=round(B[k], 3), bar=barOf(k), what=w) for k, w in s['events']],
                 prompt=STYLE + s['scene'] + '。' + s['action'] + '。')
        out.append(d)
    sb = dict(song='失眠', artist='Suki刘舒妤', clip='DJ 版片段 · 示例歌词内容示例 → 示例歌词内容', dur=DUR, bpm=round(BJ['bpm'], 2),
              beat=BJ['beat'], beats=B, breakdown=BREAK, shots=out)
    json.dump(sb, open(os.path.join(R, 'data', 'storyboard.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(R, 'out'), exist_ok=True)
    with open(os.path.join(R, 'out', '失眠_MV_分镜表.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['镜号', '段落', '起', '止', '时长', '起始小节', '唱到', '画面', '动作', '逐拍事件', '镜头', '转场', '色调', '生成提示词'])
        for d in out:
            ev = '；'.join(f"{e['bar']} {e['t']:.2f}s {e['what']}" for e in d['events'])
            w.writerow([d['id'], d['section'], f"{d['start']:.2f}", f"{d['end']:.2f}", f"{d['dur']:.2f}", d['bar0'], d['sung'], d['scene'], d['action'],
                        ev, d['camera'], d['tr'], d['tone'], d['prompt']])
    return sb


if __name__ == '__main__':
    sb = build()
    for d in sb['shots']:
        print(d['id'], f"{d['start']:6.2f}-{d['end']:6.2f}", d['tr'], d['sung'])
