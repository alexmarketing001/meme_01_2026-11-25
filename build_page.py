"""生成 index.html：样式沿用 OFT 交易赛模板（../oft/index.html），正文来自 body.src.html，Logo 全部 base64 内嵌。
用法：python3 build_page.py
"""
import base64
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE / 'template-oft.html'  # OFT 交易赛页面原件（已归档到 _archive/oft-race-202611/页面）

CONTRACT = '0x6a2b0b704650a93f7495d728c3b851a1c5f73172'
TRADE_URL = f'https://ave.ai/token/{CONTRACT}-bsc'
# (该档最后一名, 单人奖励)
TIERS = [(1, 1200), (2, 800), (3, 500), (10, 200), (30, 100), (50, 60), (100, 40), (200, 20), (350, 16), (500, 10)]
PUBLIC = 50  # 接口返回前的占位行数


def data_uri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def color(rank):
    return 1 if rank <= 10 else 2 if rank <= 100 else 3


def reward(rank):
    return next(r for last, r in TIERS if rank <= last)


def label(first, last):
    return f'Top {first}' if first == last else f'{first}–{last}'


starts = {last + 1 for last, _ in TIERS[:-1]}

prize_rows, prev, check = [], 0, 0
for last, amt in TIERS:
    first, n = prev + 1, last - prev
    check += n * amt
    prize_rows.append(
        f'<tr class="t{color(first)}"><th scope="row"><span class="tier-name"><span>{label(first, last)}</span></span></th>'
        f'<td>{amt:,}<span class="unit">U</span></td><td>{n}</td><td>{n * amt:,}<span class="unit">U</span></td></tr>')
    prev = last
assert check == 15000 and prev == 500, (check, prev)

board_rows = ''.join(
    f'<tr class="tier{color(r)}{" tier-start" if r in starts else ""}"><th scope="row" class="rank-cell">{r:02d}</th>'
    f'<td><span class="wallet-pending">待更新</span></td><td class="numeric">—</td>'
    f'<td class="numeric reward-cell">{reward(r):,} U</td></tr>'
    for r in range(1, PUBLIC + 1))
board_rows += (f'<tr class="rest-row tier-start"><td colspan="4">第 {PUBLIC + 1}–500 名奖励见奖励分配表，'
               f'榜单仅公示前 {PUBLIC} 名，最终名次以活动结束后的审核结果为准。</td></tr>')

tpl = TEMPLATE.read_text()
ave_logo = re.search(r'class="ave-logo" src="(data:[^"]+)"', tpl).group(1)
head = tpl[:tpl.index("</style>")].replace("content=\"#13294b\"", "content=\"#070b3a\"")
head = re.sub(r'<title>.*?</title>', '<title>AVE × Four.meme 专属交易狂欢赛｜40,000 USDT 等你拿</title>', head)
head = re.sub(r'<meta name="description"[^>]*>',
              '<meta name="description" content="在 Ave.ai 交易 4Stock 代币 RYDE4（BNB Chain）及以该代币为底池的 Meme：交易满 200U 瓜分 25,000 USDT 空投，交易量前 500 名瓜分 15,000 USDT。2026.11.26 18:00 开赛，持续 14 天。">', head)
head = re.sub(r'<meta property="og:title"[^>]*>', '<meta property="og:title" content="AVE × Four.meme 专属交易狂欢赛">', head)
head = re.sub(r'<meta property="og:description"[^>]*>',
              '<meta property="og:description" content="40,000 USDT 等你拿！交易 RYDE4 及其底池 Meme，满 200U 瓜分 25,000 USDT，前 500 名瓜分 15,000 USDT。">', head)

extra_css = (HERE / 'extra.css').read_text().replace('{{HERO_WIDE}}', data_uri(HERE / 'assets' / 'hero-wide.jpg', 'image/jpeg')).replace('{{HERO_TALL}}', data_uri(HERE / 'assets' / 'hero-tall.jpg', 'image/jpeg'))
body = (HERE / 'body.src.html').read_text()
for key, val in {
    'AVE_LOGO': ave_logo,
    'FM_LOGO': data_uri(HERE / 'assets' / 'fourmeme-logo.png', 'image/png'),
    'RYDE_LOGO': data_uri(HERE / 'assets' / 'ryde4.png', 'image/png'),
    'TRADE_URL': TRADE_URL,
    'PRIZE_ROWS': ''.join(prize_rows),
    'BOARD_ROWS': board_rows,
}.items():
    body = body.replace('{{' + key + '}}', val)
assert '{{' not in body

out = head + extra_css + '\n  </style>\n</head>\n' + body
(HERE / 'index.html').write_text(out)
print('index.html', len(out), 'bytes')
