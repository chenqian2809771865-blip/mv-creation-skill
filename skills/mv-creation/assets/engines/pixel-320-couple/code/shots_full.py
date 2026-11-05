# -*- coding: utf-8 -*-
"""《晴天》正片 S02–S31。t = 音频时间（渲染器已加 2 帧提前量）。"""
import math
import numpy as np
from px import (Cv, hx, mix, W, H, OUT, vgrad, bayer, text, text_w, seg, ease, ease_out, ease_in, clamp, grade_ice, vignette,
                light, silhouette, upscale, grade_warm, dither_blend)
from chars import chibi, blit_chibi, emote, blink, bust, P, TEAR
from scenes import rain, splashes, ripples, glass_rain, lamp, glow, umbrella, RED_UMB, cloud_sprite, light_cone
from shots import shot, lit, upk, up2, memory_post, bokeh_bg, rain_shadows
from story import EV as E
from scenes_qt import (shade, flash_env, shake, forecast_screen, tv_room_static, tv_body, tv_glass_off, TV, classroom_static,
                       yard_static, swing, tree, petals, SWING, eaves_static, roof_drip, EAVES_Y, BB, gate2_static, GB,
                       GATE_FEET, storm_sky)
from scenes_full import (board_static, BOARD, desk_row, desk_top, note_paper, sleeve_hand, fog_window, flower_bottle,
                         music_sheet, staff, note_head, guitar, rainbow, puddle, CHALK, CHALK_Y, GRAPHITE, draw_hands)
from shots_open import hand_pos, swing_angle, screen_now
import lyr
from lyr import L, write, progress, text_mask

STAMP = '2003.07.31'
STAMP_RAIN = '2003.06.18'


def mem(c, t, stamp=STAMP, k=0.3):
    return memory_post(c, t, stamp=stamp, k=k, dust_n=8, vig=0.2)


def flashes(t, ts, dur=0.25):
    return max([flash_env(t, x, dur) for x in ts] + [0.0])


def dark(c, Lk, base=(0.42, 0.45, 0.68), top=1.3):
    k = tuple(base[i] + (top - base[i]) * Lk for i in range(3))
    return shade(c, k)


def sunny_windows(c, t):
    for j, wx in enumerate((20, 120, 220)):
        sub = Cv(80, 86)
        vgrad(sub, 0, 86, [hx('#5aa0e6'), hx('#7ab8ee'), hx('#a8d6f6'), hx('#d0eaf8')])
        cs = cloud_sprite(40, 16, 60 + j, hx('#ffffff'), hx('#ffffff'), hx('#dce8f4'))
        sub.blit(cs, int((j * 30 + t * 4) % 120) - 40, 8 + j * 5)
        for i in range(3):
            sub.ellipse(10 + i * 30 + 3 * math.sin(t * 1.3 + i), 78, 18, 12, hx('#5aa04a') if i % 2 else hx('#4a8a3a'))
        c.paste(sub, wx, 21)
        c.rect(wx + 39, 21, 3, 86, hx('#e8e0cc')); c.rect(wx, 62, 80, 2, hx('#e8e0cc'))
    # sun patches on the floor
    for wx in (20, 120, 220):
        pts = [(wx + 10, 136), (wx + 74, 136), (wx + 104, 180), (wx + 34, 180)]
        m = Cv(W, H, alpha=True); m.poly(pts, (255, 255, 255))
        mm = (m.a[..., 3] > 0) & (bayer() < 0.5)
        c.a[mm] = np.clip(c.a[mm].astype(np.float32) * 1.12 + 18, 0, 255).astype(np.uint8)


# ================================================================ S02 deskmates
@shot('class_pair')
def class_pair(t):
    c = classroom_static().copy()
    sunny_windows(c, t)
    poke = 21.30 <= t < 21.75
    she = chibi('she', 'front', 'stand', eyes='smile' if t > 22.9 else ('closed' if blink(t, 3) else 'open'),
                mouth='smile' if (poke or t > 22.9) else 'line')
    he_eyes = 'wide' if poke or 21.75 <= t < 22.0 else ('down' if t > 22.9 else ('closed' if blink(t, 1) else 'open'))
    he = chibi('he', 'front', 'stand', eyes=he_eyes, mouth='o' if poke else 'line')
    blit_chibi(c, lit(she, 'day'), 140 + (3 if poke else 0), 160)
    blit_chibi(c, lit(he, 'day'), 182 - (1 if poke else 0), 160)
    # double desk
    c.rect(112, 146, 98, 4, hx('#c89a5a')); c.rect(112, 150, 98, 18, hx('#8a6234')); c.rect(112, 146, 98, 1, hx('#e0b47a'))
    c.rect(116, 168, 3, 10, hx('#4a4a54')); c.rect(203, 168, 3, 10, hx('#4a4a54'))
    # books on the desk
    c.rect(118, 142, 14, 4, hx('#3a6aa8')); c.rect(190, 142, 12, 4, hx('#e86a6a'))
    if poke:
        c.line(148, 136, 172, 132, hx('#f2c84a'))
        e = emote('excl', hx('#e84a5f')); c.blit(e, 186, 100)
    # the folded note slides across
    q = ease_out(seg(t, 22.6, 22.95))
    if t >= 22.6:
        nx = 146 + 26 * q
        c.rect(nx, 143, 8, 4, hx('#fbf6ea')); c.rect(nx, 143, 8, 1, hx('#ffffff')); c.px(nx + 4, 144, hx('#d8d0c0'))
    if t > 23.3:
        e = emote('heart', hx('#e84a5f')); c.blit(e, 132, 100 - (1 if int(t * 4) % 2 else 0))
    c = upk(c, 162, 126, 2)
    return mem(c, t)


