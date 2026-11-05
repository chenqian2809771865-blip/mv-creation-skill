# 《小酒窝》男女主像素小人（约 42px 高，2.3 头身），正/侧/背三视角
# 他：格纹礼帽、黑发斜刘海、紫蓝格子衬衫、黑白红格纹马甲、紫白蓝条纹领结（取自专辑封面造型）
# 她：栗色及肩发、齐刘海、珊瑚红蝴蝶结、长睫毛、笑时有小酒窝、白衬衫+粉色背带裙、红鞋
import functools, math
from PIL import Image, ImageDraw
from px import OUT, outline_rgba

HIM = dict(
    skin=(242, 201, 168), skin_d=(214, 156, 128), blush=(240, 150, 142),
    hair=(40, 30, 32), hair_h=(84, 62, 58),
    hat=(124, 116, 108), hat_d=(86, 80, 76), band=(52, 44, 48), hat_r=(178, 62, 76), hat_l=(200, 194, 186),
    shirt=(70, 60, 142), shirt_d=(46, 40, 102), shirt_m=(190, 72, 136), shirt_b=(100, 136, 226),
    vest=(48, 48, 60), vest_d=(32, 32, 42), vest_w=(150, 150, 166), vest_r=(196, 54, 70),
    bow1=(106, 68, 176), bow2=(240, 240, 250), bow3=(148, 206, 246),
    pants=(48, 48, 66), pants_d=(34, 34, 48), shoe=(72, 48, 42), sole=(232, 228, 220),
)
HER = dict(
    skin=(248, 212, 184), skin_d=(226, 168, 140), blush=(244, 150, 150), dimple=(214, 108, 118),
    hair=(102, 58, 44), hair_h=(150, 92, 64), hair_d=(72, 40, 34),
    ribbon=(238, 80, 100), ribbon_d=(186, 48, 74),
    blouse=(250, 246, 240), blouse_d=(212, 204, 200),
    dress=(242, 150, 180), dress_d=(204, 104, 140), dress_l=(252, 192, 210),
    sock=(250, 250, 252), shoe=(208, 62, 76),
)
EYE = (36, 28, 42)
MOUTH = (150, 56, 70)
TONGUE = (236, 110, 120)
WHITE = (255, 255, 255)
GREY_H = (184, 184, 194)
GREY_HH = (214, 214, 222)

SW, SH = 48, 64          # 精灵画布
AX, AY = 24, 61          # 脚底锚点（像素坐标）


