#!/usr/bin/env python3
"""Fetch the fonts the bundled engines expect (they are not shipped with the skill because of size).

usage: python3 get_fonts.py DEST [--unifont] [--fp12] [--wenkai] [--all]

  --unifont  GNU Unifont 16px (npm @fontpkg/unifont)              -> DEST/unifont.ttf
  --fp12     Fusion Pixel 12px proportional zh_hans, split woff2   -> DEST/fp12/*.ttf + DEST/fp12/cmap.json
             (npm @vp-tw/cjk-web-fonts-fusion-pixel-font; converted with fontTools, needs brotli)
  --wenkai   LXGW WenKai Regular (raw.githubusercontent.com)       -> DEST/LXGWWenKai-Regular.ttf

Where each engine looks:
  pixel-320-couple   <project>/fonts/unifont.ttf and fonts/fp12/  (or MV_FONT_DIR)  -> get_fonts.py <project>/fonts --unifont --fp12
  pixel-640       <project>/assets/unifont.ttf                                   -> get_fonts.py <project>/assets --unifont
  watercolor      <project>/fonts/ (ZCOOL KuaiLe is bundled; WenKai for wtext)   -> get_fonts.py <project>/fonts --wenkai
Licences: Unifont GPL-2.0+ with font embedding exception / OFL; Fusion Pixel OFL-1.1; LXGW WenKai OFL-1.1.
"""
import argparse
import glob
import json
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.request

WENKAI = 'https://raw.githubusercontent.com/lxgw/LxgwWenKai/main/fonts/TTF/LXGWWenKai-Regular.ttf'


def npm_unpack(pkg, tmp):
    """通过 npm 注册表下载字体包；字体流程无需安装 Node.js。"""
    metadata_url = 'https://registry.npmjs.org/' + pkg.replace('/', '%2f') + '/latest'
    with urllib.request.urlopen(metadata_url) as response:
        metadata = json.load(response)
    archive = os.path.join(tmp, 'font-package.tgz')
    urllib.request.urlretrieve(metadata['dist']['tarball'], archive)
    destination = os.path.abspath(os.path.join(tmp, pkg.replace('/', '_')))
    os.makedirs(destination, exist_ok=True)
    with tarfile.open(archive) as bundle:
        for member in bundle.getmembers():
            target = os.path.abspath(os.path.join(destination, member.name))
            if os.path.commonpath([destination, target]) != destination:
                raise ValueError('字体包中含越界路径')
            if not (member.isdir() or member.isfile()):
                raise ValueError('字体包中含不支持的链接或特殊文件')
            if member.isdir():
                os.makedirs(target, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with bundle.extractfile(member) as source, open(target, 'wb') as output:
                    shutil.copyfileobj(source, output)
    return os.path.join(destination, 'package')


def unifont(dest, tmp):
    src = glob.glob(os.path.join(npm_unpack('@fontpkg/unifont', tmp), '*.ttf'))[0]
    shutil.copy(src, os.path.join(dest, 'unifont.ttf'))
    print('unifont ->', os.path.join(dest, 'unifont.ttf'))


def fp12(dest, tmp):
    try:
        from fontTools.ttLib import TTFont
        import brotli  # noqa: F401  (woff2 decompression)
    except ImportError:
        sys.exit('python3 -m pip install fonttools brotli')
    root = npm_unpack('@vp-tw/cjk-web-fonts-fusion-pixel-font', tmp)
    files = sorted(glob.glob(os.path.join(root, 'dist', '12px', 'proportional', 'zh_hans', '*.woff2')))
    if not files:
        sys.exit('no 12px proportional zh_hans woff2 files in the package (layout changed?)')
    out = os.path.join(dest, 'fp12')
    os.makedirs(out, exist_ok=True)
    cmap = {}
    for f in files:
        name = os.path.basename(f)[:-6] + '.ttf'
        font = TTFont(f)
        font.flavor = None
        font.save(os.path.join(out, name))
        for cp in font.getBestCmap():
            cmap.setdefault(str(cp), name)
    json.dump(cmap, open(os.path.join(out, 'cmap.json'), 'w'))
    print('fp12 -> %s (%d files, %d code points)' % (out, len(files), len(cmap)))


def wenkai(dest):
    path = os.path.join(dest, 'LXGWWenKai-Regular.ttf')
    urllib.request.urlretrieve(WENKAI, path + '.part')
    os.replace(path + '.part', path)
    print('wenkai ->', path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('dest')
    for k in ('unifont', 'fp12', 'wenkai', 'all'):
        ap.add_argument('--' + k, action='store_true')
    a = ap.parse_args()
    if not (a.unifont or a.fp12 or a.wenkai or a.all):
        ap.error('choose --unifont / --fp12 / --wenkai / --all')
    os.makedirs(a.dest, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        if a.unifont or a.all:
            unifont(a.dest, tmp)
        if a.fp12 or a.all:
            fp12(a.dest, tmp)
        if a.wenkai or a.all:
            wenkai(a.dest)


if __name__ == '__main__':
    main()