# ================================================================ S03 the doodle note
@shot('note_doodle')
def note_doodle(t):
    c = Cv(160, 90)
    desk_top(c, t)
    u = seg(t, 24.55, 24.95)
    x0, y0, ww, hh = note_paper(c, 80, 44, 112, 62, unfold=u)
    if u >= 1:
        dq = seg(t, 25.0, 26.6)
        # sun
        if dq > 0:
            c.ellipse(x0 + 22, y0 + 20, 7, 7, hx('#ffb52a')) if dq > 0.1 else None
            for i in range(int(8 * min(1, dq * 2.5))):
                a = i * math.pi / 4
                c.line(x0 + 22 + math.cos(a) * 9, y0 + 20 + math.sin(a) * 9, x0 + 22 + math.cos(a) * 12, y0 + 20 + math.sin(a) * 12, hx('#ffb52a'))
        # two little figures
        for k, (fx, col) in enumerate(((x0 + 56, hx('#3b5b98')), (x0 + 72, hx('#cc3b42')))):
            if dq > 0.4 + k * 0.2:
                c.ellipse(fx, y0 + 30, 3, 3, GRAPHITE); c.ellipse(fx, y0 + 30, 2, 2, hx('#fbf6ea'))
                c.line(fx, y0 + 33, fx, y0 + 42, GRAPHITE); c.line(fx - 4, y0 + 37, fx + 4, y0 + 37, GRAPHITE)
                c.line(fx, y0 + 42, fx - 3, y0 + 48, GRAPHITE); c.line(fx, y0 + 42, fx + 3, y0 + 48, GRAPHITE)
                c.rect(fx - 2, y0 + 34, 4, 1, col)
        if dq > 0.85:  # holding hands
            c.line(x0 + 60, y0 + 37, x0 + 68, y0 + 37, GRAPHITE)
        if dq >= 1 and t > 26.0:
            for i in range(3):
                a = t * 3 + i * 2.1
                c.px(x0 + 64 + math.cos(a) * 12, y0 + 24 + math.sin(a) * 6, hx('#ffffff'))
    # his hands holding the note edges
    sleeve_hand(c, x0 + 2, y0 + hh - 4, 'he', ang=30, L=40)
    sleeve_hand(c, x0 + ww - 2, y0 + hh - 4, 'he', ang=-30, L=40)
    return mem(up2(c), t)


# ================================================================ S04 walking out together
@shot('yard_walk')
def yard_walk(t):
    c, skym = yard_static('sun')
    c = c.copy()
    sun_sky(c, skym, t)
    tree(c, 172, 128, t, sway=math.sin(t * 1.5) * 1.5, S=True, seed=3, h=60)
    tree(c, 222, 128, t, sway=math.sin(t * 1.5 + 1) * 1.5, S=True, seed=4, h=70)
    swing(c, t, 6 * math.sin(t * 2), S=True)
    q = t - 27.81
    hx_ = 70 + 18 * q
    she_run = 28.4 <= t < 29.4
    if t < 28.4:
        sx = hx_ + 14 + 18 * q * 0
        sx = 84 + 18 * q
    elif t < 29.4:
        sx = 84 + 18 * 0.59 + 60 * (t - 28.4)
    else:
        sx = 84 + 18 * 0.59 + 60
    turned = t >= 29.4
    she = chibi('she', 'side', 'run' if she_run else ('walk' if t < 28.4 else 'stand'), phase=(t * 1.6) % 1,
                eyes='smile' if turned else 'open', mouth='smile', arm=170 if turned and int(t * 5) % 2 == 0 else (150 if turned else None))
    blit_chibi(c, lit(she, 'day'), sx, 150, flip=turned)
    he = chibi('he', 'side', 'walk', phase=(q * 1.5) % 1, case=True, eyes='closed' if blink(t, 1) else 'open', mouth='smile')
    blit_chibi(c, lit(he, 'day'), hx_, 152)
    if turned:
        e = emote('note', hx('#e84a5f')); c.blit(e, int(sx) - 4, 104)
    petals(c, t, 10, 22, wind=-20, area=(0, 100, 200, 170), gust=1.0)
    return mem(c, t)


def sun_sky(c, skym, t):
    sky = Cv(W, 96)
    sky.a[:] = c.a[:96]
    sky.ellipse(276, 20, 10, 10, hx('#fff2b0')); sky.ellipse(276, 20, 8, 8, hx('#fffbe0'))
    for i in range(3):
        cs = cloud_sprite(60, 22, 80 + i, hx('#ffffff'), hx('#ffffff'), hx('#dce8f4'))
        sky.blit(cs, int((i * 120 + t * 6) % (W + 60)) - 60, 4 + i * 9)
    c.a[:96][skym] = sky.a[skym]


# ================================================================ S05 on duty: she writes on the blackboard
def board_text_xy():
    return BOARD['x'] + 76, BOARD['y'] + 24


@shot('board_day')
def board_day(t):
    c = board_static('day').copy()
    # window light from the left
    pts = [(0, 30), (40, 30), (120, 180), (0, 180)]
    m = Cv(W, H, alpha=True); m.poly(pts, (255, 255, 255))
    mm = (m.a[..., 3] > 0) & (bayer() < 0.3)
    c.a[mm] = np.clip(c.a[mm].astype(np.float32) * 1.1 + 16, 0, 255).astype(np.uint8)
    ln = L('示例一句歌词')
    x, y = board_text_xy()
    xe, ye, n = write(c, x, y, ln, t, CHALK, font='u', style='chalk', seed=1)
    # she writes, standing on the podium; hand follows the chalk
    writing = progress(t, ln)[0] < len(lyr.units(ln[2])) and t >= ln[0]
    sx = max(x - 8, min(xe - 8, x + 80))
    arm = 165 + (8 * math.sin(t * 18) if writing else 0)
    she = chibi('she', 'side', 'stand', eyes='open', mouth='line', arm=arm)
    blit_chibi(c, lit(she, 'day'), sx, 128)
    return mem(c, t)


