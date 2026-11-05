# -*- coding: utf-8 -*-
"""Phone chat UI, lock screen, title card, karaoke lyrics and VCR overlays (all on the 320x180 grid)."""
import math
import numpy as np
from px import Cv, hx, mix, text, text_w, text_big, glyph, bayer, W, H, OUT, seg, clamp, ease, ease_out
from chars import emote, PICK

THEMES = {
    'dark': dict(bg=hx('#171a26'), bar=hx('#1f2333'), line=hx('#2c3246'), her=hx('#363d52'), her_t=hx('#eef0f6'),
                 me=hx('#3b6aa8'), me_t=hx('#f4f8ff'), sys=hx('#7a8098'), name=hx('#eef0f6'), input=hx('#262b3c'),
                 input_t=hx('#eef0f6'), btn=hx('#3b6aa8'), btn_off=hx('#2e3446'), border=hx('#0e1018')),
    'old': dict(bg=hx('#efe2c2'), bar=hx('#e2cfa6'), line=hx('#cdb88c'), her=hx('#fffaf0'), her_t=hx('#4a3a30'),
                me=hx('#f2b27c'), me_t=hx('#4a2a1c'), sys=hx('#9a8462'), name=hx('#4a3a30'), input=hx('#f8efd8'),
                input_t=hx('#4a3a30'), btn=hx('#e08a54'), btn_off=hx('#d8c6a0'), border=hx('#8a7454')),
}
HEART = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
HEART_L = [".##.", "####", "####", ".###", "..##", "...#"]
HEART_R = ["##.", "###", "###", "##.", "#..", "..."]
BIG = {  # 5x7 digits for lock screen
    '0': ["#####", "#...#", "#...#", "#...#", "#...#", "#...#", "#####"], '1': ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    '2': ["#####", "....#", "....#", "#####", "#....", "#....", "#####"], '3': ["#####", "....#", "....#", ".####", "....#", "....#", "#####"],
    '4': ["#...#", "#...#", "#...#", "#####", "....#", "....#", "....#"], '5': ["#####", "#....", "#....", "#####", "....#", "....#", "#####"],
    '6': ["#####", "#....", "#....", "#####", "#...#", "#...#", "#####"], '7': ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    '8': ["#####", "#...#", "#...#", "#####", "#...#", "#...#", "#####"], '9': ["#####", "#...#", "#...#", "#####", "....#", "....#", "#####"],
    ':': [".", "#", "#", ".", "#", "#", "."],
}


from ui_tiny import TINY, pix, tiny


def rrect(c, x, y, w, h, col, border=None, r=2):
    x, y, w, h = int(x), int(y), int(w), int(h)
    if border is not None:
        c.rect(x + r - 1, y - 1, w - 2 * r + 2, h + 2, border)
        c.rect(x - 1, y + r - 1, w + 2, h - 2 * r + 2, border)
        if r >= 2:
            c.rect(x, y, w, h, border)
    c.rect(x + r, y, w - 2 * r, h, col)
    c.rect(x, y + r, w, h - 2 * r, col)
    if r >= 2:
        c.rect(x + 1, y + 1, w - 2, h - 2, col)


def avatar(c, x, y, who='she'):
    if who == 'she':
        c.rect(x, y, 10, 10, hx('#f6c2a0'))
        c.rect(x, y, 10, 4, hx('#6b3d2b')); c.rect(x, y, 2, 9, hx('#6b3d2b')); c.rect(x + 8, y, 2, 9, hx('#6b3d2b'))
        c.px(x + 3, y + 5, OUT); c.px(x + 6, y + 5, OUT); c.rect(x + 2, y + 9, 6, 1, hx('#cc3b42'))
    else:
        c.rect(x, y, 10, 10, hx('#f2c9a8'))
        c.rect(x, y, 10, 4, hx('#2c2536')); c.rect(x, y, 1, 7, hx('#2c2536')); c.rect(x + 9, y, 1, 7, hx('#2c2536'))
        c.px(x + 3, y + 5, OUT); c.px(x + 6, y + 5, OUT); c.rect(x + 1, y + 9, 8, 1, hx('#3b5b98'))


