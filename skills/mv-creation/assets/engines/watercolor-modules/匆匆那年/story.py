# story.py: 《匆匆那年》 shot table. Shot functions: story_a (S01–S03 intro), story_b (S04–S22), story_c (S23–S31 his side),
# story_d (S32–S44 ten years later, the end); data: storyboard.py.
from common import SB
import story_a, story_b, story_c, story_d

MODS = (story_a, story_b, story_c, story_d)
SHOTS = []
for s in SB['shots']:
    fn = None
    for m in MODS:
        fn = getattr(m, s['id'].lower(), None)
        if fn:
            break
    SHOTS.append((s['start'], fn or story_a.placeholder, s['tr'], s['id']))
