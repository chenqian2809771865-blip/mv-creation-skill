# story.py: the shot table. Shot functions live in story_a.py (S01–S08), story_b.py (S09–S16), story_c.py (S17–S24), story_d.py (S25–S32).
from common import SB
import story_a, story_b, story_c, story_d
FN = {}
for mod in (story_a, story_b, story_c, story_d):
    for k in dir(mod):
        if k.startswith('s') and k[1:].isdigit():
            FN['S%02d' % int(k[1:])] = getattr(mod, k)


def _missing(t, lt, dur):
    from eng import flatRect, W, H
    flatRect(-80, -80, W + 160, H + 160, '#808080')


SHOTS = [(r['t0'], FN.get(r['id'], _missing), r['transition'], r['id']) for r in SB['shots']]