# ---------------------------------------------------------------- little pictures for image bubbles
def _pic(kind):
    def f(c, x, y, w=40, h=30):
        from props import mini_pic
        c.paste(mini_pic(kind, w, h), x, y)
        c.rect(x, y, w, 1, (255, 255, 255)); c.rect(x, y + h - 1, w, 1, (255, 255, 255))
        c.rect(x, y, 1, h, (255, 255, 255)); c.rect(x + w - 1, y, 1, h, (255, 255, 255))
    return f


PICS = {k: _pic(k) for k in ('umbrella', 'candy', 'book', 'read', 'store', 'roof')}


# ---------------------------------------------------------------- chat screen
def wrap(s, maxw, font='w'):
    lines, cur = [], ''
    for ch in s:
        if ch == '\n':
            lines.append(cur); cur = ''
            continue
        if text_w(cur + ch, font) > maxw and cur and ch not in '，。？！、…》）':
            lines.append(cur); cur = ch
        else:
            cur += ch
    lines.append(cur)
    return lines


def msg_size(m, maxw):
    """returns (w,h) of a message block."""
    k = m['k']
    if k in ('date', 'sys'):
        return 0, 14
    if k == 'pic':
        return 46, 36
    if k == 'voice':
        th = 0
        if m.get('trans') and m.get('trans_n', 0) > 0:
            th = 4 + 13 * len(wrap(m['trans'][:m['trans_n']], maxw - 8, 'w')) + 5
        return 64, 22 + th
    lines = m['text'].split('\n')
    tw = max(text_w(l) for l in lines)
    return tw + 8, 17 * len(lines) + 5