# ================================================================ S06 his reply on the note
@shot('note_write')
def note_write(t):
    c = Cv(160, 90)
    desk_top(c, t)
    x0, y0, ww, hh = note_paper(c, 80, 44, 128, 66, unfold=1.0)
    # the doodle from before, small in the corner
    c.ellipse(x0 + 14, y0 + 10, 4, 4, hx('#ffb52a'))
    for k, fx in enumerate((x0 + 28, x0 + 36)):
        c.ellipse(fx, y0 + 8, 1.5, 1.5, GRAPHITE); c.line(fx, y0 + 10, fx, y0 + 15, GRAPHITE)
    ln = L('示例二句歌词内容')
    xe, ye, n = write(c, x0 + 12, y0 + 24, ln, t, GRAPHITE, font='w', style='pencil', seed=2, per_row=9)
    hxp = xe + 2 if t >= ln[0] else x0 + 12
    sleeve_hand(c, hxp + 4, y0 + 40, 'he', ang=-40, L=44, pencil=True)
    # a petal drifting down onto the paper
    q = seg(t, 36.4, 37.9)
    if q > 0:
        px_ = x0 + 96 - 20 * q + 4 * math.sin(t * 5)
        py_ = -4 + (y0 + 50) * ease_out(q)
        c.rect(px_, py_, 3, 2, hx('#ffd23a')); c.px(px_, py_, hx('#ffe878'))
    return mem(up2(c), t)


# ================================================================ S07 / S08 the swing and the chalk on the ground
GROUND_TXT = (22, 134)


@shot('swing_chalk')
def swing_chalk(t):
    c, skym = yard_static('sun')
    c = c.copy()
    sun_sky(c, skym, t)
    tree(c, 172, 128, t, sway=math.sin(t * 1.5) * 1.5, S=True, seed=3, h=60)
    tree(c, 222, 128, t, sway=math.sin(t * 1.5 + 1) * 1.5, S=True, seed=4, h=70)
    ang = 38 * math.sin(2 * math.pi * (t - 38.10) / 3.437 + 0.4)
    sx, sy = swing(c, t, ang, S=True)
    she = chibi('she', 'side', 'sit', eyes='smile', mouth='smile', wind=1 if ang < 0 else 0)
    blit_chibi(c, lit(she, 'day'), sx - 1, sy + 7)
    ln = L('示例三句歌词')
    x, y = GROUND_TXT
    write(c, x + 1, y + 1, ln, t, hx('#a8946e'), font='u', style='plain', seed=3)
    xe, ye, n = write(c, x, y, ln, t, hx('#fffaf0'), font='u', style='chalk', seed=3)
    he = chibi('he', 'side', 'crouch', eyes='down', mouth='smile', case=False)
    blit_chibi(c, lit(he, 'day'), max(x + 4, xe + 6), 156)
    petals(c, t, 10, 22, wind=-20, area=(0, 100, 200, 170), gust=1.0)
    return mem(c, t)


def stuck_umbrella(c):
    # the red umbrella hooked on the swing's top bar, upside down
    umbrella(c, SWING['x'] - 20, SWING['top'] - 18, *RED_UMB, open_=1.0, w=30, tilt=200, shaft=14)


@shot('swing_storm')
def swing_storm(t):
    c, skym = yard_static('storm')
    c = c.copy()
    sky = storm_sky(W, 96, t, light=0.0, seed=30, speed=2.2)
    c.a[:96][skym] = sky.a[skym]
    tree(c, 172, 128, t, sway=math.sin(t * 6) * 6 - 8, seed=3, h=60)
    tree(c, 222, 128, t, sway=math.sin(t * 6 + 1) * 6 - 8, seed=4, h=70)
    swing(c, t, 55 * math.sin(2 * math.pi * (t - 41.56) / 1.7184 + 0.4))
    stuck_umbrella(c)
    # yesterday's chalk washed out, today's line written and washed by the rain
    ln = L('示例四句歌词内容示')
    x, y = GROUND_TXT
    tmp = Cv(W, H, alpha=True)
    write(tmp, x, y, ln, t, (230, 234, 240, 255), font='u', style='chalk', seed=4)
    wash = 1 - 0.55 * seg(t, 43.6, 45.0)
    mm = (tmp.a[..., 3] > 0) & (bayer() < wash)
    c.a[mm] = hx('#c8d0dc')
    rain(c, t, 230, 50, speed=380, wind=-170, length=9, col=hx('#6a7aa8'))
    splashes(c, t, 130, 178, n=50, seed=51, col=hx('#8a9ac4'))
    petals(c, t, 50, 12, wind=-150, area=(0, 70, W, 180))
    return c


# ================================================================ S09 the riff on the music sheet
SOLFA_Y = {'ㄖㄨㄟ': 6, 'ㄙㄡ': 2, 'ㄒ一': 4, 'ㄉㄡ': 5, 'ㄌㄚ': 3}


def solfa_staff(c, x, y, ln, t, sp=17):
    staff(c, x, y, len(lyr.units(ln[2])) * sp + 22)
    n, frac = progress(t, ln, per=0.24)
    for i, tok in enumerate(lyr.units(ln[2])):
        if i >= n:
            break
        nx = x + 20 + i * sp
        st = SOLFA_Y.get(tok, 3)
        ny = y + 16 - st * 2 - 2
        pop = (i == n - 1 and frac < 0.5)
        note_head(c, nx, ny - (1 if pop else 0), hx('#e84a5f') if pop else hx('#2a2430'), stem_up=st < 4)
        # 注音 written vertically under the note
        for j, ch in enumerate(tok):
            text(c, nx - 3, y + 22 + j * 12, ch, hx('#e84a5f') if pop else GRAPHITE, font='w')


