# 近景大头像（在同一 320x180 像素网格上画，头宽约 64px）
import functools
import numpy as np
from PIL import Image, ImageDraw
from px import OUT, outline_rgba, bayer, lc
from chars import HIM, HER, EYE, MOUTH, TONGUE

BW, BH = 128, 122
EYE_IRIS = (120, 66, 82)


def _blush(im, box, col):
    a = np.array(im)
    x0, y0, x1, y1 = box
    yy, xx = np.mgrid[y0:y1 + 1, x0:x1 + 1]
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    m = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
    m &= bayer(x1 - x0 + 1, y1 - y0 + 1, x0, y0) < .55
    m &= a[y0:y1 + 1, x0:x1 + 1, 3] > 0
    seg = a[y0:y1 + 1, x0:x1 + 1]
    seg[m] = (*col, 255)
    return Image.fromarray(a)


@functools.lru_cache(maxsize=256)
def her_bust(eyes='open', mouth='smile', dimple=True, blush=True, lash_glow=0, hair_sway=0, look=0):
    C = HER
    im = Image.new('RGBA', (BW, BH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hs = hair_sway
    # 后发
    d.ellipse([20, 8, 108, 98], fill=C['hair_d'])
    d.polygon([(22, 56), (106, 56), (108 + hs, 116), (20 + hs, 116)], fill=C['hair_d'])
    # 衣服
    d.polygon([(14, 122), (30, 102), (98, 102), (114, 122)], fill=C['blouse'])
    d.polygon([(30, 102), (40, 100), (36, 122), (24, 122)], fill=C['blouse_d'])
    d.polygon([(42, 104), (52, 104), (50, 122), (40, 122)], fill=C['dress'])
    d.polygon([(76, 104), (86, 104), (88, 122), (78, 122)], fill=C['dress'])
    d.polygon([(48, 112), (80, 112), (82, 122), (46, 122)], fill=C['dress'])
    d.rectangle([56, 84, 72, 100], fill=C['skin_d'])
    # 圆领
    d.ellipse([44, 94, 64, 108], fill=C['blouse']); d.ellipse([64, 94, 84, 108], fill=C['blouse'])
    d.arc([44, 94, 64, 108], 0, 180, fill=C['blouse_d']); d.arc([64, 94, 84, 108], 0, 180, fill=C['blouse_d'])
    d.polygon([(58, 96), (64, 100), (58, 104)], fill=C['ribbon']); d.polygon([(70, 96), (64, 100), (70, 104)], fill=C['ribbon'])
    d.rectangle([62, 98, 66, 102], fill=C['ribbon_d'])
    # 脸
    d.ellipse([32, 20, 96, 86], fill=C['skin'])
    d.ellipse([40, 54, 88, 92], fill=C['skin'])
    # 前发顶
    d.ellipse([27, 4, 101, 58], fill=C['hair'])
    bang = [(32, 26), (96, 26), (96, 40), (90, 44), (85, 39), (79, 45), (73, 40), (67, 45), (61, 40), (55, 45), (49, 40), (43, 44), (37, 39), (32, 42)]
    d.polygon(bang, fill=C['hair'])
    d.polygon([(28, 28), (37, 34), (39, 62), (37, 90), (31, 96 + hs // 2), (24, 70)], fill=C['hair'])
    d.polygon([(100, 28), (91, 34), (89, 62), (91, 90), (97, 96 + hs // 2), (104, 70)], fill=C['hair'])
    for (x0, y0, x1, y1) in ((44, 14, 58, 12), (62, 11, 76, 11), (80, 13, 88, 16)):
        d.line([(x0, y0), (x1, y1)], fill=C['hair_h'], width=2)
    for x in (46, 58, 70, 82):
        d.line([(x, 28), (x + 1, 36)], fill=C['hair_d'])
    # 蝴蝶结
    d.polygon([(84, 8), (95, 14), (84, 22)], fill=C['ribbon']); d.polygon([(108, 6), (97, 14), (108, 22)], fill=C['ribbon'])
    d.rectangle([94, 11, 98, 17], fill=C['ribbon_d'])
    # 眼
    for i, cx in enumerate((48, 80)):
        cx += look
        out = -1 if i == 0 else 1
        if eyes == 'closed':
            d.arc([cx - 8, 50, cx + 8, 62], 20, 160, fill=EYE, width=2)
            ox = cx + out * 8
            d.line([(ox, 56), (ox + out * 4, 59)], fill=EYE); d.line([(ox - out * 2, 58), (ox + out * 1, 62)], fill=EYE)
            continue
        if eyes == 'happy':
            d.arc([cx - 8, 52, cx + 8, 66], 200, 340, fill=EYE, width=2)
            ox = cx + out * 8
            d.line([(ox, 58), (ox + out * 4, 55)], fill=EYE); d.line([(ox - out * 1, 56), (ox + out * 2, 52)], fill=EYE)
            continue
        d.ellipse([cx - 6, 49, cx + 6, 64], fill=(44, 30, 46))
        d.ellipse([cx - 5, 55, cx + 5, 64], fill=EYE_IRIS)
        d.ellipse([cx - 3, 57, cx + 3, 62], fill=(150, 90, 110))
        d.rectangle([cx - 2, 56, cx + 1, 59], fill=(44, 30, 46))
        d.rectangle([cx + 1, 51, cx + 3, 54], fill=(255, 255, 255))
        d.rectangle([cx - 4, 60, cx - 3, 61], fill=(255, 255, 255))
        # 上眼睑 + 长睫毛
        d.line([(cx - 8, 50), (cx + 8, 50)], fill=EYE, width=2)
        ox = cx + out * 8
        L = 6 + lash_glow
        d.line([(ox, 50), (ox + out * 5, 45)], fill=EYE, width=1)
        d.line([(ox - out * 2, 49), (ox + out * 2, 43 - lash_glow // 2)], fill=EYE, width=1)
        d.line([(ox - out * 5, 49), (ox - out * 4, 44)], fill=EYE, width=1)
        d.line([(ox, 51), (ox + out * 3, 51)], fill=EYE)
        d.point((ox - out * 1, 64), fill=EYE); d.point((ox + out * 1, 63), fill=EYE)
    # 眉
    d.line([(41, 43), (53, 42)], fill=C['hair_d']); d.line([(75, 42), (87, 43)], fill=C['hair_d'])
    # 鼻
    d.point((64, 70), fill=C['skin_d']); d.point((65, 71), fill=C['skin_d'])
    # 嘴
    if mouth == 'open':
        d.polygon([(55, 75), (73, 75), (70, 82), (64, 84), (58, 82)], fill=MOUTH)
        d.rectangle([57, 76, 71, 77], fill=(255, 255, 255))
        d.ellipse([60, 80, 68, 85], fill=TONGUE)
    elif mouth == 'o':
        d.ellipse([60, 74, 68, 82], fill=MOUTH)
    else:
        d.arc([55, 68, 73, 79], 25, 155, fill=MOUTH, width=2)
    im = outline_rgba(im)
    if blush:
        im = _blush(im, (34, 64, 48, 72), C['blush']); im = _blush(im, (80, 64, 94, 72), C['blush'])
    d = ImageDraw.Draw(im)
    if dimple:
        dc = C['dimple']
        for (x, y) in ((51, 78), (52, 79), (51, 79)): d.point((x, y), fill=dc)
        for (x, y) in ((77, 78), (76, 79), (77, 79)): d.point((x, y), fill=dc)
    return im


@functools.lru_cache(maxsize=256)
def his_bust(eyes='open', mouth='smile', blush=False, hat=True, look=0, wet=False):
    C = HIM
    im = Image.new('RGBA', (BW, BH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # 身体
    d.polygon([(12, 122), (28, 100), (100, 100), (116, 122)], fill=C['shirt'])
    for y in (108, 116): d.line([(16, y), (40, y)], fill=C['shirt_m']); d.line([(88, y), (112, y)], fill=C['shirt_m'])
    d.line([(30, 100), (24, 122)], fill=C['shirt_b']); d.line([(98, 100), (104, 122)], fill=C['shirt_b'])
    d.polygon([(36, 122), (40, 100), (88, 100), (92, 122)], fill=C['vest'])
    for x in (46, 82): d.line([(x, 100), (x, 122)], fill=C['vest_w'])
    d.line([(38, 112), (90, 112)], fill=C['vest_w']); d.line([(52, 100), (52, 122)], fill=C['vest_r']); d.line([(76, 100), (76, 122)], fill=C['vest_r'])
    d.polygon([(56, 100), (64, 116), (72, 100)], fill=C['shirt'])
    d.rectangle([56, 84, 72, 100], fill=C['skin_d'])
    # 领结
    d.polygon([(48, 93), (62, 98), (62, 104), (48, 109)], fill=C['bow1'])
    d.polygon([(80, 93), (66, 98), (66, 104), (80, 109)], fill=C['bow1'])
    for k in (0, 6):
        d.line([(50 + k, 95 + k // 3), (50 + k, 107 - k // 3)], fill=C['bow2'], width=2)
        d.line([(78 - k, 95 + k // 3), (78 - k, 107 - k // 3)], fill=C['bow2'], width=2)
    d.line([(53, 96), (53, 106)], fill=C['bow3'], width=2); d.line([(75, 96), (75, 106)], fill=C['bow3'], width=2)
    d.rectangle([61, 97, 67, 105], fill=C['bow3'])
    # 耳 & 脸
    d.ellipse([27, 52, 37, 68], fill=C['skin']); d.ellipse([91, 52, 101, 68], fill=C['skin'])
    d.ellipse([32, 24, 96, 92], fill=C['skin'])
    # 头发
    if not hat:
        d.ellipse([28, 14, 100, 62], fill=C['hair'])
        d.arc([40, 20, 88, 50], 200, 320, fill=C['hair_h'], width=2)
    d.polygon([(30, 30), (98, 30), (98, 44), (88, 40), (78, 47), (66, 43), (54, 52), (44, 47), (36, 58), (30, 50)], fill=C['hair'])
    d.polygon([(28, 34), (36, 34), (36, 64), (32, 62)], fill=C['hair'])
    d.polygon([(92, 34), (100, 34), (97, 62), (92, 64)], fill=C['hair'])
    d.line([(48, 40), (62, 38)], fill=C['hair_h'], width=2); d.line([(70, 36), (84, 38)], fill=C['hair_h'], width=1)
    # 眼
    for i, cx in enumerate((50, 78)):
        cx += look
        if eyes == 'squeeze':
            s = 1 if i == 0 else -1
            d.line([(cx - 5 * s, 56), (cx + 3 * s, 62), (cx - 5 * s, 68)], fill=EYE, width=2)
            continue
        if eyes == 'happy':
            d.arc([cx - 6, 58, cx + 6, 70], 200, 340, fill=EYE, width=2); continue
        if eyes == 'closed':
            d.arc([cx - 6, 56, cx + 6, 66], 20, 160, fill=EYE, width=2); continue
        if eyes == 'heart':
            d.ellipse([cx - 6, 56, cx, 62], fill=(236, 60, 90)); d.ellipse([cx, 56, cx + 6, 62], fill=(236, 60, 90))
            d.polygon([(cx - 6, 60), (cx + 6, 60), (cx, 68)], fill=(236, 60, 90)); continue
        top = 60 if eyes == 'down' else 56
        d.ellipse([cx - 4, top, cx + 4, 68], fill=(40, 30, 40))
        if eyes != 'down':
            d.rectangle([cx + 1, 58, cx + 2, 60], fill=(255, 255, 255))
        else:
            d.line([(cx - 5, 60), (cx + 5, 60)], fill=EYE, width=2)
    # 眉
    if eyes in ('down',):
        d.line([(42, 52), (56, 54)], fill=C['hair']); d.line([(72, 54), (86, 52)], fill=C['hair'])
    elif eyes == 'squeeze':
        d.line([(42, 50), (56, 54)], fill=C['hair'], width=2); d.line([(72, 54), (86, 50)], fill=C['hair'], width=2)
    else:
        d.line([(72, 50), (86, 49)], fill=C['hair'], width=2)
    d.point((64, 74), fill=C['skin_d']); d.point((65, 75), fill=C['skin_d'])
    # 嘴
    if mouth == 'sneeze':
        d.ellipse([55, 76, 73, 90], fill=MOUTH); d.ellipse([59, 82, 69, 90], fill=TONGUE)
    elif mouth == 'open':
        d.polygon([(55, 79), (73, 79), (70, 86), (64, 88), (58, 86)], fill=MOUTH)
        d.rectangle([57, 80, 71, 81], fill=(255, 255, 255)); d.ellipse([60, 84, 68, 89], fill=TONGUE)
    elif mouth == 'sad':
        d.arc([57, 82, 71, 90], 200, 340, fill=MOUTH, width=2)
    elif mouth == 'line':
        d.line([(59, 82), (69, 82)], fill=MOUTH, width=2)
    else:
        d.arc([55, 72, 73, 84], 25, 155, fill=MOUTH, width=2)
    # 帽子
    if hat:
        d.ellipse([14, 27, 114, 43], fill=C['hat_d'])
        d.ellipse([16, 25, 112, 39], fill=C['hat'])
        d.polygon([(30, 32), (34, 4), (50, 0), (64, 6), (78, 0), (94, 4), (98, 32)], fill=C['hat'])
        d.rectangle([31, 22, 97, 31], fill=C['band'])
        for x in (44, 64, 84): d.line([(x, 4 if x != 64 else 7), (x, 21)], fill=C['hat_r'], width=2)
        for x in (54, 74): d.line([(x, 3), (x, 21)], fill=C['hat_d'])
        d.line([(33, 13), (95, 13)], fill=C['hat_l'], width=2)
        d.line([(20, 36), (108, 36)], fill=C['hat_r'])
    im = outline_rgba(im)
    if blush:
        im = _blush(im, (36, 70, 48, 78), C['blush']); im = _blush(im, (80, 70, 92, 78), C['blush'])
    return im