class P:
    """以脚底为原点、y 向上的绘制器"""
    def __init__(self):
        self.im = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def r(self, x0, y0, x1, y1, c):
        if c is None: return
        xa, xb = sorted((x0, x1)); ya, yb = sorted((y0, y1))
        self.d.rectangle([AX + xa, AY - yb, AX + xb, AY - ya], fill=c)

    def p(self, x, y, c):
        if c is None: return
        self.d.point((AX + x, AY - y), fill=c)

    def rows(self, y0, spans, c):
        """spans: [(xa, xb), ...] 依次对应 y0, y0+1, ..."""
        for i, (a, b) in enumerate(spans):
            if a is not None: self.r(a, y0 + i, b, y0 + i, c)

    def line(self, x0, y0, x1, y1, c, w=2):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
            self.r(x - (w - 1) // 2, y - (w - 1) // 2, x + w // 2, y + w // 2, c)


HEAD_ROWS_F = [(-6, 6), (-8, 8)] + [(-9, 9)] * 14 + [(-8, 8), (-6, 6)]   # 18 行
HEAD_ROWS_S = [(-5, 6), (-7, 8)] + [(-8, 9)] * 14 + [(-7, 8), (-5, 6)]


def _arm(p, sx, sy, hx, hy, sleeve, skin, ex=None, ey=None):
    if ex is None: ex, ey = (sx + hx) / 2, (sy + hy) / 2
    p.line(sx, sy, round(ex), round(ey), sleeve, 2)
    p.line(round(ex), round(ey), hx, hy, sleeve, 2)
    p.r(hx, hy, hx + 1, hy + 1, skin)


def _hand_pos(state, side, view, ph, hy0):
    """返回 (手 x, 手 y, 肘)"""
    s = -1 if side == 'L' else 1
    if view == 'side':
        if state == 'swing':
            return round(-4 * math.sin(2 * math.pi * ph) * (1 if side == 'R' else -1)), hy0 - 8, None
        if state == 'phone': return 5, hy0 - 4, (2, hy0 - 6)
        if state == 'forward': return 11, hy0 - 2, None
        if state == 'up': return 6, hy0 + 11, None
        if state == 'hat': return 7, hy0 + 14, (5, hy0 + 3)
        if state == 'umbrella': return 6, hy0 + 1, (3, hy0 - 4)
        if state == 'chin': return 7, hy0 + 1, (5, hy0 - 6)
        if state == 'hold': return 3, hy0 - 5, None
        if state == 'hug': return 4, hy0 - 4, (3, hy0 - 6)
        return 0, hy0 - 8, None
    # 正面/背面
    if state == 'down': return s * 8 - (1 if s > 0 else 0), hy0 - 9, None
    if state == 'phone': return (-3 if s < 0 else 1), hy0 - 6, (s * 7, hy0 - 7)
    if state == 'up': return s * 11 - (1 if s > 0 else 0), hy0 + 10, (s * 10, hy0 + 3)
    if state == 'out': return s * 14 - (1 if s > 0 else 0), hy0 + 1, (s * 11, hy0 - 2)
    if state == 'hug': return (5 if s < 0 else -6), hy0 - 4, (s * 8, hy0 - 6)
    if state == 'hat': return s * 6 - (1 if s > 0 else 0), hy0 + 14, (s * 10, hy0 + 6)
    if state == 'wave':
        return s * 12 - (1 if s > 0 else 0), hy0 + 9 + round(2 * math.sin(ph * 2 * math.pi)), (s * 10, hy0 + 2)
    if state == 'cheek': return s * 8 - (1 if s > 0 else 0), hy0 + 4, (s * 10, hy0 - 4)
    if state == 'peace': return s * 11 - (1 if s > 0 else 0), hy0 + 12, (s * 11, hy0 + 3)
    if state == 'chin': return (-1 if s < 0 else 0), hy0 + 1, (s * 6, hy0 - 6)
    if state == 'umbrella': return (-2 if s < 0 else 1), hy0 - 1, (s * 7, hy0 - 6)
    if state == 'hold': return s * 5 - (1 if s > 0 else 0), hy0 - 6, (s * 8, hy0 - 6)
    if state == 'hip': return s * 9 - (1 if s > 0 else 0), hy0 - 7, (s * 11, hy0 - 4)
    return s * 8, hy0 - 9, None


@functools.lru_cache(maxsize=4096)
def sprite(who, view='front', ph=None, arms=('down', 'down'), eyes='open', mouth='smile',
           blush=False, dimple=False, hat=True, aged=False, sweat=False, sit=False, bob=0,
           hatcol=None, wet=False, lookdown=False, head_only=False, pal=None, look=0):
    """返回 RGBA 精灵；锚点 (AX, AY) 为脚底中心。side 视角朝右。"""
    C = dict(HIM if who == 'him' else HER)
    if pal: C.update(dict(pal))
    if aged:
        C['hair'], C['hair_h'], C['hair_d'] = GREY_H, GREY_HH, (150, 150, 162)
    if wet:
        for k in ('shirt', 'vest', 'pants', 'dress', 'blouse'):
            if k in C: C[k] = tuple(int(v * .82) for v in C[k])
    p = P()
    walking = ph is not None
    swing = math.sin(2 * math.pi * ph) if walking else 0
    up = (1 if walking and abs(swing) < .5 else 0) + bob
    hip = 8 if who == 'him' else 7
    if sit: up -= 3
    # ---------------- legs ----------------
    if not head_only:
        _legs(p, C, who, view, swing if walking else 0, walking, sit, up)
    top = (20 if who == 'him' else 19) + up      # 躯干顶 y
    hy0 = top                                      # 肩高
    # back arm (侧面在身体后)
    if not head_only and view == 'side':
        hx, hy, el = _hand_pos(arms[0], 'L', 'side', (ph or 0) + .5, hy0)
        _arm(p, -1, hy0 - 1, hx - 1, hy, C['shirt_d'] if who == 'him' else C['blouse_d'], C['skin_d'],
             *(el if el else (None, None)))
    if not head_only:
        _torso(p, C, who, view, up, aged)
    # long hair behind (她)
    head_y = top + 1
    if who == 'her' and not aged:
        _her_back_hair(p, C, view, head_y)
    # arms
    if not head_only:
        if view == 'side':
            hx, hy, el = _hand_pos(arms[1], 'R', 'side', ph or 0, hy0)
            _arm(p, 0, hy0 - 1, hx, hy, C['shirt'] if who == 'him' else C['blouse'], C['skin'],
                 *(el if el else (None, None)))
        else:
            for i, side in enumerate(('L', 'R')):
                st = arms[i]
                hx, hy, el = _hand_pos(st, side, view, ph or 0, hy0)
                sx = -7 if side == 'L' else 7
                _arm(p, sx, hy0 - 1, hx, hy, C['shirt'] if who == 'him' else C['blouse'], C['skin'],
                     *(el if el else (None, None)))
                if who == 'him':   # 袖子格纹
                    pass
            if 'phone' in arms and view == 'front':
                p.r(-2, hy0 - 7, 2, hy0 - 3, (34, 34, 44)); p.r(-1, hy0 - 6, 1, hy0 - 4, (64, 64, 80))
    # ---------------- head ----------------
    _head(p, C, who, view, head_y, eyes, mouth, blush, dimple, hat, aged, lookdown, look)
    if sweat:
        x = 10 if view != 'side' else -6
        p.r(x, head_y + 12, x + 1, head_y + 14, (150, 210, 255)); p.p(x, head_y + 15, (150, 210, 255))
    im = outline_rgba(p.im)
    # front-arm-on-top details survive outline; add tiny phone screen glow on side view
    if 'phone' in arms and view == 'side' and not head_only:
        hx, hy, _ = _hand_pos('phone', 'R', 'side', 0, hy0)
        d = ImageDraw.Draw(im)
        d.rectangle([AX + hx + 1, AY - hy - 4, AX + hx + 2, AY - hy], fill=(34, 34, 44))
        d.point((AX + hx + 1, AY - hy - 3), fill=(170, 220, 255))
    return im


def _legs(p, C, who, view, swing, walking, sit, up):
    him = who == 'him'
    pants = C['pants'] if him else C['skin']
    pd = C['pants_d'] if him else C['skin_d']
    shoe = C['shoe']
    if view == 'side':
        if sit:
            hipy = 5 + 3 + up
            # thigh 水平向右，小腿下垂
            p.r(-2, hipy - 2, 6, hipy, C['pants'] if him else C['dress_d'])
            if not him: p.r(-2, hipy - 2, 6, hipy - 1, C['skin'])
            p.r(4, 2, 6, hipy - 2, pants if him else C['skin'])
            if not him: p.r(4, 2, 6, 3, C['sock'])
            p.r(4, 0, 8, 1, shoe);
            if him: p.r(4, 0, 8, 0, C['sole'])
            return
        for k, sgn in ((0, -1), (1, 1)):   # 0 = 后腿
            fx = round(sgn * 3 * swing)
            lift = 1 if walking and (sgn * swing) < -.3 else 0
            col = pd if k == 0 else pants
            for y in range(2, 9 + up):
                x = round(fx + (0 - fx) * (y - 2) / (6 + up))
                p.r(x - 1, y + lift * (y < 4), x + 1, y + lift * (y < 4), col)
            if not him:
                p.r(fx - 1, 2 + lift, fx + 1, 4 + lift, C['sock'])
            p.r(fx - 1, lift, fx + 3, 1 + lift, shoe if k else tuple(int(v * .8) for v in shoe))
            if him: p.r(fx - 1, lift, fx + 3, lift, C['sole'])
        return
    # front / back
    if sit:
        if him:
            p.r(-5, 3, 5, 5, C['pants_d']); p.r(-4, 4, 4, 5, C['pants'])
            p.r(-4, 0, -2, 3, C['pants']); p.r(2, 0, 4, 3, C['pants'])
            p.r(-5, 0, -1, 0, C['shoe']); p.r(1, 0, 5, 0, C['shoe'])
        else:
            p.r(-4, 1, -2, 4, C['skin']); p.r(2, 1, 4, 4, C['skin'])
            p.r(-4, 1, -2, 2, C['sock']); p.r(2, 1, 4, 2, C['sock'])
            p.r(-5, 0, -1, 0, C['shoe']); p.r(1, 0, 5, 0, C['shoe'])
        return
    l1 = 1 if walking and swing > .3 else 0
    l2 = 1 if walking and swing < -.3 else 0
    if him:
        p.r(-4, 3 + l1, -1, 8 + up, pants); p.r(1, 3 + l2, 4, 8 + up, pants)
        p.r(-4, 7 + up, 4, 8 + up, pants)
        p.r(-5, l1, -1, 2 + l1, shoe); p.r(-5, l1, -1, l1, C['sole'])
        p.r(1, l2, 5, 2 + l2, shoe); p.r(1, l2, 5, l2, C['sole'])
    else:
        p.r(-3, 2 + l1, -1, 7 + up, C['skin']); p.r(1, 2 + l2, 3, 7 + up, C['skin'])
        p.r(-3, 2 + l1, -1, 4 + l1, C['sock']); p.r(1, 2 + l2, 3, 4 + l2, C['sock'])
        p.r(-4, l1, -1, 1 + l1, shoe); p.r(1, l2, 4, 1 + l2, shoe)


def _torso(p, C, who, view, up, aged):
    if who == 'him':
        b = 9 + up; t = 20 + up
        if view == 'side':
            p.r(-5, b, 5, t, C['shirt'])
            p.r(-4, b, 4, t - 1, C['vest'])
            p.r(3, b + 6, 4, t - 1, C['shirt'])            # 开襟处衬衫
            for y in (b + 3, b + 7): p.r(-4, y, 2, y, C['vest_w'])
            p.r(-1, b, -1, t - 1, C['vest_w']); p.p(-1, b + 5, C['vest_r'])
            p.r(4, t - 1, 6, t, C['bow1']); p.p(5, t, C['bow2']); p.p(6, t - 1, C['bow3'])
            return
        if view == 'back':
            p.r(-6, b, 6, t, C['shirt'])
            p.r(-5, b, 5, t - 1, C['vest_d'])
            p.r(-2, b + 2, 2, b + 2, (70, 70, 84))
            return
        p.r(-6, b, 6, t, C['shirt'])
        p.r(-6, b, 6, t - 1, C['vest'])
        p.p(0, b, C['shirt'])                               # 马甲下摆凹口
        for y in range(b + 6, t): p.r(-(y - b - 5), y, (y - b - 5), y, C['shirt'])  # V 领
        for x in (-4, 4): p.r(x, b, x, t - 1, C['vest_w'])
        for y in (b + 3,): p.r(-6, y, 6, y, C['vest_w'])
        for (x, y) in ((-4, b + 3), (4, b + 3)): p.p(x, y, C['vest_r'])
        p.p(-2, b + 1, C['vest_r']); p.p(2, b + 1, C['vest_r'])
        p.p(0, b + 2, C['vest_w']); p.p(0, b + 4, C['vest_w'])  # 纽扣
        # 领结
        p.r(-3, t - 1, -1, t, C['bow1']); p.r(1, t - 1, 3, t, C['bow1'])
        p.p(-2, t - 1, C['bow2']); p.p(2, t - 1, C['bow2']); p.p(-3, t, C['bow3']); p.p(3, t, C['bow3'])
        p.r(0, t - 1, 0, t, C['bow3'])
    else:
        b = 8 + up; t = 19 + up
        if view == 'side':
            spans = [(-6, 6), (-6, 6), (-5, 5), (-5, 5), (-5, 5), (-4, 5), (-4, 4), (-4, 4)]
            p.rows(b, spans, C['dress'])
            p.r(-6, b, 6, b, C['dress_d'])
            p.r(-4, b + 8, 4, t, C['blouse'])
            p.r(-1, b + 8, 3, t - 1, C['dress'])
            p.r(2, t - 1, 4, t, C['blouse']); p.p(4, t - 1, C['ribbon'])
            return
        spans = [(-7, 7), (-7, 7), (-6, 6), (-6, 6), (-6, 6), (-6, 6), (-5, 5), (-5, 5)]
        p.rows(b, spans, C['dress'])
        p.r(-7, b, 7, b, C['dress_d'])
        for x in (-5, -1, 3): p.p(x, b + 1, C['dress_l'])
        p.r(-5, b + 8, 5, t, C['blouse'])
        if view == 'back':
            p.r(-5, b + 8, 5, t - 1, C['blouse_d']); p.r(-3, b + 8, -2, t - 1, C['dress']); p.r(2, b + 8, 3, t - 1, C['dress'])
            return
        p.r(-3, b + 8, 3, t - 2, C['dress'])
        p.r(-3, t - 2, -2, t - 1, C['dress']); p.r(2, t - 2, 3, t - 1, C['dress'])   # 背带
        p.r(-3, t, 3, t, C['blouse']); p.p(-1, t - 1, C['blouse']); p.p(1, t - 1, C['blouse'])
        p.p(0, t - 1, C['ribbon']); p.p(-1, t, C['ribbon']); p.p(1, t, C['ribbon'])
        p.r(-1, b + 4, 1, b + 5, C['dress_l'])                                            # 口袋


def _her_back_hair(p, C, view, hy):
    if view == 'side':
        p.rows(hy - 6, [(-9, -1), (-10, 0), (-10, 0), (-10, 1), (-10, 1), (-10, 1)], C['hair_d'])
        p.r(-10, hy, 1, hy + 8, C['hair_d'])
    elif view == 'back':
        p.rows(hy - 6, [(-8, 8), (-9, 9), (-10, 10), (-10, 10), (-10, 10), (-10, 10)], C['hair'])
        p.r(-10, hy, 10, hy + 8, C['hair'])
    else:
        p.rows(hy - 6, [(-9, -7), (-10, -7), (-10, -7), (-10, -7), (-10, -7), (-10, -7)], C['hair_d'])
        p.rows(hy - 6, [(7, 9), (7, 10), (7, 10), (7, 10), (7, 10), (7, 10)], C['hair_d'])
        p.r(-10, hy, -8, hy + 8, C['hair_d']); p.r(8, hy, 10, hy + 8, C['hair_d'])


def _head(p, C, who, view, y0, eyes, mouth, blush, dimple, hat, aged, lookdown, look=0):
    him = who == 'him'
    rows = HEAD_ROWS_S if view == 'side' else HEAD_ROWS_F
    if view == 'back':
        p.rows(y0, rows, C['hair'])
        if him:
            p.r(-2, y0, 2, y0 + 1, C['skin_d'])      # 后颈
            for x in (-5, 0, 4): p.r(x, y0 + 4, x, y0 + 10, C['hair_h'])
        else:
            for x in (-5, -1, 4): p.r(x, y0 + 3, x, y0 + 14, C['hair_h'])
            if aged: _bun(p, C, 'back', y0)
            else: _ribbon(p, C, -3, y0 + 16)
        if him and hat: _hat(p, C, 'front', y0)
        return
    p.rows(y0, rows, C['skin'])
    side = view == 'side'
    ly = -1 if lookdown else 0
    if him:
        if side:
            p.rows(y0 + 6, [(-8, 1), (-8, 1), (-8, 2), (-8, 3), (-8, 4)], C['hair'])
            p.rows(y0 + 11, [(-8, 9), (-7, 8), (-5, 6)], C['hair'])
            p.r(-8, y0 + 2, -4, y0 + 6, C['hair'])
            p.r(-1, y0 + 4, 0, y0 + 6, C['skin']); p.p(0, y0 + 5, C['skin_d'])   # 耳朵
            p.r(5, y0 + 9, 9, y0 + 10, C['hair']); p.p(9, y0 + 8, C['hair'])   # 刘海
            p.r(-6, y0 + 13, -1, y0 + 13, C['hair_h'])
            p.p(10, y0 + 4, C['skin'])                                         # 鼻
        else:
            p.rows(y0 + 9, [(-9, -7), (-9, -2), (-9, 5), (-9, 9), (-8, 8), (-6, 6)], C['hair'])
            p.r(7, y0 + 9, 9, y0 + 11, C['hair'])
            p.r(-9, y0 + 4, -8, y0 + 9, C['hair']); p.r(8, y0 + 4, 9, y0 + 9, C['hair'])
            p.r(-5, y0 + 12, 0, y0 + 12, C['hair_h']); p.r(2, y0 + 13, 5, y0 + 13, C['hair_h'])
    else:
        if aged:
            if side:
                p.rows(y0 + 7, [(-8, 0), (-8, 1), (-8, 3), (-8, 8), (-8, 9), (-8, 9), (-8, 9), (-8, 9), (-8, 9), (-7, 8), (-5, 6), (-3, 4)], C['hair'])
                p.r(-8, y0 + 2, -5, y0 + 7, C['hair'])
            else:
                p.rows(y0 + 9, [(-9, 9), (-9, 9), (-9, 9), (-9, 9), (-9, 9), (-9, 9), (-9, 9), (-8, 8), (-6, 6), (-4, 4)], C['hair'])
                p.r(-9, y0 + 3, -8, y0 + 9, C['hair']); p.r(8, y0 + 3, 9, y0 + 9, C['hair'])
                for x in (-6, -2, 2, 6): p.p(x, y0 + 9, C['skin'])
            _bun(p, C, view, y0)
        elif side:
            p.rows(y0 + 6, [(-8, 1), (-8, 1), (-8, 2), (-8, 3), (-8, 9)], C['hair'])
            p.rows(y0 + 11, [(-8, 9), (-8, 9), (-8, 9), (-8, 9), (-8, 9), (-7, 8), (-5, 6), (-3, 4)], C['hair'])
            p.r(-8, y0 + 1, -4, y0 + 6, C['hair'])
            p.p(8, y0 + 9, C['skin']); p.p(5, y0 + 10, C['skin'])
            p.r(-5, y0 + 14, 0, y0 + 14, C['hair_h'])
            p.p(10, y0 + 4, C['skin'])
            _ribbon(p, C, -4, y0 + 15)
        else:
            p.rows(y0 + 10, [(-9, 9), (-9, 9), (-9, 9), (-9, 9), (-9, 9), (-9, 9), (-8, 8), (-6, 6), (-4, 4)], C['hair'])
            for x in (-6, -2, 3, 6): p.p(x, y0 + 10, C['skin'])          # 齐刘海碎缝
            p.r(-9, y0 + 1, -8, y0 + 10, C['hair']); p.r(8, y0 + 1, 9, y0 + 10, C['hair'])
            p.r(-4, y0 + 14, 1, y0 + 14, C['hair_h']); p.r(3, y0 + 13, 5, y0 + 13, C['hair_h'])
            _ribbon(p, C, 5, y0 + 16)
    # ---- face ----
    ey = y0 + 4 + ly
    if side:
        xs = [5]
    else:
        xs = [-5, 3] if him else [-5, 3]
    for i, ex in enumerate(xs):
        _eye(p, ex + look, ey, eyes, him, side, i, C)
    my = y0 + 1 + (0 if not lookdown else 0)
    mx = 7 if side else 0
    _mouth(p, mx, my, mouth, side)
    if blush or dimple:
        if side:
            p.r(4, y0 + 2, 5, y0 + 2, C['blush'])
        else:
            p.r(-8, y0 + 2, -7, y0 + 2, C['blush']); p.r(6, y0 + 2, 7, y0 + 2, C['blush'])
    if dimple and not him:
        if side: p.p(6, y0 + 1, C['dimple'])
        else: p.p(-3, y0 + 1, C['dimple']); p.p(3, y0 + 1, C['dimple'])
    if aged and not side:
        p.p(-7, y0 + 4, C['skin_d']); p.p(7, y0 + 4, C['skin_d'])
    if aged and him and not side:      # 圆眼镜
        g = (90, 80, 70)
        for ex in (-5, 3):
            p.r(ex - 1, ey - 1, ex + 2, ey - 1, g); p.r(ex - 1, ey + 3, ex + 2, ey + 3, g)
            p.r(ex - 1, ey - 1, ex - 1, ey + 3, g); p.r(ex + 2, ey - 1, ex + 2, ey + 3, g)
        p.r(0, ey + 2, 1, ey + 2, g)
    if him and hat:
        _hat(p, C, 'side' if side else 'front', y0)
    elif him:   # 不戴帽：补头顶头发
        if side:
            p.rows(y0 + 11, [(-8, 9)] * 5 + [(-7, 8), (-5, 6), (-3, 4)], C['hair'])
            p.r(-4, y0 + 16, 2, y0 + 16, C['hair_h'])
        else:
            p.rows(y0 + 12, [(-9, 9)] * 4 + [(-8, 8), (-6, 6), (-4, 4)], C['hair'])
            p.r(-5, y0 + 16, -1, y0 + 16, C['hair_h']); p.r(2, y0 + 15, 5, y0 + 15, C['hair_h'])


def _eye(p, x, y, kind, him, side, i, C):
    if kind == 'closed':
        p.r(x, y + 1, x + 1, y + 1, EYE)
        if not him: p.p(x + (2 if (side or i == 1) else -1), y + 2, EYE)
        return
    if kind == 'happy':   # ^ ^
        p.p(x, y + 1, EYE); p.p(x + 1, y + 2, EYE); p.p(x + 2 if not side else x + 2, y + 1, EYE) if not him else p.p(x + 1, y + 2, EYE)
        if him: p.p(x - 0, y + 1, EYE); p.p(x + 1, y + 1, EYE)
        if not him: p.p(x + (3 if (side or i == 1) else -1), y + 2, EYE)
        return
    if kind == 'heart':
        hc = (236, 60, 90)
        p.r(x - 1, y + 1, x + 2, y + 2, hc); p.r(x, y, x + 1, y, hc); p.p(x - 1, y + 3, hc); p.p(x + 2, y + 3, hc)
        return
    if kind == 'dizzy':
        p.r(x - 1, y, x + 2, y, EYE); p.r(x - 1, y + 3, x + 2, y + 3, EYE); p.p(x - 1, y + 1, EYE); p.p(x + 2, y + 2, EYE); p.p(x + 1, y + 1, EYE)
        return
    if kind == 'wide':
        p.r(x, y - 1, x + 1, y + 3, EYE); p.p(x, y + 3, WHITE); p.p(x + 1, y + 2, WHITE)
        if not him: _lash(p, x, y, side, i)
        return
    if kind == 'sad':
        p.r(x, y, x + 1, y + 2, EYE); p.p(x, y + 2, WHITE)
        p.p(x + (0 if i == 0 else 1), y + 4, EYE); p.p(x + (1 if i == 0 else 0), y + 3, EYE)
        if not him: _lash(p, x, y, side, i)
        return
    if kind == 'down':
        p.r(x, y, x + 1, y + 1, EYE)
        p.r(x - (0 if him else 1), y + 2, x + (1 if him else 2), y + 2, EYE)
        return
    # open
    if him:
        p.r(x, y, x + 1, y + 2, EYE); p.p(x + 1, y + 2, WHITE)
    else:
        p.r(x, y, x + 1, y + 2, EYE); p.p(x + 1, y + 2, WHITE); p.p(x, y, (110, 60, 70))
        _lash(p, x, y, side, i)


def _lash(p, x, y, side, i):
    # 长睫毛：上眼睑横出一格并上翘
    if side or i == 1:
        p.r(x, y + 3, x + 2, y + 3, EYE); p.p(x + 3, y + 4, EYE); p.p(x + 2, y + 2, EYE)
    else:
        p.r(x - 1, y + 3, x + 1, y + 3, EYE); p.p(x - 2, y + 4, EYE); p.p(x - 1, y + 2, EYE)


def _mouth(p, x, y, kind, side):
    if kind == 'none': return
    if side:
        if kind in ('open', 'laugh', 'o', 'sneeze'):
            p.r(x, y - 1, x + 1, y, MOUTH); p.p(x + 1, y - 1, TONGUE); return
        if kind == 'sad': p.p(x, y - 1, MOUTH); return
        if kind == 'smile': p.p(x, y, (196, 96, 100)); return
        p.p(x, y, (176, 88, 96)); return
    if kind == 'smile':
        p.r(-1, y - 1, 1, y - 1, MOUTH); p.p(-2, y, MOUTH); p.p(2, y, MOUTH)
    elif kind in ('open', 'laugh'):
        p.r(-2, y - 1, 2, y, MOUTH); p.r(-1, y - 2, 1, y - 2, MOUTH); p.r(-1, y - 2, 0, y - 2, TONGUE)
        p.r(-1, y, 1, y, (250, 250, 250))
    elif kind == 'o':
        p.r(-1, y - 2, 0, y, MOUTH); p.p(-1, y - 1, TONGUE)
    elif kind == 'sneeze':
        p.r(-2, y - 2, 2, y, MOUTH); p.r(-1, y - 2, 1, y - 1, TONGUE)
    elif kind == 'sad':
        p.r(-1, y, 1, y, MOUTH); p.p(-2, y - 1, MOUTH); p.p(2, y - 1, MOUTH)
    elif kind == 'wavy':
        p.p(-2, y, MOUTH); p.p(-1, y - 1, MOUTH); p.p(0, y, MOUTH); p.p(1, y - 1, MOUTH); p.p(2, y, MOUTH)
    elif kind == 'cat':   # ω
        p.p(-2, y, MOUTH); p.p(-1, y - 1, MOUTH); p.p(0, y, MOUTH); p.p(1, y - 1, MOUTH); p.p(2, y, MOUTH)
    else:
        p.r(-1, y, 1, y, MOUTH)


def _ribbon(p, C, x, y):
    p.r(x, y, x + 1, y + 2, C['ribbon']); p.r(x + 3, y, x + 4, y + 2, C['ribbon'])
    p.r(x + 2, y + 1, x + 2, y + 1, C['ribbon_d']); p.p(x, y, C['ribbon_d']); p.p(x + 4, y, C['ribbon_d'])


def _bun(p, C, view, y0):
    if view == 'side':
        p.r(-7, y0 + 15, -2, y0 + 19, C['hair']); p.r(-6, y0 + 19, -3, y0 + 20, C['hair'])
        _ribbon(p, C, -7, y0 + 14)
    else:
        p.r(-3, y0 + 17, 3, y0 + 21, C['hair']); p.r(-2, y0 + 21, 2, y0 + 22, C['hair'])
        _ribbon(p, C, 4, y0 + 15)


def _hat(p, C, view, y0):
    b = y0 + 12
    if view == 'side':
        p.r(-11, b, 13, b + 1, C['hat_d']); p.r(-10, b + 1, 12, b + 1, C['hat'])
        p.r(-7, b + 2, 7, b + 7, C['hat']); p.r(-6, b + 8, -1, b + 8, C['hat']); p.r(1, b + 8, 6, b + 8, C['hat'])
        p.r(-7, b + 2, 7, b + 3, C['band'])
        for x in (-4, 1, 5): p.r(x, b + 4, x, b + 7, C['hat_r'])
        p.r(-7, b + 6, 7, b + 6, C['hat_l'])
        return
    p.r(-12, b, 12, b + 1, C['hat_d']); p.r(-11, b + 1, 11, b + 1, C['hat'])
    p.r(-8, b + 2, 8, b + 7, C['hat']); p.r(-7, b + 8, -2, b + 8, C['hat']); p.r(2, b + 8, 7, b + 8, C['hat'])
    p.r(-8, b + 2, 8, b + 3, C['band'])
    for x in (-5, 0, 5): p.r(x, b + 4, x, b + 7, C['hat_r'])
    p.r(-8, b + 6, 8, b + 6, C['hat_l'])
    p.p(-1, b + 7, C['hat_d']); p.p(1, b + 7, C['hat_d'])


def blink(t, seed=0, period=3.7):
    ph = (t + seed * 1.37) % period
    return ph < .11


def draw(base, who, x, y, flip=False, light=None, rim=None, **kw):
    """把角色以脚底 (x,y) 贴到 base（PIL RGB）。light 为乘色。"""
    from px import tint
    im = sprite(who, **kw)
    if light is not None:
        im = tint(im, light)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    base.paste(im, (int(round(x - AX)) if not flip else int(round(x - (SW - 1 - AX))), int(round(y - AY))), im)
    return im


# ---------------- NPC ----------------
NPC_HAIR = [(40, 30, 32), (90, 60, 40), (150, 110, 70), (60, 50, 70), (120, 70, 50), (30, 30, 40)]
NPC_TOP = [(90, 140, 110), (200, 120, 80), (110, 120, 180), (180, 160, 110), (150, 90, 120), (90, 110, 130), (220, 200, 160)]
NPC_DRESS = [(140, 190, 230), (250, 210, 120), (170, 220, 170), (220, 170, 220), (240, 160, 130), (200, 200, 210)]

def npc_pal(kind, seed):
    import random
    r = random.Random(seed)
    hc = r.choice(NPC_HAIR)
    if kind == 'm':
        top = r.choice(NPC_TOP); dk = tuple(int(v * .72) for v in top)
        pants = r.choice([(50, 50, 70), (70, 60, 50), (90, 100, 120), (40, 40, 44)])
        return tuple(dict(hair=hc, hair_h=tuple(min(255, v + 30) for v in hc), shirt=top, shirt_d=dk, vest=top, vest_d=dk,
                          vest_w=top, vest_r=top, bow1=top, bow2=top, bow3=top, pants=pants, pants_d=tuple(int(v * .75) for v in pants),
                          shoe=(60, 50, 50)).items())
    dc = r.choice(NPC_DRESS)
    return tuple(dict(hair=hc, hair_h=tuple(min(255, v + 40) for v in hc), hair_d=tuple(int(v * .8) for v in hc), dress=dc,
                      dress_d=tuple(int(v * .78) for v in dc), dress_l=tuple(min(255, v + 25) for v in dc),
                      ribbon=r.choice([(250, 250, 250), (90, 90, 120), dc]), ribbon_d=tuple(int(v * .7) for v in dc),
                      shoe=r.choice([(60, 50, 50), (240, 240, 240), (120, 80, 60)])).items())


def npc(base, kind, seed, x, y, flip=False, light=None, **kw):
    who = 'him' if kind == 'm' else 'her'
    kw.setdefault('hat', False)
    return draw(base, who, x, y, flip=flip, light=light, pal=npc_pal(kind, seed), **kw)


# ---------------- 橘猫 ----------------
@functools.lru_cache(maxsize=64)
def cat_sprite(pose='sit', blink_=False, tail=0):
    im = Image.new('RGBA', (24, 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    o, o2, w_ = (240, 160, 80), (210, 120, 60), (255, 240, 220)
    if pose == 'sit':
        d.ellipse([6, 8, 17, 19], fill=o); d.rectangle([8, 15, 15, 19], fill=o)
        d.rectangle([9, 14, 14, 19], fill=w_)
        d.ellipse([7, 1, 17, 10], fill=o)
        d.polygon([(7, 4), (8, 0), (11, 2)], fill=o); d.polygon([(17, 4), (16, 0), (13, 2)], fill=o)
        if blink_: d.line([(9, 5), (10, 5)], fill=OUT); d.line([(14, 5), (15, 5)], fill=OUT)
        else: d.rectangle([9, 4, 10, 6], fill=OUT); d.rectangle([14, 4, 15, 6], fill=OUT)
        d.point((12, 7), fill=(220, 90, 100))
        for i in range(3): d.point((9 + i * 2, 1 + 0), fill=o2)
        tx = 18 + tail
        d.line([(16, 17), (19, 16), (20 + tail, 12)], fill=o, width=2)
    elif pose == 'jump':
        d.ellipse([4, 7, 19, 14], fill=o); d.ellipse([15, 3, 23, 11], fill=o)
        d.polygon([(16, 5), (17, 0), (19, 3)], fill=o); d.polygon([(22, 5), (22, 0), (20, 3)], fill=o)
        d.line([(5, 12), (1, 16)], fill=o, width=2); d.line([(17, 12), (21, 17)], fill=o, width=2)
        d.line([(5, 9), (0, 5)], fill=o, width=2)
        d.point((18, 6), fill=OUT); d.point((21, 6), fill=OUT)
    elif pose == 'curl':
        d.ellipse([3, 9, 21, 19], fill=o); d.ellipse([12, 6, 21, 15], fill=o)
        d.polygon([(13, 8), (14, 4), (16, 7)], fill=o); d.polygon([(20, 8), (20, 4), (18, 7)], fill=o)
        d.line([(15, 11), (16, 11)], fill=OUT); d.line([(18, 11), (19, 11)], fill=OUT)
        d.line([(3, 16), (12, 18)], fill=o2)
    return outline_rgba(im)


def cat(base, x, y, pose='sit', flip=False, blink_=False, tail=0, light=None):
    """(x,y) 为底边中心"""
    from px import tint
    im = cat_sprite(pose, blink_, tail)
    if light is not None: im = tint(im, light)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    base.paste(im, (int(x - 12), int(y - 20)), im)