@shot('guitar_sheet')
def guitar_sheet(t):
    c = eaves_static('day').copy()
    # him playing guitar on a stool, her next to him swaying
    strum = (t * 2.33) % 1
    he = chibi('he', 'side', 'sit', eyes='closed' if blink(t, 1) else 'down', mouth='smile', arm=60 + 20 * math.sin(t * 14.6))
    blit_chibi(c, lit(he, 'day'), 262, 142, flip=True)
    guitar(c, 258, 128, s=1, strum=strum, flip=True)
    she = chibi('she', 'side', 'sit', eyes='closed', mouth='smile')
    blit_chibi(c, lit(she, 'day'), 296 + int(math.sin(t * 3.66) * 1), 142, flip=True)
    # music stand + sheet (foreground)
    c.rect(118, 150, 3, 30, hx('#2a2a32')); c.line(118, 178, 100, 180, hx('#2a2a32')); c.line(120, 178, 138, 180, hx('#2a2a32'))
    music_sheet(c, 8, 18, 228, 150)
    solfa_staff(c, 18, 30, L('示例五 句歌 词内 容示 例五 句歌'), t, sp=17)
    solfa_staff(c, 18, 96, L('示例 六句 歌词 内容 示例 六句 歌词 内容 示例 六句 歌词'), t, sp=17)
    c.rect(4, 164, 236, 5, hx('#3a3a44'))
    return mem(c, t)


# ================================================================ S10 she holds up the sketchbook
@shot('sketchbook')
def sketchbook(t):
    c = eaves_static('day').copy()
    he = chibi('he', 'side', 'sit', eyes='open', mouth='smile', look=1, arm=60 + 20 * math.sin(t * 14.6))
    blit_chibi(c, lit(he, 'day'), 214, 142, flip=True)
    guitar(c, 210, 128, s=1, strum=(t * 2.33) % 1, flip=True)
    bob = int(round(math.sin(t * 3.66 * math.pi) * 1))
    she = chibi('she', 'front', 'stand', eyes='smile', mouth='smile', arm='cup')
    blit_chibi(c, lit(she, 'day'), 150, 142 + bob)
    # sketchbook sign
    sx, sy = 120, 119 + bob
    c.rect(sx - 1, sy - 1, 62, 34, OUT); c.rect(sx, sy, 60, 32, hx('#fbf6ea'))
    for k in range(6):
        c.rect(sx + 4 + k * 10, sy - 2, 2, 3, hx('#8a8a96'))
    ln = L('示例七句歌词内容')
    write(c, sx + 6, sy + 3, ln, t, GRAPHITE, font='w', style='pencil', seed=5, per_row=4, row_h=14)
    c = upk(c, 168, 118, 2)
    return mem(c, t)


