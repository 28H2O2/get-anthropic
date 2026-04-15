# Changelog

## 2026-04-15（修复"一键直达"滚动落点）

### 修复
- `public/index.html`：`.archive-section` 加 `scroll-margin-top: 2rem`，点击"一键直达 → 所有引用"后"全部引用链接"标题能完整显示在视口内，不再被推出上边缘

## 2026-04-14（Red Team / Transformer 精确日期 + References 独立样式 + Favicon）

### 改进
- `fetchers/transformer.py`：`fetch_article_content` 改为返回元组，从页面提取 "Published Month DD, YYYY" 格式精确日期
- `fetchers/red_team.py`：回填全部 17 篇精确日期到 `article_index.json`
- 回填 transformer 10 篇年份级别日期升级为完整日期
- `build_data.py`：`static_refs` 独立为顶层字段，不再混入 `all_urls`
- `public/index.html`：References 以胶囊 chip 样式独立展示于归档区底部；加 SVG favicon

## 2026-04-14（Cookbook 日期回填 + 归档排序 + 10 篇新文章翻译）

### 改进
- `build_data.py`：归档区（all_urls）按日期倒序排列，无日期排最后
- 回填全部 76 篇 cookbook 文章的真实发布日期到 `article_index.json`
- 30 天内 10 篇 cookbook 文章重置为未处理并完成翻译，已加入前端首页

## 2026-04-14（Cookbook 支持精确发布日期）

### 改进
- `fetchers/cookbook.py`：`fetch_article_content()` 改为返回 `(content, title, pub_date)` 元组，从详情页解析 "Published on Month DD, YYYY" 格式日期
- `main.py`：cookbook 分支改为先拉详情页取日期 + 日期窗口过滤，翻译仍优先用列表页 description（减少全文请求）

## 2026-04-14（run.sh 自动调用 build_data.py）

### 修复
- `run.sh` 每次运行 `main.py` 后自动调用 `build_data.py`，确保前端 `public/data.json` 每日随之更新，30 天滚动窗口生效

## 2026-04-14（新增 alignment / engineering 来源 + claude_blog 卡片修复 + 文档）

### 新增信息来源
- `fetchers/alignment.py`：抓取 alignment.anthropic.com（Anthropic 对齐科学博客，36 篇）
- `fetchers/engineering.py`：抓取 anthropic.com/engineering（工程实践博客，22 篇）
  - 日期从 Next.js payload 中提取 `publishedOn` 字段
- `config.json`：新增 `alignment: true` / `engineering: true` 开关

### 修复 claude_blog 漏抓新卡片
- `fetchers/claude_blog.py`：兼容三种卡片格式（旧 marquee_cms / 新 card_blog_wrap 封面卡 / card_blog_list_wrap 列表条目）
- 修复前漏掉约 12 篇文章（含 the-advisor-strategy 等）

### 新增固定参考链接
- `build_data.py`：新增 `STATIC_REFS` 顶层常量，归档区底部显示 Claude's Constitution 链接

### 文档
- `docs/overview.md`：仓库概要（架构、数据流、目录结构、运行方式、TODO）
- `docs/code_review.md`：全仓库 code review 结果（必须修复 / 建议改进 / 可选优化）

### 数据更新
- 批量回填所有 alignment 文章日期（月份精度）
- 翻译近 60 天内新文章，总已处理 185 篇

---

## 2026-04-13（修复 is_new 日期误判 + 补翻 claude_blog 缺失摘要）

### 修复 `is_new()` 使用 sitemap lastmod 导致旧文章反复出现
- `main.py`：`is_new()` 改为优先读取 `index[url]["date"]`（已修正的真实日期），而非 sitemap 返回的 `lastmod`
- `main.py`：翻译循环结束后，对所有 `new_articles`（含跳过的）都将真实日期回写 index，防止下次再被误判

