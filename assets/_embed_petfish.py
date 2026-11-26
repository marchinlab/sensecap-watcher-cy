#!/usr/bin/env python3
"""把 petfish 鲸鱼娘裁成圆形并 base64 内嵌到 banner.svg / watch-states.svg。

README 用 <img src="*.svg"> 引用，浏览器图片模式禁止 SVG 加载外部图片，
所以角色图必须 data URI 内嵌。改图只需改下面的 PICKS 再跑本脚本。
"""
import base64
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent

# (源文件, 取景框 原图320x320, 输出边长)
PICKS = {
    "banner":  ("fish_01.webp", (60, 10, 260, 210), 260),
    "idle":    ("fish_13.webp", (60, 12, 260, 212), 196),
    "listen":  ("fish_06.webp", (60, 12, 260, 212), 196),
    "speak":   ("fish_17.webp", (60, 12, 260, 212), 196),
}


def circle_data(name):
    src, box, size = PICKS[name]
    im = Image.open(ROOT / "petfish" / src).convert("RGBA").crop(box)
    im = im.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    im.putalpha(mask)
    out = ROOT / ("_tmp_" + name + ".png")
    im.save(out, optimize=True)
    data = base64.b64encode(out.read_bytes()).decode("ascii")
    out.unlink()
    return "data:image/png;base64," + data


def main():
    uris = {k: circle_data(k) for k in PICKS}

    # 1) banner.svg：替换右侧整个圆屏<g>（保留外圈细线，删几何眼，放角色）
    p = ROOT / "banner.svg"
    s = p.read_text(encoding="utf-8")
    start = s.index('  <!-- 右侧：极简圆屏')
    end = s.index('  <!-- 底部基线 -->')
    b = int(PICKS["banner"][2])
    block = f'''  <!-- 右侧：桌宠鲸鱼娘待机屏（fish_01，圆形内嵌） -->
  <g transform="translate(950 220)">
    <circle r="164" fill="none" stroke="#ded9cd" stroke-width="1"/>
    <circle r="150" fill="none" stroke="#2f2d29" stroke-width="1.5"/>
    <circle r="132" fill="#fbfaf6" stroke="#ded9cd" stroke-width="1"/>
    <image href="{uris['banner']}" x="{-b//2}" y="{-b//2}" width="{b}" height="{b}" preserveAspectRatio="xMidYMid slice"/>
    <circle r="132" fill="none" stroke="#ded9cd" stroke-width="1"/>
    <text x="-112" y="-96" class="m" font-size="9" fill="#8d887e">01 / 37</text>
    <text x="112" y="-96" class="m" font-size="9" fill="#8d887e" text-anchor="end">LIVE</text>
    <rect x="-64" y="96" width="128" height="20" fill="#fbfaf6" fill-opacity=".88"/>
    <text x="0" y="110" class="m" font-size="10" fill="#8d887e" text-anchor="middle" letter-spacing="1">播报 · 早报 03</text>
  </g>

'''
    s = s[:start] + block + s[end:]
    p.write_text(s, encoding="utf-8")

    # 2) watch-states.svg：三态圆内几何眼 → 角色图
    p = ROOT / "watch-states.svg"
    s = p.read_text(encoding="utf-8")
    repos = [
        ("  <!-- 待机 -->", "  <!-- 聆听 -->", "idle", 200, "待机", "樱花浅笑 · 安静待机"),
        ("  <!-- 聆听 -->", "  <!-- 播报 -->", "listen", 600, "聆听", "大眼捂脸 · 瞳孔朝声源"),
        ("  <!-- 播报 -->", "  <line x1=\"60\" y1=\"398\"", "speak", 1000, "播报", "眨眼微笑 · 句末眨眼"),
    ]
    for mark, nextmark, key, cx, label, desc in repos:
        a = s.index(mark)
        z = s.index(nextmark, a + len(mark))
        tpl = (f'{mark}\n'
               f'  <g transform="translate({cx} 190)">\n'
               '    <circle r="112" fill="none" stroke="#ded9cd" stroke-width="1"/>\n'
               '    <circle r="98" fill="#fbfaf6" stroke="#2f2d29" stroke-width="1.5"/>\n'
               '    <image href="{u}" x="-96" y="-96" width="192" height="192"/>\n'
               '    <circle r="98" fill="none" stroke="#2f2d29" stroke-width="1.5"/>\n'
               '  </g>\n'
               f'  <text x="{cx}" y="336" class="h" font-size="15" font-weight="600" fill="#2f2d29" text-anchor="middle">{label}</text>\n'
               f'  <text x="{cx}" y="362" class="h" font-size="12" fill="#8d887e" text-anchor="middle">{desc}</text>\n\n')
        s = s[:a] + tpl.format(u=uris[key]) + s[z:]
    p.write_text(s, encoding="utf-8")

    for name, u in uris.items():
        print(name, len(u), "bytes base64")


if __name__ == "__main__":
    main()
