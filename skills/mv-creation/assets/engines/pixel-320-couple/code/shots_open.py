# -*- coding: utf-8 -*-
"""《晴天》开场 O1–O5 + 进正片 S01。每个镜头函数接收音频时间 t，返回 320x180 Cv。"""
import math
import numpy as np
from px import (Cv, hx, mix, W, H, OUT, vgrad, bayer, text, text_w, seg, ease, ease_out, ease_in, clamp, grade_ice, vignette,
                light, silhouette, upscale, grade_warm)
from chars import chibi, blit_chibi, emote, blink, P
from scenes import rain, splashes, ripples, glass_rain, lamp, glow, umbrella, RED_UMB, cloud_sprite
from shots import shot, lit, upk, memory_post
from story import EV as E
from scenes_qt import (shade, flash_env, shake, forecast_screen, tv_room_static, tv_body, tv_glass_off, TV, classroom_static,
                       desk, storm_sky, yard_static, swing, tree, petals, SWING, eaves_static, roof_drip, EAVES_Y,
                       gate2_static, GATE_FEET, icon_cloud)


def hand_pos(x, y, ang, flip=False):
    a = math.radians(ang)
    dx = -1 + 7 * math.sin(a)
    return (x - dx if flip else x + dx), y - 18 + 7 * math.cos(a)


def mixk(a, b, f):
    return tuple(a[i] + (b[i] - a[i]) * f for i in range(3))


# ================================================================ O1 TV forecast
def tv_state(t):
    if t < E['f1']:
        return 0
    if t < E['f2']:
        return 1
    if t < E['f3']:
        return 2
    return 3