### 补翻 3 篇缺摘要的 claude_blog 文章
- 运行 `python3 main.py --lookback 30` 成功翻译：
  - Preparing your security program for AI-accelerated offense (2026-04-10)
  - Claude Managed Agents: get to production 10x faster (2026-04-08)
  - Harnessing Claude's intelligence (2026-04-02)
- 重新生成 `public/data.json`

---

## 2026-04-13（Vercel 部署 + 日期修复）

### 修复文章日期错误（sitemap lastmod → 真实发布时间）
- `fetchers/anthropic_blog.py`：`fetch_article_content` 改为返回 `(content, title, pub_date)` 三元组，pub_date 从 `<meta property="article:published_time">` 或 `<time datetime>` 提取
- `main.py`：获取内容后用真实发布日期覆盖 sitemap lastmod；若真实日期超出 lookback 窗口则跳过该文章

### 新增 Vercel 静态站部署
- `build_data.py`：将 `article_index.json` + `output/*/digest.md` 合并为 `public/data.json`（前端数据源）
- `public/index.html`：中文前端，按日期展示近 14 天文章，含英文/中文标题、中文摘要、全量链接归档
- `.github/workflows/daily-fetch.yml`：每天 23:30 UTC（北京时间 07:30）自动抓取 + 翻译 + 生成数据 + 推送（触发 Vercel 重新部署）
- `vercel.json`：静态站配置，输出目录指向 `public/`
- `.gitignore`：忽略 `.env`、日志、Python 缓存等敏感/临时文件
- 停止本地 crontab，改由 GitHub Actions 托管定时任务

### 仓库
- GitHub：https://github.com/28H2O2/get-anthropic

---

## 2026-04-10（第二次更新）

### 修复日报只显示近期文章 + 维护文章总索引

**问题**：旧版 state.json 无日期信息，导致日报会包含历史上所有未处理文章（429 篇）

**变更**：
- `state.json` → 废弃，改为 `article_index.json`（含 title/date/source/processed 字段）
- `anthropic_blog.py`：fetch_article_list() 从 sitemap `<lastmod>` 提取文章日期
- `main.py`：
  - 新增 `--init` 参数：首次使用时初始化索引，将无日期文章标记为已知
  - 新增 `--date YYYY-MM-DD` 参数：模拟指定日期运行
  - 新增 `--lookback N` 参数：控制时间窗口（默认 3 天）
  - 过滤逻辑：有日期文章必须在时间窗口内；无日期文章（Cookbook/transformer）只在首次发现时处理
- `translator.py`：占位符改为 `{{N}}` 格式（花括号），避免被阿里云翻译为「名词N」

**正确使用流程**：
1. `python3 main.py --init`（只运行一次）
2. 之后每天 `bash run.sh` 或 crontab 自动运行


## 2026-04-10

### 初始版本完成

**功能**：
- 监控 4 个 Anthropic 信息源：`/news`、`/research`、Cookbook、transformer-circuits.pub
- 通过 `sitemap.xml` 检测 Anthropic 博客/研究新文章（无官方 RSS）
- 解析 Cookbook 卡片列表和 transformer-circuits 首页文章列表
- 调用阿里云机器翻译 API 翻译标题和正文摘要（前 500 字符）
- 专有名词保护机制（Claude/Sonnet/Haiku 等不被错误翻译）
- 生成 `output/YYYY-MM-DD/digest.md` 每日中文日报
- `state.json` 持久化已处理 URL，避免重复处理
- `run.sh` wrapper 脚本供 crontab 调用，自动加载环境变量
- crontab 定时任务：每天 07:30 自动运行

**文件结构**：
```
main.py              # 主入口
config.json          # 配置（引擎、模式、信息源开关）
state.json           # 已处理 URL 记录
fetchers/
  anthropic_blog.py  # /news + /research（sitemap + requests）
  cookbook.py        # Cookbook 卡片列表
  transformer.py     # transformer-circuits.pub
translator.py        # 阿里云/Claude/DeepL 三引擎翻译
run.sh               # crontab 调用的 shell wrapper
output/              # 每日日报输出目录
logs/                # 运行日志
```
