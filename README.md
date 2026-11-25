# AVE × Four.meme 专属交易狂欢赛 活动页

正式域名：https://ryde4.ave.ai/ （GitHub Pages，`main` 分支根目录发布，`CNAME` 已配置）

## 文件
- `index.html`：发布的页面（样式、脚本、图片全部内嵌，可单独打开或转发）。**不要直接改它**，改下面的源文件后重新生成。
- `body.src.html`：页面正文和脚本。顶部「活动配置」里有 `START_AT`（开赛时间）和 `LEADERBOARD_API_URL`（榜单接口）。
- `extra.css`：本活动样式（叠加在 OFT 模板样式之上）。
- `template-oft.html`：OFT 交易赛页面，提供基础样式。
- `build_page.py`：`python3 build_page.py` 生成 `index.html`，并校验活动二奖励合计 15,000。
- `assets/`：Ave、Four.meme、RYDE4 的 Logo，以及设计组出的首屏背景（横版 `hero-wide.jpg` 给电脑，竖版 `hero-tall.jpg` 给手机）。

## 活动信息
- 交易范围：4Stock 代币 RYDE4（BNB Chain，`0x6a2b0b704650a93f7495d728c3b851a1c5f73172`）及以该代币为底池的 Meme。
- 活动一：累计交易量 ≥200U，瓜分 25,000 USDT。活动二：Top 500，上榜门槛 500U，瓜分 15,000 USDT（10 档）。
- 赛期：2026-11-26 18:00 至 2026-12-10 18:00（UTC+8），共 14 天。
- 交易按钮：https://ave.ai/token/0x6a2b0b704650a93f7495d728c3b851a1c5f73172-bsc

## 发布
1. 改 `body.src.html` 或 `extra.css`，运行 `python3 build_page.py`。
2. 本地预览：`python3 -m http.server 4181`，打开 http://localhost:4181/
3. 提交并推送到 `main`，GitHub Pages 自动发布。线上用 `?v=任意值` 绕开缓存检查。

## 待办
- 后端公开榜单接口（地址打码，字段同 OFT 接口）→ 填 `LEADERBOARD_API_URL`，并对 `https://ryde4.ave.ai` 开放跨域。未填时榜单显示"活动尚未开始"。
- DNS：`ryde4.ave.ai` 需要 CNAME 指向 `pc-h5-allpages.github.io`（Cloudflare，只做 DNS 解析，不开代理）。
- 结算用的完整数据（含完整地址）不得放进本仓库或页面。
