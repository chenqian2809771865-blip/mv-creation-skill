# items.py: hand-held props for 阿屿 (drawn at the hand, local unit coords)
import math
from eng import *
from ayu import AYU, _P, part, bottle


def item_bottle(s=1.0, glowK=0, rot=0):
    def f(u, sw, C):
        push()
        rotate(rot)
        translate(.15 * u, -.9 * u * s)
        bottle(u, sw, C, s, glowK=glowK)
        pop()
    return f


def item_scope(u, sw, C):
    """brass spyglass pointing right, eyepiece at the hand"""
    segs = [(0, 1.9, .42, '#C9A24E'), (1.8, 3.6, .52, '#B48A3A'), (3.5, 5.3, .64, '#C9A24E')]
    for a, b, r, col in segs:
        part(_P([[a, -r], [b, -r], [b, r], [a, r]], u), col, mixCol(col, INK, .3), '#F1D58C', sd=(0, .6), sw=sw * .6, curv=False)
    paint(ellPts(5.3 * u, 0, .2 * u, .64 * u, 12), wash='#9FD0E8', ink=INK, sw=sw * .5)


def item_bowl(u, sw, C):
    pts = [[-1.5, -.6], [1.5, -.6], [1.15, .55], [-1.15, .55]]
    part(_P(pts, u), '#B9C0C8', '#7E8792', '#EEF2F5', sd=(.4, .5), sw=sw * .7, curv=False)
    paint(ellPts(0, -.6 * u, 1.5 * u, .32 * u, 16), wash='#8E97A2', ink=INK, sw=sw * .5)


def item_cone(melt=0.0):
    """ice-cream Earth on a cone — continents melting into drips"""
    def f(u, sw, C):
        push()
        translate(0, -.4 * u)
        part(_P([[-.85, -.6], [.85, -.6], [0, 2.2]], u), '#E2B36A', '#B78434', None, sw=sw * .6, curv=False)
        for k in range(3):
            inkLine(_P([[-.6 + k * .45, -.5], [.1 + k * .2, 1.4]], u), sw * .3, '#B78434', 'inkfine', 0)
        part(ellPts(0, -1.55 * u, 1.25 * u, 1.15 * u, 22), '#5FA3D6', '#3B75A8', '#BFE0F5', sd=(.5, .4), sw=sw * .7)
        paint(_P([[-.7, -2.1], [-.1, -2.4], [.2, -1.9], [-.3, -1.4], [-.8, -1.6]], u), wash='#7DB46A', ink=None)
        paint(_P([[.3, -1.3], [.9, -1.6], [1.0, -1.0], [.5, -.8]], u), wash='#7DB46A', ink=None)
        for i, dx in enumerate((-.75, .05, .7)):
            L = (.5 + .5 * hash1(i + 3)) * (.4 + melt * 1.4)
            paint(ribbon(_P([[dx, -.6], [dx + .03, -.6 + L * .6], [dx, -.6 + L]], u), .32 * u, .22 * u), wash='#5FA3D6', ink=INK, sw=sw * .35)
        pop()
    return f


def item_photo(u, sw, C):
    push()
    rotate(-.12)
    paint(_P([[-.2, -2.3], [2.4, -2.3], [2.4, -.2], [-.2, -.2]], u), wash='#FBF3DE', ink=INK, sw=sw * .55)
    paint(_P([[.05, -2.05], [2.15, -2.05], [2.15, -.75], [.05, -.75]], u), wash='#7FD0E0', ink=None)
    paint(_P([[.05, -1.2], [2.15, -1.2], [2.15, -.75], [.05, -.75]], u), wash='#3E9FC0', ink=None)
    paint(ellPts(1.1 * u, -1.22 * u, .55 * u, .2 * u, 12), wash='#F2E2B0', ink=None)
    inkLine(_P([[1.0, -1.25], [1.12, -1.75]], u), sw * .35, '#7A5A3A', 'inkfine', .3)
    paint(ellPts(1.12 * u, -1.8 * u, .32 * u, .14 * u, 8), wash='#6EA85A', ink=None)
    pop()


def hatAlone(x, y, u, sw, old=False, view='front'):
    """draw just the bucket hat with its brim centre at (x, y)"""
    from ayu import hatShape
    push()
    translate(x, y + 16.1 * u)
    hatShape(u, sw, AYU, view, old=old)
    pop()
