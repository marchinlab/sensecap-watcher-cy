# -*- coding: utf-8 -*-
"""
生成展示页用的「手表圆屏界面效果图」SVG。
风格：奶油纸卡面 + 深色圆屏（还原真机），矢量可版本化。
运行：python _gen_screens.py
"""
import math, os

OUT = os.path.dirname(os.path.abspath(__file__))

# 真机圆屏：外框 412，屏幕半径约 196，中心 220
C = 220
R = 196
FONT = "'Microsoft YaHei','PingFang SC',sans-serif"
MONO = 'ui-monospace,Consolas,monospace'


def wrap(inner, title):
    """瑞士风白底卡面 + 深色表壳 + 圆屏裁剪（圆屏内部仍是真实界面还原）"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 476" width="440" height="476" role="img" aria-label="{title}">
<defs>
  <radialGradient id="bezel" cx="42%" cy="34%" r="72%">
    <stop offset="0%" stop-color="#4a4640"/><stop offset="62%" stop-color="#26231f"/><stop offset="100%" stop-color="#0e0d0b"/>
  </radialGradient>
  <clipPath id="scr"><circle cx="{C}" cy="{C}" r="{R}"/></clipPath>
</defs>
<rect width="440" height="476" fill="#ffffff"/>
<rect x="8" y="8" width="424" height="460" fill="none" stroke="#dcdcd8" stroke-width="1"/>
<rect x="8" y="8" width="56" height="5" fill="#e2231a"/>
<circle cx="{C}" cy="{C}" r="212" fill="url(#bezel)"/>
<circle cx="{C}" cy="{C}" r="204" fill="#000" opacity=".55"/>
<circle cx="{C}" cy="{C}" r="{R+3}" fill="none" stroke="#070707" stroke-width="2"/>
<g clip-path="url(#scr)">
{inner}
</g>
<circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="#3a352e" stroke-width="3"/>
<line x1="24" y1="440" x2="416" y2="440" stroke="#111111" stroke-width="1"/>
<text x="24" y="459" text-anchor="start" font-family="{MONO}" font-size="11" letter-spacing="1" fill="#8c8c8c">{title}</text>
</svg>'''


def radar():
    """v1.7.48 龙珠风航班雷达：方格网 + 同心圆 + 方位刻度 + 扫描扇形 + 飞机光点"""
    p = [f'<rect x="0" y="0" width="440" height="440" fill="#061a10"/>']
    # 方格网
    for i in range(0, 440, 26):
        p.append(f'<line x1="{i}" y1="0" x2="{i}" y2="440" stroke="#0e3320" stroke-width="1"/>')
        p.append(f'<line x1="0" y1="{i}" x2="440" y2="{i}" stroke="#0e3320" stroke-width="1"/>')
    # 同心圆
    for r in (48, 96, 144, 190):
        p.append(f'<circle cx="{C}" cy="{C}" r="{r}" fill="none" stroke="#1d5c39" stroke-width="1.5"/>')
    # 十字
    p.append(f'<line x1="{C}" y1="24" x2="{C}" y2="416" stroke="#1d5c39" stroke-width="1.5"/>')
    p.append(f'<line x1="24" y1="{C}" x2="416" y2="{C}" stroke="#1d5c39" stroke-width="1.5"/>')
    # 12 方位刻度
    for k in range(12):
        a = math.radians(k * 30 - 90)
        x1, y1 = C + 182 * math.cos(a), C + 182 * math.sin(a)
        x2, y2 = C + 192 * math.cos(a), C + 192 * math.sin(a)
        p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#2f8a55" stroke-width="2.5"/>')
    # 扫描扇形拖尾（14 条渐隐）
    for k in range(14):
        a0 = math.radians(-90 - k * 3.2)
        a1 = math.radians(-90 - (k + 1) * 3.2)
        op = 0.30 * (1 - k / 14)
        x0, y0 = C + 190 * math.cos(a0), C + 190 * math.sin(a0)
        x1, y1 = C + 190 * math.cos(a1), C + 190 * math.sin(a1)
        p.append(f'<path d="M{C} {C} L{x0:.1f} {y0:.1f} A190 190 0 0 0 {x1:.1f} {y1:.1f} Z" fill="#6dffb0" opacity="{op:.3f}"/>')
    a = math.radians(-90)
    p.append(f'<line x1="{C}" y1="{C}" x2="{C+190*math.cos(a):.1f}" y2="{C+190*math.sin(a):.1f}" stroke="#b6ffd2" stroke-width="5"/>')
    # 飞机光点（角度/半径/呼号）
    planes = [(-58,95,'CCA1324'),(22,120,'CSN3612'),(128,78,'UAL889'),(178,140,'CPA52'),
              (-132,150,'CES5703'),(72,52,'HNA7231'),(-24,68,'CSZ9931'),(150,168,'FDX5910'),
              (-96,72,'CKK208'),(40,168,'CHH7521'),(-170,118,'AIC312'),(108,128,'JAL620'),
              (-52,178,'KLM889'),(190,100,'SIA863'),(-150,180,'THY68'),(84,182,'DHL721')]
    for deg, rr, call in planes:
        ang = math.radians(deg - 90)
        x, y = C + rr * math.cos(ang), C + rr * math.sin(ang)
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#eaff7a" opacity=".22"/>')
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#f4ff9a" stroke="#0a2a16" stroke-width="1"/>')
        p.append(f'<text x="{x+7:.1f}" y="{y-6:.1f}" font-family="{MONO}" font-size="9" fill="#c7f5d4">{call}</text>')
    # 中心黄色指向三角
    p.append(f'<path d="M{C} {C-16} L{C+12} {C+12} L{C} {C+5} L{C-12} {C+12} Z" fill="#ffd23f" stroke="#0a2a16" stroke-width="1.5"/>')
    # 顶部标题
    p.append(f'<text x="{C}" y="72" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="bold" fill="#d9ffe6">广州白云 · 16 架</text>')
    p.append(f'<line x1="150" y1="82" x2="290" y2="82" stroke="#2f8a55" stroke-width="1"/>')
    # 底部比例尺
    p.append(f'<line x1="{C-50}" y1="386" x2="{C+50}" y2="386" stroke="#7fdca0" stroke-width="2"/>')
    p.append(f'<line x1="{C-50}" y1="382" x2="{C-50}" y2="390" stroke="#7fdca0" stroke-width="2"/>')
    p.append(f'<line x1="{C+50}" y1="382" x2="{C+50}" y2="390" stroke="#7fdca0" stroke-width="2"/>')
    p.append(f'<text x="{C}" y="378" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#7fdca0">50 km</text>')
    return wrap('\n'.join(p), '航班雷达 · 龙珠盘面 v1.7.48')


def lyrics():
    """v1.7.50 满屏歌词：封面 + 歌名 + 5 行滚动 + 进度条"""
    p = [f'<rect x="0" y="0" width="440" height="440" fill="#12100e"/>']
    # 顶部封面（渐变方块）
    p.append('<defs><linearGradient id="cov" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5b3a6e"/><stop offset="1" stop-color="#b4562f"/></linearGradient></defs>')
    p.append(f'<rect x="{C-46}" y="54" width="92" height="92" rx="12" fill="url(#cov)"/>')
    p.append(f'<circle cx="{C}" cy="100" r="24" fill="#000" opacity=".35"/>')
    p.append(f'<circle cx="{C}" cy="100" r="9" fill="#f0e2c8" opacity=".8"/>')
    # 歌名（双标签叠印模拟加粗）
    p.append(f'<text x="{C+1}" y="171" text-anchor="middle" font-family="{FONT}" font-size="21" fill="#fff3e0">情歌王</text>')
    p.append(f'<text x="{C}" y="170" text-anchor="middle" font-family="{FONT}" font-size="21" font-weight="bold" fill="#fff3e0">情歌王</text>')
    p.append(f'<text x="{C}" y="192" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#9a8e7e">王菲 · 1995 最精彩演唱会</text>')
    p.append(f'<line x1="112" y1="205" x2="328" y2="205" stroke="#3a332b" stroke-width="1"/>')
    # 5 行歌词，第 2 行高亮
    lines = [('如果 我 没有 遇见 你', '#6f665a', 15),
             ('也许 我 会 在 人群 里', '#ffcf6a', 18),
             ('寻 找 一个 相似 的 背影', '#6f665a', 15),
             ('把 每 一 句 爱 的 诺 言', '#6f665a', 15),
             ('都 藏 进 歌 里 慢慢 唱', '#6f665a', 15)]
    for i, (t, col, sz) in enumerate(lines):
        y = 240 + i * 33
        if i == 1:
            p.append(f'<rect x="96" y="{y-24}" width="248" height="32" rx="8" fill="#ffcf6a" opacity=".08"/>')
        p.append(f'<text x="{C}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{sz}" fill="{col}">{t}</text>')
    # 进度条 + 时间
    p.append(f'<rect x="72" y="386" width="296" height="5" rx="2.5" fill="#3a332b"/>')
    p.append(f'<rect x="72" y="386" width="112" height="5" rx="2.5" fill="#ffcf6a"/>')
    p.append(f'<circle cx="184" cy="388.5" r="6" fill="#ffcf6a"/>')
    p.append(f'<text x="72" y="404" font-family="{MONO}" font-size="10" fill="#8d8071">02:14</text>')
    p.append(f'<text x="368" y="404" text-anchor="end" font-family="{MONO}" font-size="10" fill="#8d8071">04:36</text>')
    return wrap('\n'.join(p), '满屏歌词 · 跟设备真实进度 v1.7.51')


def board():
    """v1.7.65 WorkBuddy 看板：蓝色圆形底板 + 真实数据行"""
    p = [f'<rect x="0" y="0" width="440" height="440" fill="#0d1830"/>']
    # 蓝色圆形底板
    p.append('<defs><radialGradient id="bd" cx="45%" cy="35%" r="75%"><stop offset="0" stop-color="#24457e"/><stop offset="1" stop-color="#12224a"/></radialGradient></defs>')
    p.append(f'<circle cx="{C}" cy="{C}" r="{R}" fill="url(#bd)" stroke="#3a63a8" stroke-width="2"/>')
    # 抬头
    p.append(f'<text x="96" y="86" font-family="{MONO}" font-size="18" font-weight="bold" fill="#eaf1ff">CY·PRO</text>')
    p.append(f'<text x="344" y="86" text-anchor="end" font-family="{MONO}" font-size="15" fill="#9fc0f0">54%</text>')
    p.append(f'<line x1="96" y1="98" x2="344" y2="98" stroke="#3a63a8" stroke-width="1"/>')
    # 上下文大字
    p.append(f'<text x="96" y="128" font-family="{FONT}" font-size="14" fill="#9fc0f0">上下文用量</text>')
    p.append(f'<text x="96" y="168" font-family="{MONO}" font-size="34" font-weight="bold" fill="#ffd23f">47%</text>')
    p.append(f'<text x="344" y="166" text-anchor="end" font-family="{MONO}" font-size="13" fill="#9fc0f0">141k/300k</text>')
    p.append(f'<rect x="96" y="180" width="248" height="6" rx="3" fill="#1b2c55"/>')
    p.append(f'<rect x="96" y="180" width="117" height="6" rx="3" fill="#ffd23f"/>')
    # 数据行
    rows = [('● 今日额度消耗', '9435', 222),
            ('● 累计额度消耗', '13883', 252),
            ('● 今日会话', '6', 282),
            ('TTS 本月', '19%', 312)]
    for label, val, y in rows:
        p.append(f'<text x="96" y="{y}" font-family="{FONT}" font-size="15" fill="#c9d9f5">{label}</text>')
        p.append(f'<text x="344" y="{y}" text-anchor="end" font-family="{MONO}" font-size="17" font-weight="bold" fill="#eaf1ff">{val}</text>')
    p.append(f'<line x1="96" y1="330" x2="344" y2="330" stroke="#3a63a8" stroke-width="1"/>')
    p.append(f'<text x="96" y="356" font-family="{FONT}" font-size="13" fill="#7fa8e8">● 实时同步</text>')
    # Q 版示意（右下）
    p.append(f'<circle cx="316" cy="356" r="20" fill="#d9c9f0" opacity=".9"/>')
    p.append(f'<circle cx="310" cy="352" r="2.6" fill="#2b2723"/><circle cx="322" cy="352" r="2.6" fill="#2b2723"/>')
    p.append(f'<path d="M311 362 Q316 367 321 362" stroke="#2b2723" stroke-width="1.6" fill="none"/>')
    return wrap('\n'.join(p), 'WorkBuddy 工作状态看板 v1.7.65')


def radio():
    """常听电台列表：编号 + 台名 + 当前播放高亮"""
    p = [f'<rect x="0" y="0" width="440" height="440" fill="#10140f"/>']
    p.append(f'<text x="{C}" y="70" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="bold" fill="#f5e8c8">收音机 · 常听 11 台</text>')
    p.append(f'<line x1="88" y1="82" x2="352" y2="82" stroke="#4a5c3a" stroke-width="1"/>')
    stations = [('1','香港电台第一台','RTHK 1'),('2','香港电台第二台','RTHK 2'),
                ('3','香港电台第五台','RTHK 5'),('7','BBC World Service','BBC'),
                ('8','Classic FM','Classic'),('12','Radio Paradise','Paradise')]
    for i, (num, name, alias) in enumerate(stations):
        y = 118 + i * 42
        hot = (i == 1)
        if hot:
            p.append(f'<rect x="66" y="{y-26}" width="308" height="36" rx="9" fill="#b4562f" opacity=".22"/>')
            p.append(f'<rect x="66" y="{y-26}" width="3" height="36" rx="1.5" fill="#e07a45"/>')
        p.append(f'<text x="84" y="{y}" font-family="{MONO}" font-size="14" fill="{("#ffcf6a" if hot else "#8d8071")}">{num}</text>')
        p.append(f'<text x="112" y="{y}" font-family="{FONT}" font-size="15" fill="{("#fff3e0" if hot else "#c9c0ae")}">{name}</text>')
        p.append(f'<text x="356" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11" fill="#8d8071">{alias}</text>')
    # 底部波形
    p.append(f'<line x1="88" y1="380" x2="352" y2="380" stroke="#4a5c3a" stroke-width="1"/>')
    for i in range(28):
        h = 4 + 12 * abs(math.sin(i * 0.9))
        x = 94 + i * 9.5
        p.append(f'<rect x="{x:.1f}" y="{382-4:.1f}" width="3" height="{h:.1f}" rx="1.5" fill="#7fdca0" opacity=".7"/>')
    p.append(f'<text x="{C}" y="406" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#8d8071">正在播放 · 香港电台第二台</text>')
    return wrap('\n'.join(p), '常听电台列表 · 11 台编号')


def camera():
    """拍照识别：取景框 + 识别结果"""
    p = [f'<rect x="0" y="0" width="440" height="440" fill="#141210"/>']
    p.append(f'<text x="{C}" y="66" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="bold" fill="#f5e8c8">睇下呢个</text>')
    # 取景框四角
    for (x1,y1,x2,y2) in [(70,92,70,122),(70,92,100,92),(370,92,370,122),(370,92,340,92),
                          (70,300,70,270),(70,300,100,300),(370,300,370,270),(370,300,340,300)]:
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8fd6a0" stroke-width="3"/>')
    # 场景色块（模拟食物）
    p.append('<defs><linearGradient id="food" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9a86a"/><stop offset="1" stop-color="#7a4a2f"/></linearGradient></defs>')
    p.append(f'<ellipse cx="{C}" cy="206" rx="82" ry="58" fill="url(#food)"/>')
    p.append(f'<ellipse cx="{C}" cy="196" rx="66" ry="40" fill="#e8c48a" opacity=".7"/>')
    for i in range(9):
        a = i * 0.7
        p.append(f'<circle cx="{C+34*math.cos(a):.1f}" cy="{196+20*math.sin(a):.1f}" r="7" fill="#5c7a3a" opacity=".8"/>')
    # 识别结果条
    p.append(f'<rect x="62" y="320" width="316" height="76" rx="12" fill="#0c1f14" stroke="#2f8a55" stroke-width="1.5"/>')
    p.append(f'<text x="80" y="348" font-family="{FONT}" font-size="17" font-weight="bold" fill="#d9ffe6">车仔面 · 约 520 kcal</text>')
    p.append(f'<text x="80" y="374" font-family="{FONT}" font-size="12" fill="#8fd6a0">蛋白质 24g · 碳水 61g · 脂肪 18g</text>')
    return wrap('\n'.join(p), '拍照识别 · 食物热量 v1.7.14')


def failover():
    """云端主备流程：本机 owner + 云端 standby + 心跳接管"""
    W, H = 900, 340
    p = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="#dcdcd8" stroke-width="1"/>',
         f'<rect x="8" y="8" width="56" height="5" fill="#e2231a"/>']
    p.append(f'<text x="450" y="46" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="bold" fill="#111111">本机全量生产 · 云端待命接管</text>')
    # 手机/设备
    p.append(f'<rect x="40" y="150" width="130" height="72" rx="12" fill="#2f6b62"/>')
    p.append(f'<text x="105" y="182" text-anchor="middle" font-family="{FONT}" font-size="15" fill="#fff">手表 / 手机</text>')
    p.append(f'<text x="105" y="204" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#cfe6e0">设备轮询</text>')
    # 本机 owner
    p.append(f'<rect x="300" y="110" width="240" height="112" rx="14" fill="#b4562f"/>')
    p.append(f'<text x="420" y="146" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="bold" fill="#fff">本机 owner</text>')
    p.append(f'<text x="420" y="172" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#ffe6d0">localAll=true · 家用内网地址</text>')
    p.append(f'<text x="420" y="196" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#ffe6d0">在线即抑制云端 4 处生产</text>')
    # 云端 standby
    p.append(f'<rect x="650" y="150" width="210" height="72" rx="12" fill="#35507a"/>')
    p.append(f'<text x="755" y="182" text-anchor="middle" font-family="{FONT}" font-size="15" fill="#fff">云端 standby</text>')
    p.append(f'<text x="755" y="204" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#cfe0f5">standbyRole=true</text>')
    # 箭头：设备→本机
    p.append(f'<path d="M170 186 L292 166" stroke="#5d5347" stroke-width="2" fill="none" marker-end="url(#ar)"/>')
    p.append(f'<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#5d5347"/></marker></defs>')
    # 心跳线
    p.append(f'<path d="M540 150 Q600 96 650 150" stroke="#2f6b62" stroke-width="2" fill="none" stroke-dasharray="5 4" marker-end="url(#ar)"/>')
    p.append(f'<text x="596" y="102" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#2f6b62">心跳 10s (带 maxId)</text>')
    # 接管说明
    p.append(f'<rect x="290" y="250" width="320" height="56" rx="10" fill="#f2e8d3" stroke="#d8c9a8"/>')
    p.append(f'<text x="450" y="274" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#5d5347">60s 无心跳 → 云端接管播报与播放</text>')
    p.append(f'<text x="450" y="294" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#5d5347">本机回来 → 让位并回灌新增消息（不覆盖文件）</text>')
    p.append(f'<path d="M755 222 Q700 290 610 278" stroke="#35507a" stroke-width="2" fill="none" stroke-dasharray="5 4" marker-end="url(#ar)"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="本机云端主备流程">\n' + '\n'.join(p) + '\n</svg>'


def route():
    """高德路线规划：问路线默认公交优先，播报可直接念"""
    p = [f'<rect x="0" y="0" width="440" height="440" fill="#101a24"/>']
    # 简化路网底纹
    for x in range(20, 440, 44):
        p.append(f'<line x1="{x}" y1="24" x2="{x-28}" y2="416" stroke="#1b2b3a" stroke-width="1"/>')
    for y in range(48, 440, 52):
        p.append(f'<line x1="24" y1="{y}" x2="416" y2="{y}" stroke="#1b2b3a" stroke-width="1"/>')
    # 一条河
    p.append('<path d="M24 292 Q140 256 248 316 Q340 364 416 326" fill="none" stroke="#16384b" stroke-width="13"/>')
    # 地铁折线：1 号线（绿）→ 2 号线（蓝）
    p.append('<path d="M96 142 L176 142 L176 224 L278 224" fill="none" stroke="#6fd08c" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append('<path d="M278 224 L278 292 L344 292" fill="none" stroke="#5aa9f0" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    stops = [(96,142),(176,142),(176,224),(278,224),(278,292),(344,292)]
    for x, y in stops:
        p.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#101a24" stroke-width="2"/>')
    # 起终点
    p.append(f'<circle cx="96" cy="142" r="13" fill="#2f6b62" stroke="#fff" stroke-width="2"/>')
    p.append(f'<circle cx="344" cy="292" r="13" fill="#b4562f" stroke="#fff" stroke-width="2"/>')
    p.append(f'<text x="96" y="146" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#fff">起</text>')
    p.append(f'<text x="344" y="296" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#fff">终</text>')
    # 换乘标记
    p.append(f'<circle cx="278" cy="224" r="10" fill="#ffd23f" stroke="#101a24" stroke-width="2"/>')
    p.append(f'<text x="278" y="228" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#3b2c00">换</text>')
    # 顶部标题
    p.append(f'<text x="{C}" y="70" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="bold" fill="#eaf6ff">路线规划 · 公交优先</text>')
    p.append(f'<text x="{C}" y="94" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#a9c3d8">天河城 → 广州南站</text>')
    # 站点名
    p.append(f'<text x="96" y="126" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#9fc7e0">天河城</text>')
    p.append(f'<text x="334" y="314" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#9fc7e0">广州南站</text>')
    p.append(f'<text x="278" y="212" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#ffd23f">换乘</text>')
    # 方案卡（往圆屏安全区收窄，避免左右下沿被裁）
    p.append(f'<rect x="94" y="326" width="252" height="78" rx="11" fill="#0d2231" stroke="#2f6b62" stroke-width="1.5"/>')
    p.append(f'<text x="108" y="352" font-family="{FONT}" font-size="14" font-weight="bold" fill="#eaf6ff">1号线 4站 → 2号线 10站</text>')
    p.append(f'<text x="108" y="376" font-family="{FONT}" font-size="13" fill="#6fd08c">56 分钟 · 5 元 · 步行 6 分钟</text>')
    return wrap('\n'.join(p), '高德路线 · 公交优先 v1.7.66')


def workflow():
    """WorkBuddy 语音指挥工作流：派活 / 触发 / 问进度 + 实时列工作流"""
    W, H = 900, 390
    p = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="#dcdcd8" stroke-width="1"/>',
         f'<rect x="8" y="8" width="56" height="5" fill="#e2231a"/>']
    p.append(f'<text x="450" y="48" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="bold" fill="#111111">手表说一句话 · 电脑干活 · 回来问结果</text>')
    p.append('<defs><marker id="aw" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#5d5347"/></marker></defs>')
    # 四个节点
    nodes = [(30,'手表语音','派活 / 触发 / 问进度','#2f6b62'),
             (255,'clawbot_workbuddy','第 37 个工具 · 三场景','#b4562f'),
             (480,'文件队列桥','queue.json · 原子写','#6b5b8a'),
             (705,'WorkBuddy 电脑端','automation 每小时消费','#35507a')]
    for x, t1, t2, col in nodes:
        p.append(f'<rect x="{x}" y="92" width="165" height="76" rx="13" fill="{col}"/>')
        p.append(f'<text x="{x+82}" y="124" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="bold" fill="#fff">{t1}</text>')
        p.append(f'<text x="{x+82}" y="148" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#f2e8d3">{t2}</text>')
    for x1, x2 in [(195,255),(420,480),(645,705)]:
        p.append(f'<path d="M{x1} 130 L{x2-8} 130" stroke="#5d5347" stroke-width="2" fill="none" marker-end="url(#aw)"/>')
    # 结果回灌
    p.append(f'<path d="M787 168 Q787 214 640 214 Q330 214 112 168" stroke="#b4562f" stroke-width="2" fill="none" stroke-dasharray="6 4" marker-end="url(#aw)"/>')
    p.append(f'<rect x="290" y="196" width="320" height="20" rx="4" fill="#fdfaf2"/>')
    p.append(f'<text x="450" y="210" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#b4562f">result.json 回灌 · 再问「结果点样」就把结果念出来</text>')
    # 三个场景卡
    cards = [(30,'① 派活','电脑帮我做件事 → 排队等电脑端领走'),
             (315,'② 触发工作流','按名字找到同名任务，立刻按它的 prompt 执行一次'),
             (600,'③ 问进度 / 列工作流','status 念结果；list_flows 实时读 SQLite 列最新 5 条')]
    for x, title, desc in cards:
        p.append(f'<rect x="{x}" y="248" width="270" height="76" rx="11" fill="#f2e8d3" stroke="#d8c9a8"/>')
        p.append(f'<text x="{x+16}" y="276" font-family="{FONT}" font-size="14" font-weight="bold" fill="#b4562f">{title}</text>')
        p.append(f'<text x="{x+16}" y="302" font-family="{FONT}" font-size="11" fill="#5d5347">{desc}</text>')
    p.append(f'<text x="450" y="354" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#8d8071">为什么用文件队列：桌面端无稳定对外 API，本地 MCP token 绑会话会过期——文件最耐长跑</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="WorkBuddy 语音指挥工作流程">\n' + '\n'.join(p) + '\n</svg>'


for name, fn in [('radar', radar), ('lyrics', lyrics), ('board', board),
                 ('radio', radio), ('camera', camera), ('failover', failover),
                 ('route', route), ('workflow', workflow)]:
    path = os.path.join(OUT, f'{name}.svg')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fn())
    print('wrote', path)