# ================================================================ S11 / S16 fogged window
def fog_write(t, ln, present, rows, xy, k=2, who='he', bottle=None, drop=0.0, seed=1):
    n, frac = progress(t, ln, per=0.24)
    total = len(lyr.units(ln[2]))
    combined = np.zeros((H, W), bool)
    cur = None
    remaining = n
    for s_, (mx, my) in zip(rows, xy):
        m, ps = text_mask(s_, 'u', k)
        take = min(len(s_), remaining)
        remaining -= take
        if take <= 0:
            break
        last = remaining == 0 and n < total
        cut = ps[take - 1] + (int(16 * k * min(1.0, 0.2 + frac)) if last else 16 * k)
        mm = m.copy(); mm[:, cut:] = False
        hh, ww = mm.shape
        combined[my:my + hh, mx:mx + ww] |= mm[:H - my, :W - mx]
        cur = (mx + cut, my + hh // 2)
    c = fog_window(t, present, combined[10:146, 18:302], (18, 10), None, seed=seed)
    if bottle is not None:
        flower_bottle(c, bottle[0], bottle[1], t, drop=drop, present=present)
    if cur is not None and t < ln[1]:
        sleeve_hand(c, cur[0] + 3, cur[1] + 6, who, ang=-30, L=60, finger=True)
    return c


@shot('fog_present')
def fog_present(t):
    ln = L('示例八句歌词内容示')
    c = fog_write(t, ln, True, ['示例歌词内', '示例歌词'], [(44, 28), (44, 74)], bottle=(262, 150),
                  drop=2 + 4 * seg(t, 55.5, 57.0), seed=3)
    return dark(c, flash_env(t, 54.9, 0.2) * 0.4, base=(0.85, 0.88, 1.0), top=1.15)


@shot('fog_memory')
def fog_memory(t):
    ln = L('示例十三句歌')
    c = fog_write(t, ln, False, ['示例歌词内容'], [(64, 46)], who='she', bottle=(262, 150), drop=0, seed=4)
    return mem(c, t, stamp=STAMP_RAIN, k=0.24)


# ================================================================ S12 skipping class
@shot('board_skip')
def board_skip(t):
    c = board_static('day').copy()
    ln = L('示例九句歌词内容')
    write(c, BOARD['x'] + 36, BOARD['y'] + 30, ln, t, CHALK_Y, font='u', style='chalk', seed=6)
    q = seg(t, 58.75, 60.1)
    for who, off in (('she', 0), ('he', -18)):
        x = 110 + 190 * q + off
        ch = chibi(who, 'side', 'walk', phase=(t * 2.2 + (0.5 if who == 'he' else 0)) % 1, eyes='open',
                   mouth='smile', case=(who == 'he'), arm=40)
        blit_chibi(c, lit(ch, 'day'), x, 150 - (1 if int(t * 8) % 2 else 0))
    return mem(c, t)


# ================================================================ S13 the note in her hand among falling petals
@shot('note_hand')
def note_hand(t):
    c = Cv(160, 90)
    vgrad(c, 0, 90, [hx('#8cc46a'), hx('#6aa84a'), hx('#5a8a3a')])
    r = np.random.default_rng(2)
    for i in range(60):
        x, y = r.uniform(0, 160), r.uniform(40, 90)
        c.px(x, y, hx('#ffd83a')); c.px(x + 1, y, hx('#ffe878'))
    sleeve_hand(c, 52, 66, 'she', ang=60, L=50)
    x0, y0, ww, hh = note_paper(c, 88, 42, 92, 30, unfold=1.0, crease=True)
    write(c, x0 + 8, y0 + 8, L('示例十句歌词'), t, GRAPHITE, font='w', style='pencil', seed=7)
    sleeve_hand(c, x0 + 4, y0 + hh - 2, 'she', ang=50, L=40)
    for i in range(12):
        ph = (t * 0.5 + i * 0.29) % 1
        c.rect(int((i * 37 + t * 9) % 160), int(ph * 96) - 4, 2, 1, hx('#ffd23a'))
    return mem(up2(c), t)


# ================================================================ S14 / S15 the dark classroom board
def board_dark_bg(t, Lk):
    c = board_static('dark').copy()
    desk_row(c, 150, 1.25, n=5, x0=-10, gap=72)
    dark(c, Lk, base=(0.20, 0.23, 0.40), top=1.2)
    return c


@shot('board_dark')
def board_dark(t):
    Lk = flashes(t, (61.90, 62.78), 0.22)
    c = board_dark_bg(t, Lk)
    col = mix(hx('#8a96a0'), CHALK, 0.35 + 0.65 * Lk)
    write(c, BOARD['x'] + 70, BOARD['y'] + 30, L('示例十一句歌'), t, col, font='u', style='chalk', seed=8)
    rain_shadows(c, t, 0, W, 0, 150, seed=5, k=0.2)
    return c


@shot('he_bust_board')
def he_bust_board(t):
    Lk = flashes(t, (63.62, 64.49), 0.25)
    c = board_dark_bg(t, Lk)
    col = mix(hx('#8a96a0'), CHALK, 0.35 + 0.65 * Lk)
    write(c, BOARD['x'] + 12, BOARD['y'] + 22, L('示例十二句歌'), t, col, font='u', style='chalk', seed=9)
    b = bust('he', 'down' if t < 64.2 else 'open', 'line', 'sad', look=-1, hood=True)
    b = light(b, tuple(0.5 + 0.7 * Lk for _ in range(3)), rim=(200, 210, 250), rim_side=-1, rim_k=0.3 + 0.3 * Lk)
    c.blit(b, 206, 100)
    rain_shadows(c, t, 180, W, 90, H, seed=6, k=0.25)
    return c


# ================================================================ S17 stepping out into the rain (bulletin board)
@shot('eaves_board')
def eaves_board(t):
    Lk = flashes(t, (67.05,), 0.3)
    c = eaves_static('storm').copy()
    col = mix(hx('#8a96a0'), CHALK, 0.4 + 0.6 * Lk)
    write(c, BB['x'] + 8, BB['y'] + 32, L('示例十四句歌词'), t, col, font='u', style='chalk', seed=10, per_row=4, row_h=19)
    rain(c, t, 140, 60, speed=380, wind=-90, length=9, col=hx('#8a9ac4'), area=(0, 146, W, 180))
    splashes(c, t, 148, 178, n=40, seed=61, col=hx('#a8b8dc'))
    q = ease(seg(t, 67.6, 68.3))
    y = 142 + 12 * q
    out_ = q > 0.5
    he = chibi('he', 'front', 'walk' if 0 < q < 1 else 'stand', phase=(t * 1.6) % 1, case=True, hood=False,
               eyes='closed' if t > 68.4 else 'open', mouth='line')
    blit_chibi(c, lit(he, 'rain'), 128, int(y))
    dark(c, Lk, base=(0.40, 0.43, 0.66))
    if out_:
        rain(c, t, 60, 62, speed=380, wind=-60, length=8, col=hx('#a8b8dc'), area=(98, 100, 158, 160))
        splashes(c, t, 112, 124, n=10, seed=63, col=hx('#c8d4ec'), x0=116, x1=140)
    roof_drip(c, t, n=22, col=hx('#8a9ac4'))
    return upk(c, 172, 103, 2)


# ================================================================ S18 grabbing the umbrella off the swing
@shot('grab_umbrella')
def grab_umbrella(t):
    c, skym = yard_static('storm')
    c = c.copy()
    sky = storm_sky(W, 96, t, light=0.0, seed=30, speed=2.2)
    c.a[:96][skym] = sky.a[skym]
    tree(c, 172, 128, t, sway=math.sin(t * 6) * 6 - 8, seed=3, h=60)
    tree(c, 222, 128, t, sway=math.sin(t * 6 + 1) * 6 - 8, seed=4, h=70)
    swing(c, t, 50 * math.sin(2 * math.pi * (t - 41.56) / 1.7184 + 0.4))
    got = t >= 70.95
    if not got:
        stuck_umbrella(c)
    if t < 70.6:
        x = 40 + 125 * seg(t, 69.6, 70.6)
        he = chibi('he', 'side', 'run', phase=(t * 2.4) % 1, case=True, eyes='open', mouth='line')
        blit_chibi(c, lit(he, 'rain'), x, 150)
    elif t < 71.3:
        q = seg(t, 70.6, 71.3)
        y = 150 - 22 * math.sin(q * math.pi)
        he = chibi('he', 'side', 'stand', case=True, eyes='open', mouth='o', arm=175)
        blit_chibi(c, lit(he, 'rain'), 165, int(y))
        if got:
            hx_, hy_ = hand_pos(165, int(y), 175)
            umbrella(c, hx_, hy_, *RED_UMB, open_=0.05, tilt=0, shaft=12)
    else:
        he = chibi('he', 'side', 'stand', case=True, eyes='open', mouth='line', arm=30)
        blit_chibi(c, lit(he, 'rain'), 165, 150)
        hx_, hy_ = hand_pos(165, 150, 30)
        umbrella(c, hx_, hy_, *RED_UMB, open_=0.05, tilt=150, shaft=12)
    rain(c, t, 230, 50, speed=380, wind=-170, length=9, col=hx('#6a7aa8'))
    splashes(c, t, 130, 178, n=50, seed=51, col=hx('#8a9ac4'))
    petals(c, t, 40, 12, wind=-150, area=(0, 70, W, 180))
    return c


# ================================================================ gate scenes (present) with the 黑板报
def gate_bg(t, rain_k=1.0, mode='storm', lamp_on=True):
    c = gate2_static(mode).copy()
    if lamp_on:
        lamp(c, 246, GATE_FEET + 2, h=74, on=True, glow_col=hx('#ffd68a'), post=hx('#2a2636'), glow_r=30)
    return c


def gate_rain(c, t, k=1.0, seed=70):
    if k <= 0:
        return
    rain(c, t, int(200 * k), seed, speed=380, wind=-150, length=9, col=hx('#7a8ab0'))
    splashes(c, t, 154, 178, n=int(46 * min(k, 2)), seed=seed + 1, col=hx('#9aaad0'))
    ripples(c, t, 160, 178, n=8, seed=seed + 2, col=hx('#3a3e58'))


def board_write(c, ln, t, Lk=0.0, lit_=None, per_row=7):
    col = lit_ or mix(hx('#9aa6b0'), CHALK, 0.45 + 0.55 * Lk)
    return write(c, GB['x'] + 6, GB['y'] + 14, ln, t, col, font='w', style='chalk', seed=hash(ln[2]) % 97, per_row=per_row, row_h=15)


@shot('board_run')
def board_run(t):
    Lk = flashes(t, (72.39, 75.85), 0.3)
    c = gate_bg(t)
    board_write(c, L('示例十五句歌词内容示例十'), t, Lk)
    q = seg(t, 73.3, 75.4)
    x = 20 + 180 * q
    he = chibi('he', 'side', 'run' if 0 < q < 1 else 'stand', phase=(t * 2.4) % 1, case=True, eyes='open', mouth='line', arm=20)
    blit_chibi(c, lit(he, 'rain'), x, 152)
    hx_, hy_ = hand_pos(x, 152, 20)
    umbrella(c, hx_, hy_, *RED_UMB, open_=0.05, tilt=150, shaft=12)
    gate_rain(c, t)
    dark(c, Lk, base=(0.52, 0.55, 0.78))
    return upk(c, 108, 96, 2)


@shot('gate_alone')
def gate_alone(t):
    Lk = 0.0
    c = gate_bg(t)
    board_write(c, L('示例十六句歌'), t)
    she = chibi('she', 'side', 'stand', eyes='down' if not blink(t, 2) else 'closed', mouth='line', arm=10)
    blit_chibi(c, lit(she, 'lamp'), 214, GATE_FEET, flip=True)
    gate_rain(c, t, 1.2)
    dark(c, Lk, base=(0.52, 0.55, 0.78))
    return c


@shot('gate_arrive')
def gate_arrive(t):
    c = gate_bg(t)
    board_write(c, L('示例十七句歌词内'), t)
    q = seg(t, 79.0, 80.3)
    x = -10 + 184 * ease_out(q)
    he = chibi('he', 'side', 'run' if q < 1 else 'stand', phase=(t * 2.4) % 1, case=True, eyes='open', mouth='line', arm=20)
    blit_chibi(c, lit(he, 'rain'), x, GATE_FEET)
    hx_, hy_ = hand_pos(x, GATE_FEET, 20)
    umbrella(c, hx_, hy_, *RED_UMB, open_=0.05, tilt=150, shaft=12)
    up_ = t >= 80.6
    she = chibi('she', 'side', 'stand', eyes='open' if up_ else 'down', mouth='o' if 80.6 <= t < 81.2 else 'line', arm=10)
    blit_chibi(c, lit(she, 'lamp'), 214, GATE_FEET, flip=True)
    gate_rain(c, t, 1.2)
    dark(c, 0.0, base=(0.52, 0.55, 0.78))
    return c


@shot('busts_open')
def busts_open(t):
    c = Cv(W, H)
    bokeh_bg(c, t, 'rain', seed=23)
    if t < 84.30:
        b = bust('she', 'wet' if not blink(t, 3) else 'closed', 'sad', 'sad', tear=min(12, int((t - 82.9) * 9)), wind=0)
        c.blit(lit(b, 'rain'), 124, 100)
        rain(c, t, 120, 33, speed=320, wind=-60, length=10, col=hx('#9aaad0'))
        c = upk(c, 160, 128, 2) if t > 83.5 else c
    else:
        b = bust('he', 'open', 'line', 'knit', hood=False)
        c.blit(lit(b, 'rain'), 124, 100)
        op = ease_out(seg(t, 85.0, 85.25))
        if t < 85.0:
            rain(c, t, 120, 34, speed=320, wind=-60, length=10, col=hx('#9aaad0'))
        else:
            rain(c, t, 120, 34, speed=320, wind=-60, length=10, col=hx('#9aaad0'), area=(0, 0, W, 40))
            umbrella(c, 160, 168, *RED_UMB, open_=op, w=300, tilt=0, shaft=120)
    return c


# ---- the couple under the umbrella (S23 / S25)
def couple(c, t, she_alpha=1.0, hold=True, he_arm2=70):
    he = chibi('he', 'side', 'stand', case=True, eyes='closed' if blink(t, 1) else 'open', mouth='line', arm=150, arm2=he_arm2)
    blit_chibi(c, lit(he, 'rain'), 192, GATE_FEET)
    if she_alpha > 0.02:
        she = chibi('she', 'side', 'stand', eyes='open' if not blink(t, 4) else 'closed', mouth='line', arm=70 if hold else 10)
        blit_chibi(c, lit(she, 'lamp'), 214, GATE_FEET, flip=True, alpha_mul=she_alpha)
    hx_, hy_ = hand_pos(192, GATE_FEET, 150)
    umbrella(c, hx_, hy_, *RED_UMB, open_=1.0, w=40, tilt=6, shaft=16)
    if hold and she_alpha > 0.5:
        c.rect(201, GATE_FEET - 18, 4, 3, hx('#f4cbaa'))


@shot('gate_hold')
def gate_hold(t):
    c = gate_bg(t)
    board_write(c, L('示例十八句歌词内容示例'), t)
    couple(c, t, hold=t >= 86.6, he_arm2=70 if t >= 86.6 else 10)
    gate_rain(c, t, 1.2)
    dark(c, flashes(t, (85.85,), 0.3), base=(0.52, 0.55, 0.78))
    return c


@shot('hands')
def hands(t):
    c = Cv(160, 90)
    vgrad(c, 0, 90, [hx('#2a3048'), hx('#3a4566'), hx('#56607e')])
    draw_hands(c, t, grip=1.0)
    # umbrella rim at the top, drops falling off it
    c.rect(0, 0, 160, 10, RED_UMB[0]); c.rect(0, 9, 160, 2, RED_UMB[1])
    for k in range(8):
        x = 10 + k * 20
        ph = (t * 1.8 + k * 0.37) % 1
        c.rect(x, 11 + ph * 70, 1, 3, hx('#b8c8e8'))
    rain(c, t, 30, 35, speed=200, wind=-40, length=6, col=hx('#8a9ac4'), area=(0, 12, 160, 90))
    return up2(c)


@shot('gate_whiteout')
def gate_whiteout(t):
    c = gate_bg(t)
    board_write(c, L('示例十九句歌词内容示例十九'), t)
    a = 1 - ease(seg(t, 93.4, 95.6))
    couple(c, t, she_alpha=a, hold=True, he_arm2=70)
    k = 1.2 + 3.5 * ease_in(seg(t, 91.0, 95.0))
    gate_rain(c, t, k, seed=80)
    dark(c, 0.0, base=(0.52, 0.55, 0.78))
    haze = 0.62 * ease(seg(t, 92.0, 95.0)) - 0.22 * ease(seg(t, 95.6, 96.5))
    if haze > 0:
        c.a[:] = np.clip(c.a.astype(np.float32) * (1 - haze) + np.array(hx('#aab4c8')) * haze, 0, 255).astype(np.uint8)
        rain(c, t, int(260 * haze), 86, speed=420, wind=-160, length=11, col=hx('#e8eef8'))
    return c


@shot('he_bust_rain')
def he_bust_rain(t):
    c = Cv(W, H)
    bokeh_bg(c, t, 'rain', seed=31)
    tear = min(12, max(0, int((t - 96.9) * 6)))
    b = bust('he', 'down' if not (98.4 < t < 98.6) else 'closed', 'sad', 'sad', tear=tear)
    c.blit(lit(b, 'rain'), 124, 100)
    rain(c, t, 140, 36, speed=340, wind=-60, length=10, col=hx('#9aaad0'))
    rain_shadows(c, t, 100, 220, 90, H, seed=7, k=0.3)
    return upk(c, 160, 130, 2) if t >= 98.0 else c


@shot('gate_kneel')
def gate_kneel(t):
    Lk = flashes(t, (100.02,), 0.35)
    c = gate_bg(t)
    board_write(c, L('示例二十句歌词内容示例'), t, Lk)
    he = chibi('he', 'side', 'crouch', case=True, eyes='down', mouth='line')
    blit_chibi(c, lit(he, 'rain'), 196, GATE_FEET)
    umbrella(c, 232, GATE_FEET - 4, *RED_UMB, open_=1.0, w=34, tilt=168, shaft=14)
    gate_rain(c, t, 1.6, seed=90)
    dark(c, Lk, base=(0.50, 0.53, 0.76))
    return c


@shot('umbrella_ground')
def umbrella_ground(t):
    c = Cv(160, 90)
    vgrad(c, 0, 90, [hx('#1e2232'), hx('#262a3c'), hx('#2e3246')])
    ripples(c, t, 10, 88, n=14, seed=5, col=hx('#4a5070'), x0=0, x1=160, rate=1.6)
    lift = ease(seg(t, 105.5, 106.25))
    umbrella(c, 76, 44 - 60 * lift, *RED_UMB, open_=1.0, w=96, tilt=170 - 160 * lift, shaft=24)
    if t >= 104.8:
        q = ease_out(seg(t, 104.8, 105.4))
        hxp, hyp = 76 + 30 * (1 - q) + 0, 44 - 60 * lift - 2
        sleeve_hand(c, hxp + 6, hyp + 2, 'he', ang=-140, L=50)
    rain(c, t, 50, 37, speed=220, wind=-30, length=6, col=hx('#8a9ac4'), area=(0, 0, 160, 90))
    splashes(c, t, 10, 88, n=20, seed=9, col=hx('#a8b8dc'), x0=0, x1=160)
    return up2(c)


@shot('gate_clear')
def gate_clear(t):
    q = ease(seg(t, 106.4, 108.3))
    a = gate_bg(t, mode='storm')
    dark(a, 0.0, base=(0.52, 0.55, 0.78))
    b = gate_bg(t, mode='sun', lamp_on=False)
    for kx in range(3):  # sun beams through the clouds
        light_cone(b, 60 + kx * 90, 0, 152, 20, 60, hx('#fff4d0'), k=0.18, dens=0.45)
    c = Cv(arr=dither_blend(a.a, b.a, q))
    board_write(c, L('示例二十一句歌词内容示例二十一句'), t, lit_=mix(hx('#9aa6b0'), CHALK, 0.5 + 0.5 * q), per_row=8)
    he = chibi('he', 'side', 'stand', case=True, eyes='open', mouth='o' if 107.6 < t < 108.4 else ('smile' if t > 108.8 else 'line'),
               look=1 if q > 0.3 else 0, arm=30)
    blit_chibi(c, lit(he, 'rain') if q < 0.5 else lit(he, 'day'), 196, GATE_FEET)
    hx_, hy_ = hand_pos(196, GATE_FEET, 30)
    umbrella(c, hx_, hy_, *RED_UMB, open_=0.05, tilt=150, shaft=12)
    gate_rain(c, t, 1.2 * (1 - q), seed=95)
    if q > 0.9:
        for i in range(6):  # sparkle on the wet ground
            ph = (t * 1.3 + i * 0.4) % 1
            if ph < 0.3:
                c.px(30 + i * 47, 160 + (i * 7) % 16, hx('#ffffff'))
    return c


@shot('yard_after')
def yard_after(t):
    c, skym = yard_static('sun')
    c = c.copy()
    sun_sky(c, skym, t)
    rainbow(c, 238, 110, 100, alpha=ease(seg(t, 110.4, 111.6)), width=2)
    tree(c, 172, 128, t, sway=math.sin(t * 1.5) * 1.5, S=True, seed=3, h=60)
    tree(c, 222, 128, t, sway=math.sin(t * 1.5 + 1) * 1.5, S=True, seed=4, h=70)
    amp = 22 * math.exp(-(t - 110.38) / 1.6)
    swing(c, t, amp * math.sin(2 * math.pi * (t - 110.38) / 1.7184), S=True)
    for (x, y, rx, ry) in ((60, 140, 26, 4), (150, 170, 34, 5), (260, 150, 22, 3)):
        puddle(c, x, y, rx, ry, hx('#8cc4ee'))
    he = chibi('he', 'side', 'stand', case=True, eyes='closed' if blink(t, 1) else 'open', mouth='smile', look=1, arm=30)
    blit_chibi(c, lit(he, 'day'), 132, 154)
    hx_, hy_ = hand_pos(132, 154, 30)
    umbrella(c, hx_, hy_, *RED_UMB, open_=0.05, tilt=150, shaft=12)
    petals(c, t, 16, 22, wind=-25, area=(0, 80, W, 170), gust=1.0)
    # drops falling from the trees
    for i in range(10):
        ph = (t * 1.2 + i * 0.31) % 1
        c.px(160 + i * 8, 80 + ph * 50, hx('#e8f4fc'))
    return c


# ================================================================ S31 the power comes back: TV forecast again
T_ON = 113.82
T_OFF = 118.40


@shot('tv_end')
def tv_end(t):
    c = tv_room_static(chalk=False).copy()
    for (x0, x1) in ((6, 26), (30, 46)):
        pts = [(x0, 14), (x1, 14), (x1 - 10, 150), (x0 - 10, 150)]
        m = Cv(W, H, alpha=True); m.poly(pts, (255, 255, 255))
        mm = (m.a[..., 3] > 0) & (bayer() < 0.55)
        c.a[mm] = hx('#f6e8c6')
    # screen
    tt = t - T_ON + E['power_on']  # map onto the opening's power-on timeline
    if t < T_ON:
        g, led, ecol, ek = None, 'red', (0, 0, 0), 0.0
    elif tt < E['hit']:
        g, led, ecol, ek = screen_now(tt)
    elif t < T_OFF:
        burst = flash_env(tt, E['hit'], 0.3)
        g = forecast_screen(t, 0, 1.0, burst, True)
        if E['hit'] <= tt < E['hit'] + 0.09:
            g.a = np.roll(g.a, -2, 0)
        led, ecol, ek = 'green', hx('#7cb6ec'), 0.3
    else:
        dt = t - T_OFF
        g = tv_glass_off(t, 0.2)
        sw, sh = TV['sw'], TV['sh']
        if dt < 0.09:
            src = forecast_screen(T_OFF, 0, 1.0, 0, True)
            p = dt / 0.09
            hh = max(1, int(sh * (1 - ease_in(p))))
            idx = np.linspace(0, sh - 1, hh).astype(int)
            g.a[(sh - hh) // 2:(sh - hh) // 2 + hh] = np.clip(src.a[idx].astype(np.int16) + int(120 * p), 0, 255).astype(np.uint8)
        elif dt < 0.18:
            lw = max(2, int(sw * (1 - ease_in((dt - 0.09) / 0.09))))
            g.rect((sw - lw) // 2, sh // 2, lw, 1, hx('#ffffff'))
        elif dt < 0.45:
            f = 1 - seg(dt, 0.18, 0.45)
            g.rect(sw // 2 - 1, sh // 2 - 1, 3, 3, mix(hx('#181a22'), hx('#ffffff'), f))
        led, ecol, ek = 'off', (0, 0, 0), 0.0
    tv_body(c, led, None)
    if ek > 0:
        glow(c, TV['sx'] + TV['sw'] // 2, TV['sy'] + TV['sh'] // 2, 150, ecol, k=ek * 0.6, dens=0.55, sy=0.8)
    if g is None:
        g = tv_glass_off(t, 0.15)
    c.paste(g, TV['sx'], TV['sy'])
    cy = TV['sy'] + TV['sh'] + 9
    lc = {'red': hx('#ff3a3a'), 'green': hx('#5aff7a'), 'off': hx('#3a1a1e')}[led]
    c.rect(TV['sx'] + TV['sw'] - 8, cy + 1, 3, 2, lc)
    # the last line in chalk on the blackboard's top edge
    write(c, 10, 165, L('示例二十二句歌词内容示'), t, hx('#dfe6dc'), font='w', style='chalk', seed=11)
    # fade to black with the music
    f = seg(t, 118.55, 119.15)
    if f > 0:
        shade(c, (1 - f * 0.85,) * 3)
        m = bayer() < f
        c.a[m] = (0, 0, 0)
    return c
