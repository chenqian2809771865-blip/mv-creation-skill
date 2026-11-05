# story.py: 《罗生门》 shot table. Shot functions: story_a (S01–S07 intro + first line), story_b (S08–S26 chorus 1 + verse 1, his version),
# story_c (S27–S53 chorus 2, bridge, verse 2 her version, chorus 3, outro); data: storyboard.py.
from common import SB
import story_a, story_b, story_c

MODS = (story_a, story_b, story_c)
SHOTS = []
for s in SB['shots']:
    fn = None
    for m in MODS:
        fn = getattr(m, s['id'].lower(), None)
        if fn:
            break
    SHOTS.append((s['start'], fn or story_a.placeholder, s['tr'], s['id']))