def draw_chat(c, x0, y0, sw, sh, msgs, theme='dark', header='她', typing=False, heart=1.0, input_text='', cursor=True,
              t=0.0, read_idx=None, scroll=0, clock='23:41', top_y=None, glow=None, voice_p=None, pop=None, other='she',
              glitch_idx=None):
    """draw a chat app into screen rect (x0,y0,sw,sh). msgs: list of dicts k in her/me/date/sys/pic/voice.
    pop: dict idx->scale progress 0..1 for the pop-in of the newest bubbles."""
    T = THEMES[theme]
    scr = Cv(sw, sh, T['bg'])
    # status bar
    scr.rect(0, 0, sw, 9, T['bar'])
    tiny(scr, 4, 2, clock, T['name'])
    for i in range(4):
        scr.rect(sw - 30 + i * 3, 6 - i, 2, i + 1, T['name'])
    scr.rect(sw - 15, 2, 10, 5, T['name']); scr.rect(sw - 14, 3, 6, 3, T['bar']); scr.rect(sw - 5, 3, 1, 3, T['name'])
    # header
    scr.rect(0, 9, sw, 20, T['bar'])
    scr.rect(0, 29, sw, 1, T['line'])
    pix(scr, ["..#", ".#.", "#..", ".#.", "..#"], 5, 16, T['name'])
    if typing:
        s = '对方正在输入' + '.' * (1 + int(t * 6) % 3)
        text(scr, (sw - text_w('对方正在输入...', 'w')) // 2, 13, s, T['name'], font='w')
    else:
        nw = text_w(header)
        nx = (sw - nw - 10) // 2
        text(scr, nx, 11, header, T['name'])
        if heart > 0:
            if heart >= 1.0:
                pix(scr, HEART, nx + nw + 3, 16, hx('#e84a5f'))
            else:  # breaking: halves drift apart and fall
                p = 1 - heart
                pix(scr, HEART_L, nx + nw + 3 - int(p * 3), 16 + int(p * p * 10), hx('#e84a5f'))
                pix(scr, HEART_R, nx + nw + 7 + int(p * 3), 16 + int(p * p * 12), hx('#e84a5f'))
                scr.vline(nx + nw + 6, 16, 21, T['bar'])
    # input bar
    iy = sh - 22
    scr.rect(0, iy - 2, sw, 24, T['bar'])
    scr.rect(0, iy - 2, sw, 1, T['line'])
    rrect(scr, 5, iy + 1, sw - 40, 18, T['input'], r=3)
    if input_text:
        tw = text_w(input_text)
        tx = 9 if tw < sw - 52 else 9 - (tw - (sw - 52))
        sub = Cv(sw - 48, 18, T['input'])
        text(sub, tx - 5, 1, input_text, T['input_t'])
        c_x = tx - 5 + tw + 1
        if cursor and int(t * 2.5) % 2 == 0:
            sub.rect(c_x, 2, 1, 15, T['input_t'])
        scr.paste(sub, 9, iy + 1)
    elif cursor and int(t * 2.5) % 2 == 0:
        scr.rect(10, iy + 3, 1, 14, T['input_t'])
    on = bool(input_text)
    rrect(scr, sw - 32, iy + 2, 28, 16, T['btn'] if on else T['btn_off'], r=3)
    text(scr, sw - 30, iy + 4, '发送', (255, 255, 255) if on else T['sys'], font='w')
    # messages bottom-up
    top = 31
    bottom = iy - 5 + scroll
    maxw = sw - 40
    y = bottom
    layout = []
    for i in range(len(msgs) - 1, -1, -1):
        m = msgs[i]
        w_, h_ = msg_size(m, maxw)
        extra = 12 if (read_idx is not None and i == read_idx) else 0
        y -= h_ + extra
        layout.append((i, y, w_, h_))
        y -= 4
        if y < top - 200:
            break
    area = Cv(sw, iy - 3 - top, T['bg'])
    for (i, yy, w_, h_) in layout:
        m = msgs[i]
        yy -= top
        k = m['k']
        sc = 1.0
        if pop and i in pop:
            sc = pop[i]
            if sc <= 0:
                continue
        if k == 'date':
            s = m['text']
            text(area, (sw - text_w(s, 'w')) // 2, yy + 1, s, T['sys'], font='w')
        elif k == 'sys':
            s = m['text']
            tw = text_w(s, 'w')
            rrect(area, (sw - tw) // 2 - 4, yy, tw + 8, 13, mix(T['bg'], T['sys'], 0.18), r=2)
            text(area, (sw - tw) // 2, yy + 1, s, T['sys'], font='w')
        else:
            mine = m.get('me', k == 'me')
            if k in ('her',):
                mine = False
            bx = sw - 5 - w_ if mine else 18
            if not mine:
                avatar(area, 4, yy, other)
            bcol = T['me'] if mine else T['her']
            tcol = T['me_t'] if mine else T['her_t']
            if sc < 1.0:
                # pop: grow from the side
                ww = max(4, int(w_ * ease_out(sc)))
                hh = max(4, int(h_ * ease_out(sc)))
                bx2 = (sw - 5 - ww) if mine else 18
                rrect(area, bx2, yy + (h_ - hh), ww, hh, bcol, r=3)
                continue
            if glow is not None and i == glow[0]:
                g = glow[1]
                rrect(area, bx - 2, yy - 2, w_ + 4, h_ + 4, mix(bcol, (255, 240, 200), 0.5 * g), r=4)
            bh_ = 22 if k == 'voice' else h_
            rrect(area, bx, yy, w_, bh_, bcol, r=3)
            # tail
            if mine:
                area.rect(bx + w_, yy + 5, 2, 2, bcol)
            else:
                area.rect(bx - 2, yy + 5, 2, 2, bcol)
            if k == 'voice' and m.get('trans') and m.get('trans_n', 0) > 0:
                lines = wrap(m['trans'][:m['trans_n']], maxw - 8, 'w')
                tw = max(text_w(l, 'w') for l in lines) + 8
                tx = sw - 5 - tw if mine else 18
                rrect(area, tx, yy + 26, tw, 13 * len(lines) + 5, T['her'], r=3)
                for j, ln in enumerate(lines):
                    text(area, tx + 4, yy + 28 + 13 * j, ln, T['her_t'], font='w')
            if k in ('her', 'me'):
                for j, ln in enumerate(m['text'].split('\n')):
                    text(area, bx + 4, yy + 2 + 17 * j, ln, tcol)
                if glitch_idx is not None and i == glitch_idx[0]:
                    rr = np.random.default_rng(int(glitch_idx[1] * 1000))
                    for q in range(6):
                        gy = yy + int(rr.integers(0, max(1, h_)))
                        sh = int(rr.integers(-8, 9))
                        area.a[gy:gy + 2] = np.roll(area.a[gy:gy + 2], sh, axis=1)
            elif k == 'pic':
                PICS[m['pic']](area, bx + 3, yy + 3)
            elif k == 'voice':
                area.rect(bx + 5, yy + 6, 1, 9, tcol)
                pix(area, ["#..", "##.", "###", "##.", "#.."], bx + 6, yy + 8, tcol)
                n = 9
                for b in range(n):
                    hgt = [3, 6, 9, 5, 8, 4, 7, 3, 5][b]
                    if voice_p is not None and voice_p > 0:
                        hgt = int(hgt * (0.5 + 0.5 * abs(math.sin(t * 9 + b * 1.7)))) + 1
                        colb = hx('#f6d27a') if b / n < voice_p else tcol
                    else:
                        colb = tcol
                    area.rect(bx + 14 + b * 3, yy + 11 - hgt // 2, 2, hgt, colb)
                text(area, bx + 44, yy + 6, m.get('dur', '0:08'), tcol, font='w')
        if read_idx is not None and i == read_idx:
            s = m.get('read', '已读')
            text(area, sw - 5 - text_w(s, 'w'), yy + h_ + 1, s, T['sys'], font='w')
    scr.paste(area, 0, top)
    c.paste(scr, x0, y0)


def phone_body(c, x, y, w, h, col=hx('#1b1824'), edge=hx('#3a3648')):
    """bezel around a screen rect (x,y,w,h); extends beyond frame as needed."""
    c.rect(x - 5, y - 8, w + 10, h + 16, col)
    c.rect(x - 5, y - 8, 1, h + 16, edge)
    c.rect(x + w + 4, y - 8, 1, h + 16, mix(edge, (0, 0, 0), 0.4))
    c.rect(x + w + 5, y + 20, 1, 14, edge)


# ---------------------------------------------------------------- lock screen
def big_digits(c, x, y, s, col, k=3):
    for ch in s:
        rows = BIG[ch]
        pix(c, rows, x, y, col, k)
        x += (len(rows[0]) + 1) * k
    return x


def wallpaper_umbrella(scr, t, warm=False):
    """photo-like wallpaper: the two under her red umbrella on a rainy night street."""
    from px import vgrad
    from scenes import rain, buildings, umbrella, RED_UMB, glow
    from chars import chibi, blit_chibi
    sw, sh = scr.w, scr.h
    vgrad(scr, 0, sh, [hx('#10142c'), hx('#1a1e3e'), hx('#262a50'), hx('#30345a')])
    buildings(scr, int(sh * 0.72), 5, hx('#14172e'), win=hx('#e8b868'), lit=0.3, x1=sw, hmin=20, hmax=70)
    r = np.random.default_rng(8)
    yy, xx = np.mgrid[0:sh, 0:sw]
    for i in range(9):
        bx, by, br = r.uniform(0, sw), r.uniform(10, sh * 0.6), r.uniform(5, 12)
        m = ((xx - bx) ** 2 + (yy - by) ** 2 < br * br) & (bayer(sh, sw) < 0.4)
        scr.a[m] = [hx('#e8b868'), hx('#ffd68a'), hx('#c87a5a')][i % 3]
    scr.rect(0, int(sh * 0.72), sw, sh, hx('#22243a'))
    for x in range(0, sw, 9):
        scr.rect(x, int(sh * 0.72) + 14, 5, 1, hx('#3a3c54'))
    cx, fy = sw // 2, int(sh * 0.72) + 22
    blit_chibi(scr, chibi('he', 'front', 'stand', eyes='smile', mouth='smile', look=1), cx - 8, fy)
    blit_chibi(scr, chibi('she', 'front', 'stand', eyes='smile', mouth='smile', arm='up', look=-1), cx + 8, fy)
    umbrella(scr, cx + 15, fy - 26, *RED_UMB, open_=1.0, w=44, tilt=-14, shaft=16)
    rain(scr, t, 45, 77, speed=200, wind=-30, length=6, col=hx('#5a6a9a'), area=(0, 0, sw, sh))
    scr.a[:] = (scr.a.astype(np.float32) * 0.82).astype(np.uint8)


def lock_screen(c, x0, y0, sw, sh, t, clock='23:17', date='10月25日 星期日', wall='umbrella', notes=(), note_p=1.0, dim=0.0,
                dismiss=0.0, empty_text=None):
    from px import vgrad
    from scenes import rain, glass_rain, buildings, glow
    from props import mini_pic
    scr = Cv(sw, sh)
    if wall == 'umbrella':
        wallpaper_umbrella(scr, t)
    else:  # dawn after rain
        vgrad(scr, 0, sh, [hx('#3a4a7a'), hx('#6a6a9a'), hx('#b08aa8'), hx('#f0b48a'), hx('#fde0b0')])
        scr.ellipse(sw * 0.7, sh * 0.72, 10, 10, hx('#fff0c8'))
        buildings(scr, sh, 21, hx('#4a3e5e'), win=hx('#f6d090'), lit=0.06, x1=sw, hmin=14, hmax=44)
        buildings(scr, sh, 22, hx('#5e4e6a'), win=None, x1=sw, hmin=6, hmax=24)
    big_digits(scr, (sw - (4 * 18 + 6)) // 2, 24, clock, (246, 244, 240), 3)
    text(scr, (sw - text_w(date, 'w')) // 2, 50, date, (236, 236, 244), font='w')
    ny = 72
    for i, (title, body) in enumerate(notes):
        p = clamp(note_p)
        if p <= 0:
            continue
        yy = ny + i * 34 - int((1 - ease_out(p)) * 30)
        xo = -int(ease(dismiss) * (sw + 10))
        if xo < -sw:
            continue
        sub = Cv(sw, 32, alpha=True)
        rrect(sub, 6, 1, sw - 12, 30, hx('#2a2a3c') + (255,), border=hx('#121220') + (255,), r=3)
        rrect(sub, 10, 5, 10, 10, hx('#58b06a') + (255,), r=2)
        sub.rect(12, 8, 6, 4, (255, 255, 255, 255)); sub.px(13, 12, (255, 255, 255, 255))
        text(sub, 24, 4, title, (240, 240, 246, 255), font='w')
        if body.startswith('♥'):
            pix(sub, HEART, 10, 19, hx('#e84a5f') + (255,))
            text(sub, 20, 17, body[1:].strip(), (200, 204, 220, 255), font='w')
        else:
            text(sub, 10, 17, body, (200, 204, 220, 255), font='w')
        scr.blit(sub, xo, yy - 1)
    if empty_text:
        text(scr, (sw - text_w(empty_text, 'w')) // 2, 84, empty_text, (236, 236, 244), font='w')
    # bottom bar
    scr.rect(sw // 2 - 14, sh - 6, 28, 2, (236, 236, 244))
    if dim > 0:
        m = bayer(sh, sw) < dim
        scr.a[m] = (0, 0, 0)
    c.paste(scr, x0, y0)


# ---------------------------------------------------------------- karaoke lyrics
def karaoke(c, t, line, y=158, lead=0.083, col=hx('#f6f2e8'), sung=hx('#f39a4a'), outline_col=OUT, alpha=1.0):
    a, b, s, opt = line
    ct = opt['ct']
    n = sum(1 for v in ct if t + lead >= v)
    tw = text_w(s)
    x = (W - tw) // 2
    if alpha < 1.0:
        sub = Cv(W, 20, alpha=True)
        text(sub, x, 2, s, sung + (255,), outline_col=outline_col + (255,), col2=col + (255,), split=n)
        # swap: sung first chars -> sung color
        m = sub.a[..., 3] > 0
        m &= bayer(20, W, 0, y - 2) < alpha
        c.a[y - 2:y + 18][m] = sub.a[..., :3][m]
    else:
        text(c, x, y, s, sung, outline_col=outline_col, col2=col, split=n)


# ---------------------------------------------------------------- VCR overlay
def vcr(c, t, label='◀◀ x8', stamp=None, noise=0.0, seed=0, blink=True, col=(246, 240, 230)):
    if label and (not blink or int(t * 3) % 2 == 0):
        x = 8
        if label.startswith('◀◀'):
            pix(c, ["...#...#", "..##..##", ".###.###", "########", ".###.###", "..##..##", "...#...#"], x, 8, col)
            text(c, x + 12, 6, label[2:].strip(), col, font='w', outline_col=OUT)
        elif label.startswith('▶▶'):
            pix(c, ["#...#...", "##..##..", "###.###.", "########", "###.###.", "##..##..", "#...#..."], x, 8, col)
            text(c, x + 12, 6, label[2:].strip(), col, font='w', outline_col=OUT)
        else:
            text(c, x, 6, label, col, font='w', outline_col=OUT)
    if stamp:
        tw = len(stamp) * 4
        tiny(c, W - 8 - tw + 1, H - 13 + 1, stamp, (40, 20, 10))
        tiny(c, W - 8 - tw, H - 13, stamp, hx('#f2b040'))
    if noise > 0:
        r = np.random.default_rng(int(t * 24) + seed)
        nb = int(1 + noise * 4)
        for i in range(nb):
            y = int((t * 90 + i * 53 + r.integers(0, 40)) % H)
            hgt = int(r.integers(1, 4))
            sh = int(r.integers(-6, 7) * noise)
            band = c.a[y:y + hgt].copy()
            c.a[y:y + hgt] = np.roll(band, sh, axis=1)
            if r.random() < 0.6:
                xs = r.integers(0, W, int(20 * noise))
                for xx in xs:
                    c.a[y, xx] = (230, 230, 240)


def title_card(c, t, t0, t1=5.34):
    """keyhole beam with dust, title lands on t0, artist types in from t1."""
    from px import vgrad
    from scenes import dust
    vgrad(c, 0, H, [hx('#07070d'), hx('#0c0b14'), hx('#14111c'), hx('#1c1622')])
    p = t - t0
    # beam from a keyhole at top-left, widening toward bottom-right
    kx, ky = 60, 22
    br = ease_out(seg(p, 0.0, 0.25)) * (0.8 + 0.2 * ease(seg(t, t1, t1 + 0.3)))
    beam = Cv(W, H, alpha=True)
    beam.poly([(kx - 2, ky), (kx + 3, ky), (W + 40, H + 10), (W - 150, H + 10)], (255, 255, 255))
    bm = beam.a[..., 3] > 0
    yy, xx = np.mgrid[0:H, 0:W]
    fall = np.clip(1 - np.sqrt((xx - kx) ** 2 + (yy - ky) ** 2) / 330, 0, 1)
    m = bm & (bayer() < fall * 0.55 * br)
    c.a[m] = (np.array(c.a[m], np.float32) * 0.5 + np.array([200, 170, 110]) * 0.5).astype(np.uint8)
    # keyhole plate
    c.rect(kx - 8, ky - 10, 18, 22, hx('#5a4a2a')); c.rect(kx - 8, ky - 10, 18, 1, hx('#8a7040'))
    c.rect(kx - 1, ky - 5, 4, 4, hx('#fff2c8') if br > 0.2 else hx('#100c10')); c.rect(kx, ky - 1, 2, 6, hx('#fff2c8') if br > 0.2 else hx('#100c10'))
    dust(c, t, 70, 41, area=(0, 0, W, H), col=hx('#f6e6c0'), speed=2.5, beam=bm)
    k = 4
    s = '半岛铁盒'
    gw = 16 * k * len(s)
    x = (W - gw) // 2 + 20
    land = ease_out(p / 0.16)
    y = 52 - int((1 - land) * 8)
    shake = int(round(math.sin(p * 70) * 2 * max(0, 1 - p / 0.3))) if p > 0.1 else 0
    text_big(c, x + 3 + shake, y + 3, s, hx('#3a2a1a'), k=k)
    text_big(c, x + shake, y, s, hx('#f4ead6'), k=k, outline_col=OUT)
    if t >= t1:
        q = t - t1
        wl = int(ease_out(seg(q, 0.0, 0.4)) * 120)
        c.rect(x + gw - 120, y + 16 * k + 6, wl, 2, hx('#cc3b42'))
        s2 = '周杰伦'
        text(c, x + gw - text_w(s2), y + 16 * k + 12, s2, hx('#f4ead6'), outline_col=OUT, upto=int(q / 0.07) + 1)
        if q > 0.5:
            s3 = 'Jay Chou · 八度空间'
            text(c, x + gw - text_w(s3, 'w'), y + 16 * k + 32, s3, hx('#b8a890'), font='w')
