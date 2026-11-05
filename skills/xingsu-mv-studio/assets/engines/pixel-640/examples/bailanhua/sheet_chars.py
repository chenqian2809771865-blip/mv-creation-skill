import sys; sys.path.insert(0,'.')
from core import *
from chibi import *
from sprite import place
img = new((96, 104, 130), 640, 360)
img[200:] = (70, 76, 100)
x = 40
items = [
 ('him', dict(view='front', s=1.0, light='day')),
 ('him', dict(view='side', s=1.0, light='day', walk=0.25)),
 ('him', dict(view='back', s=1.0, light='day')),
 ('her', dict(view='front', s=1.0, light='day', dimple=True)),
 ('her', dict(view='side', s=1.0, light='day', walk=0.25)),
 ('her', dict(view='back', s=1.0, light='day')),
 ('her', dict(view='front', s=1.0, light='day', style='now')),
 ('her', dict(view='side', s=1.0, light='day', style='now', walk=0.6)),
]
for who, kw in items:
    spr, anc = (HIM if who=='him' else HER)(**kw)
    place(img, spr, anc, x, 190)
    x += 74
# night row, smaller + big busts
x = 40
items2 = [
 ('him', dict(view='front', s=0.6, light='night')),
 ('him', dict(view='side', s=0.6, light='night', walk=0.5)),
 ('her', dict(view='front', s=0.6, light='night', style='now')),
 ('him', dict(view='side', s=0.6, light='night', head_back=True, walk=0.1)),
 ('her', dict(view='side', s=0.6, light='warm', sit=True)),
 ('him', dict(view='side', s=0.6, light='warm', sit=True, hand_r=(10,62))),
]
for who, kw in items2:
    spr, anc = (HIM if who=='him' else HER)(**kw)
    place(img, spr, anc, x, 300)
    x += 52
spr, anc = HIM(view='front', s=2.2, light='night', mouth='sad', eyes='open', tear=0.3)
place(img, spr, anc, 430, 470)
spr, anc = HER(view='front', s=2.2, light='warm', style='memory', mouth='smile', dimple=True)
place(img, spr, anc, 560, 470)
save_png(img, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'out', 'chars_sheet.png'), 2)