def screen_now(t):
    """returns (screen Cv or None, led, emissive colour, emissive strength)."""
    T = TV
    sw, sh = T['sw'], T['sh']
    if t < E['power_on']:
        return None, 'red', (0, 0, 0), 0.0
    if t < E['hit']:
        # CRT power-on: bright line opens up
        g = tv_glass_off(t, 0.2)
        p = seg(t, E['power_on'], E['hit'] - 0.03)
        cy = sh // 2
        lw = int(sw * ease_out(min(1, p * 2.2)))
        lh = max(1, int(sh * ease_in(max(0, p * 1.6 - 0.6))))
        g.rect((sw - lw) // 2, cy - lh // 2, lw, lh, hx('#e8f0ff'))
        g.rect((sw - lw) // 2, cy, lw, 1, hx('#ffffff'))
        return g, 'green', hx('#c8d8ff'), 0.25 * p
    if t < E['cut']:
        st = tv_state(t)
        flip_p = 1.0
        for k, tf in enumerate((E['f1'], E['f2'], E['f3'])):
            if tf - 0.125 <= t < tf:
                flip_p = seg(t, tf - 0.125, tf) * 0.999
                st = k  # keep the old background while flapping
        burst = max(flash_env(t, E['hit'], 0.25), flash_env(t, E['acc'], 0.3))
        alert = int((t - E['f3']) / 0.2148) % 2 == 0
        g = forecast_screen(t, st, flip_p, burst, alert, seed=int(t * 24))
        # slam bounce on the first hit
        if E['hit'] <= t < E['hit'] + 0.09:
            g.a = np.roll(g.a, -2 if t < E['hit'] + 0.045 else -1, 0)
        # thunder: cloud slides over the sun + static
        if E['thunder'] <= t < E['f1'] - 0.02:
            q = seg(t, E['thunder'], E['thunder'] + 0.06)
            icon_cloud(g, int(-30 + 42 * ease_out(q)), 22, dark=True)
        if E['thunder'] <= t < E['thunder'] + 2 / 24 or E['f3'] <= t < E['f3'] + 1 / 24:
            r = np.random.default_rng(int(t * 240))
            m = r.random((sh, sw)) < 0.45
            g.a[m] = (r.integers(120, 255, (int(m.sum()), 1)) * np.ones((1, 3))).astype(np.uint8)
        col = {0: hx('#7cb6ec'), 1: hx('#8a98b0'), 2: hx('#4a5a80'), 3: hx('#ff3a3a')}[tv_state(t)]
        k = 0.30 if tv_state(t) < 3 else (0.55 if alert else 0.25)
        return g, 'green', col, k
    # power cut: picture collapses to a line, then a dot
    dt = t - E['cut']
    g = tv_glass_off(t, refl=clamp(dt / 0.5))
    if dt < 0.09:
        src = forecast_screen(E['cut'], 3, 1.0, 0, True)
        p = dt / 0.09
        hh = max(1, int(sh * (1 - ease_in(p))))
        idx = np.linspace(0, sh - 1, hh).astype(int)
        y0 = (sh - hh) // 2
        g.a[y0:y0 + hh] = np.clip(src.a[idx].astype(np.int16) + int(120 * p), 0, 255).astype(np.uint8)
        return g, 'green', hx('#ff3a3a'), 0.4 * (1 - p)
    if dt < 0.18:
        p = (dt - 0.09) / 0.09
        lw = max(2, int(sw * (1 - ease_in(p))))
        g.rect((sw - lw) // 2, sh // 2, lw, 1, hx('#ffffff'))
        g.rect((sw - lw) // 2 + lw // 4, sh // 2 - 1, lw // 2, 3, hx('#dfe8ff'))
        return g, 'off', hx('#dfe8ff'), 0.15
    if dt < 0.45:
        f = 1 - seg(dt, 0.18, 0.45)
        cx, cy = sw // 2, sh // 2
        g.rect(cx - 1, cy - 1, 3, 3, mix(hx('#181a22'), hx('#ffffff'), f))
        g.px(cx, cy, mix(hx('#181a22'), hx('#ffffff'), min(1, f * 1.5)))
        return g, 'off', (0, 0, 0), 0.0
    return g, 'off', (0, 0, 0), 0.0


@shot('tv')
def tv(t):
    c = tv_room_static().copy()
    # afternoon sun patch on the wall (left of the TV), gone when the thunder hits
    sun = 1 - ease(seg(t, E['thunder'], E['thunder'] + 0.4))
    if sun > 0:
        for (x0, x1) in ((6, 26), (30, 46)):
            pts = [(x0, 14), (x1, 14), (x1 - 10, 150), (x0 - 10, 150)]
            m = Cv(W, H, alpha=True); m.poly(pts, (255, 255, 255))
            mm = (m.a[..., 3] > 0) & (bayer() < 0.55 * sun)
            c.a[mm] = hx('#f6e8c6')
    # room light level
    if t < E['thunder']:
        k = (1.0, 1.0, 1.0)
    elif t < E['f2']:
        k = mixk((1.0, 1.0, 1.0), (0.66, 0.70, 0.84), ease(seg(t, E['thunder'], E['f1'])))
    elif t < E['f3']:
        k = (0.54, 0.58, 0.74)
    elif t < E['cut']:
        k = (0.44, 0.40, 0.52)
    else:
        k = mixk((0.30, 0.30, 0.42), (0.20, 0.22, 0.34), seg(t, E['cut'], E['cut'] + 0.3))
    g, led, ecol, ek = screen_now(t)
    tv_body(c, led, None)
    shade(c, k)
    # emissive spill from the screen onto the wall
    if ek > 0:
        glow(c, TV['sx'] + TV['sw'] // 2, TV['sy'] + TV['sh'] // 2, 150, ecol, k=ek * 0.6, dens=0.55, sy=0.8)
    T = TV
    if g is None:
        g = tv_glass_off(t, 0.15)
        # sunny reflection on the dark glass
        for x in range(8, 40):
            g.px(x, 4 + int((x - 24) ** 2 / 90), hx('#5a5e70'))
    c.paste(g, T['sx'], T['sy'])
    # lightning glimmer on the dead glass (O1 tail, before the O2 flash)
    if t >= E['cut'] + 0.45:
        pass
    # standby LED re-drawn on top of shading
    cy = T['sy'] + T['sh'] + 9
    lc = {'red': hx('#ff3a3a'), 'green': hx('#5aff7a'), 'off': hx('#3a1a1e')}[led]
    c.rect(T['sx'] + T['sw'] - 8, cy + 1, 3, 2, lc)
    if t < E['power_on'] and int(t * 12) % 2 == 0:
        c.rect(T['sx'] + T['sw'] - 9, cy, 5, 4, mix(lc, (40, 20, 20), 0.5)); c.rect(T['sx'] + T['sw'] - 8, cy + 1, 3, 2, lc)
    # shakes: thunder, the locks, the red alert hit
    dx = dy = 0
    for t0, amp in ((E['hit'], 2), (E['thunder'], 3), (E['f3'], 2)):
        if t0 <= t < t0 + 0.17:
            p = (t - t0) / 0.17
            dx = int(round(math.sin(p * 40) * amp * (1 - p)))
            dy = int(round(math.cos(p * 33) * amp * 0.6 * (1 - p)))
    shake(c, dx, dy, fill=OUT)
    return c


# ================================================================ O2 dark classroom
@shot('class_dark')
def class_dark(t):
    c = classroom_static().copy()
    L = max(flash_env(t, E['flash1'], 0.32), 0.65 * flash_env(t, E['flick'], 0.1))
    # desks (three rows, back to front)
    for row, (y, s) in enumerate(((118, 0.8), (130, 0.95), (148, 1.15))):
        for i in range(5):
            x = -10 + i * 72 + (row % 2) * 30
            desk(c, int(x), y, s)
    # flower bottle on the middle sill
    c.rect(156, 100, 6, 8, hx('#9ac8d0')); c.rect(157, 101, 1, 6, hx('#d8f0f4'))
    c.line(159, 100, 157, 92, hx('#4a7a3a')); c.line(159, 100, 162, 94, hx('#4a7a3a'))
    c.ellipse(157, 91, 2, 2, hx('#ffd23a')); c.ellipse(162, 93, 2, 2, hx('#ffd23a')); c.px(157, 91, hx('#b8861a'))
    # dead TV in the top-right corner
    c.rect(276, 8, 36, 26, hx('#3c3a46')); c.rect(279, 11, 30, 18, hx('#181a22')); c.rect(292, 0, 4, 8, hx('#5a5866'))
    # window light shadows on the floor when lightning
    if L > 0.05:
        for wx in (20, 120, 220):
            pts = [(wx + 10, 136), (wx + 74, 136), (wx + 110, 180), (wx + 36, 180)]
            m = Cv(W, H, alpha=True); m.poly(pts, (255, 255, 255))
            mm = (m.a[..., 3] > 0) & (bayer() < 0.5 * L)
            c.a[mm] = np.clip(c.a[mm].astype(np.float32) * 1.25 + 30, 0, 255).astype(np.uint8)
    base = (0.24, 0.26, 0.40)
    k = tuple(base[i] + (1.25 - base[i]) * L for i in range(3))
    shade(c, k)
    # windows: storm outside, rain on the glass (more and more)
    for j, wx in enumerate((20, 120, 220)):
        sky = storm_sky(80, 86, t + j * 3.1, light=L * 0.7, seed=10 + j, speed=1.6)
        # thrashing tree silhouettes
        r = np.random.default_rng(j)
        tc = mix(hx('#141826'), hx('#4a5470'), L)
        sky.rect(0, 76, 80, 10, tc)
        for i in range(3):
            bx = r.uniform(-10, 60); sway = math.sin(t * 7 + i) * 4 + math.sin(t * 13 + i) * 2
            cs = cloud_sprite(40, 26, 90 + j * 3 + i, tc, tc, tc)
            sky.blit(cs, int(bx + sway), 56 + int(r.uniform(0, 8)))
        rain(sky, t, 46, 40 + j, speed=360, wind=-150, length=8, col=hx('#8a9ac4'), area=(0, 0, 80, 86))
        glass_rain(sky, t, 0, 0, 80, 86, seed=21 + j, n=6 + int(10 * seg(t, E['cut'], E['bass'])),
                   static=int(20 + 90 * seg(t, E['cut'], E['bass'])), col=hx('#5a6a96'), hi=hx('#b8c8ec'))
        c.paste(sky, wx, 21)
        c.rect(wx + 39, 21, 3, 86, mix(hx('#e8e0cc'), (0, 0, 0), 0.7 - 0.5 * L))
        c.rect(wx, 62, 80, 2, mix(hx('#e8e0cc'), (0, 0, 0), 0.7 - 0.5 * L))
    if E['flash1'] <= t < E['flash1'] + 1 / 24:
        c.a[:] = (236, 242, 255)
    return c


# ================================================================ O3 storm yard (wide master)
SWING_T0 = E['bass']


def swing_angle(t, amp=55.0, period=1.7184):
    gust = flash_env(t, E['hit2'], 0.5) * 12 + flash_env(t, E['bar2'], 0.5) * 10
    return (amp + gust) * math.sin(2 * math.pi * (t - SWING_T0) / period + 0.9)


@shot('yard_storm')
def yard_storm(t):
    c, skym = yard_static('storm')
    c = c.copy()
    sky = storm_sky(W, 96, t, light=0.0, seed=30, speed=2.2)
    c.a[:96][skym] = sky.a[skym]
    tree(c, 172, 128, t, sway=math.sin(t * 6) * 6 - 8, seed=3, h=60)
    tree(c, 222, 128, t, sway=math.sin(t * 6 + 1) * 6 - 8, seed=4, h=70)
    swing(c, t, swing_angle(t))
    rain(c, t, 230, 50, speed=380, wind=-170, length=9, col=hx('#6a7aa8'))
    splashes(c, t, 130, 178, n=50, seed=51, col=hx('#8a9ac4'))
    ripples(c, t, 134, 158, n=10, seed=52, col=hx('#3a4058'))
    gust = 1.0 + 0.6 * flash_env(t, E['hit2'], 0.4) + 0.6 * flash_env(t, E['bar2'], 0.4)
    petals(c, t, 70, 12, wind=-150, area=(0, 70, W, 180), gust=gust)
    petals(c, t, 18, 13, wind=-210, area=(0, 120, 140, 180), gust=gust)
    # hits: shake
    dx = dy = 0
    for t0 in (E['bass'], E['hit2'], E['bar2']):
        if t0 <= t < t0 + 0.15:
            p = (t - t0) / 0.15
            dx = int(round(math.sin(p * 36) * 2 * (1 - p))); dy = int(round(math.cos(p * 30) * 1.5 * (1 - p)))
    shake(c, dx, dy, fill=hx('#141828'))
    return c


# ================================================================ O4 he under the eaves
HE_X = 150


WALK0, WALK1 = E['look'] + 0.36, 11.96   # he takes a few steps toward the gate, stops on the hit at 11.96


def he_x(t):
    q = seg(t, WALK0, WALK1)
    return HE_X + 30 * q


def he_scene(t, L):
    c = eaves_static().copy()
    rain(c, t, 140, 60, speed=380, wind=-90, length=9, col=hx('#8a9ac4'), area=(0, 146, W, 180))
    splashes(c, t, 148, 178, n=40, seed=61, col=hx('#a8b8dc'))
    look = t >= E['look']
    walking = WALK0 <= t < WALK1
    he = chibi('he', 'side', 'walk' if walking else 'stand', phase=((t - WALK0) * 1.55) % 1, case=True, hood=True,
               eyes='closed' if blink(t, 2) and not (E['look'] <= t < E['look'] + 0.5) else 'open',
               mouth='o' if E['look'] <= t < E['look'] + 0.6 else 'line', look=1 if look else 0)
    x = he_x(t)
    blit_chibi(c, lit(he, 'rain'), x, EAVES_Y)
    base = (0.40, 0.43, 0.66)
    k = tuple(base[i] + (1.3 - base[i]) * L for i in range(3))
    shade(c, k)
    roof_drip(c, t, n=26, col=mix(hx('#8a9ac4'), (255, 255, 255), 0.3 * L))
    if look:
        p = t - E['look']
        if p < 1.4:
            e = emote('excl', hx('#e84a5f'))
            c.blit(e, int(x) + 2, EAVES_Y - 52 - (2 if p < 0.08 else 0))
    return c


@shot('he_eaves')
def he_eaves(t):
    L = max(flash_env(t, E['L1'], 0.28), flash_env(t, E['L2'], 0.3), 0.35 * flash_env(t, E['look'], 0.2))
    c = he_scene(t, L)
    if t >= E['L2']:
        c = upk(c, he_x(t) + 4, EAVES_Y - 20, 2)
    for t0 in (E['L1'], E['L2']):
        if t0 <= t < t0 + 1 / 24:
            c.a[:] = (236, 242, 255)
    return c


# ================================================================ O5 she at the gate, umbrella ripped away
SHE_X = 214


def she_scene(t, L, tf=None, umb=None, shade_on=True):
    """tf: frozen time for the rain/pose; umb: (x, y, scale, tilt) override for the flying umbrella."""
    tr = t if tf is None else tf
    c = gate2_static().copy()
    lamp(c, 246, GATE_FEET + 2, h=74, on=True, glow_col=hx('#ffd68a'), post=hx('#2a2636'), glow_r=30)
    rain(c, tr, 200, 70, speed=380, wind=-150 - 80 * seg(tr, E['gust'], E['freeze']), length=9, col=hx('#7a8ab0'))
    splashes(c, tr, 154, 178, n=46, seed=71, col=hx('#9aaad0'))
    ripples(c, tr, 160, 178, n=8, seed=72, col=hx('#3a3e58'))
    g = seg(tr, E['gust'], E['freeze'])
    wob = math.sin(tr * 9) * (4 + 16 * g) + math.sin(tr * 23) * 3 * g
    ripped = tr >= E['freeze'] - 0.16
    arm = 150 if not ripped else 172
    eyes = 'open' if tr < E['gust'] + 0.3 else ('closed' if not ripped else 'open')
    mouth = 'o' if ripped else 'line'
    lean = int(round(3 * g * (0.5 + 0.5 * math.sin(tr * 9))))
    she = chibi('she', 'side', 'stand', eyes=eyes, mouth=mouth, arm=arm, wind=1 + (1 if g > 0.3 else 0))
    blit_chibi(c, lit(she, 'lamp'), SHE_X - lean, GATE_FEET, flip=True)
    hx_, hy_ = hand_pos(SHE_X - lean, GATE_FEET, arm, flip=True)
    base = (0.52, 0.55, 0.78)
    k = tuple(base[i] + (1.3 - base[i]) * L for i in range(3))
    if shade_on:
        shade(c, k)
    if umb is None:
        if not ripped:
            umbrella(c, hx_, hy_, *RED_UMB, open_=1.0, w=36, tilt=8 + wob, shaft=16)
        else:
            q = seg(tr, E['freeze'] - 0.16, E['freeze'])
            ux, uy = hx_ - 34 * ease_out(q), hy_ - 22 * ease_out(q)
            umbrella(c, ux, uy, *RED_UMB, open_=1.0, w=36, tilt=8 + 70 * q, shaft=16)
    else:
        ux, uy, s, tilt = umb
        umbrella(c, ux, uy, *RED_UMB, open_=1.0, w=int(36 * s), tilt=tilt, shaft=int(16 * s))
    return c


UMB_FROZEN = None


def umb_frozen_pos():
    hx_, hy_ = hand_pos(SHE_X, GATE_FEET, 172, flip=True)
    return hx_ - 34, hy_ - 22


@shot('she_gate')
def she_gate(t):
    L = flash_env(t, E['L3'], 0.3)
    if t < E['freeze']:
        c = she_scene(t, L)
        if t >= E['gust']:  # wind picks up on the bar line: hard push in on her
            c = upk(c, SHE_X - 14, GATE_FEET - 34, 2)
    elif t < E['thaw']:
        c = she_scene(t, 0, tf=E['freeze'] - 0.001, shade_on=False)
        c = Cv(arr=grade_ice(c.a))
        c = Cv(arr=vignette(c.a, 0.55, col=(14, 18, 34)))
        if t >= E['hit3']:
            ux, uy = umb_frozen_pos()
            c = upk(c, ux, uy - 18, 2)
    else:
        q = seg(t, E['thaw'], E['crash'] - 0.05)
        ux0, uy0 = umb_frozen_pos()
        s = 1 + 15 * ease_in(q) ** 1.2
        # canopy centre heads to screen centre while growing
        cx = ux0 + (W / 2 - ux0) * ease(q)
        cy = (uy0 - 16) + (H / 2 + 10 - (uy0 - 16)) * ease(q)
        tilt = 78 + 300 * ease_in(q)
        a = math.radians(tilt)
        sh = 16 * s
        hxp = cx - sh * math.sin(a)
        hyp = cy + sh * math.cos(a)
        c = she_scene(t, 0, umb=(hxp, hyp, s, tilt))
        if q > 0.97:
            c.a[:] = RED_UMB[0]
    for t0 in (E['L3'],):
        if t0 <= t < t0 + 1 / 24:
            c.a[:] = (236, 242, 255)
    return c


# ================================================================ S01 memory: the same yard on a sunny day
@shot('memory_sun')
def memory_sun(t):
    c, skym = yard_static('sun')
    c = c.copy()
    # drifting white clouds + sun
    sky = Cv(W, 96)
    sky.a[:] = c.a[:96]
    sky.ellipse(276, 20, 10, 10, hx('#fff2b0')); sky.ellipse(276, 20, 8, 8, hx('#fffbe0'))
    for i in range(3):
        cs = cloud_sprite(60, 22, 80 + i, hx('#ffffff'), hx('#ffffff'), hx('#dce8f4'))
        sky.blit(cs, int((i * 120 + t * 6) % (W + 60)) - 60, 4 + i * 9)
    c.a[:96][skym] = sky.a[skym]
    tree(c, 172, 128, t, sway=math.sin(t * 1.5) * 1.5, S=True, seed=3, h=60)
    tree(c, 222, 128, t, sway=math.sin(t * 1.5 + 1) * 1.5, S=True, seed=4, h=70)
    ang = 22 * math.sin(2 * math.pi * (t - E['crash']) / 3.437 + 1.2)
    sx, sy = swing(c, t, ang, S=True)
    she = chibi('she', 'side', 'sit', eyes='closed' if blink(t, 4) else 'open', mouth='smile', wind=1 if ang < 0 else 0)
    blit_chibi(c, lit(she, 'day'), sx - 1, sy + 7)
    he = chibi('he', 'side', 'stand', case=True, eyes='closed' if blink(t, 1) else 'open', mouth='smile')
    blit_chibi(c, lit(he, 'day'), 138, 150)
    petals(c, t, 14, 22, wind=-20, area=(0, 100, 200, 170), gust=1.0)
    c = memory_post(c, t, stamp='2003.07.31', k=0.3, dust_n=8, vig=0.2)
    return c
