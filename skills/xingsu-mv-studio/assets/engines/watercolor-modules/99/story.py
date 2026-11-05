# story.py: 《99》 (TizzyT) shot table. Shot functions live in story1 (S01–S13) and story2 (S14–S25); data: storyboard.py.
from common import SB
import story1, story2

_FN = {}
for i in range(1, 26):
    sid = f'S{i:02d}'
    mod = story1 if i <= 13 else story2
    _FN[sid] = getattr(mod, f's{i:02d}')
SHOTS = []
for s in SB['shots']:
    SHOTS.append((s['start'], _FN[s['id']], s['tr'], s['id']))
