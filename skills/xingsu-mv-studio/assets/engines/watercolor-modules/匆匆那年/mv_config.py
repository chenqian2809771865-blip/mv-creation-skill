"""读取用户配置的片头署名；可随代码复制到新工程。"""
import json
import os
import inspect
from pathlib import Path


def load_signature():
    """优先使用 MV_SIGNATURE；否则向上查找技能或工程的 config.json。"""
    value = os.environ.get('MV_SIGNATURE', '').strip()
    if not value:
        starts = [Path(__file__).resolve().parent, Path.cwd()]
        frame = inspect.currentframe().f_back
        if frame is not None:
            starts.insert(0, Path(frame.f_code.co_filename).resolve().parent)
        for start in starts:
            for folder in (start, *start.parents):
                config = folder / 'config.json'
                if config.is_file():
                    value = str(json.loads(config.read_text(encoding='utf-8')).get('SIGNATURE', '')).strip()
                    break
            if value:
                break
    if not value or value in ('★你的署名', '你的署名'):
        raise ValueError('尚未配置片头署名：请先询问用户，在 config.json 的 SIGNATURE 或环境变量 MV_SIGNATURE 中设置。')
    return value
