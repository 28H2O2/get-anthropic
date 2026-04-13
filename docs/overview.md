# get_anthropic 仓库概要

> 每天自动抓取 Anthropic 全平台最新文章，翻译为中文摘要，生成静态网站。

---

## 这个仓库是做什么的

**一句话**：定时爬取 Anthropic 旗下 8 个内容来源，用阿里云机器翻译生成中文日报，通过 GitHub Actions 驱动、Vercel 托管，输出一个公开可访问的中文资讯聚合页。

**访问地址**：部署到 Vercel 后通过项目域名访问，展示近 30 天文章摘要 + 全量归档链接。

---

## 信息来源（8 个）

| 来源 key | 网站 | 内容类型 |
|---------|------|---------|
| `anthropic_news` | anthropic.com/news | 官方新闻、产品公告 |
| `anthropic_research` | anthropic.com/research | 研究论文、技术博客 |
| `red_team` | red.anthropic.com | 红队安全研究 |
| `claude_blog` | claude.com/blog | Claude 用户/企业博客 |
| `alignment` | alignment.anthropic.com | 对齐科学专项博客 |
| `engineering` | anthropic.com/engineering | 工程实践文章 |
| `cookbook` | platform.claude.com/cookbook | 开发示例与教程 |
| `transformer_circuits` | transformer-circuits.pub | 可解释性研究 |

另有固定参考链接：[Claude's Constitution](https://www.anthropic.com/constitution)（Model Spec）

---

## 目录结构

```
get_anthropic/
├── main.py                  # 主入口：调度 fetcher → 对比索引 → 翻译 → 写日报
├── build_data.py            # 数据构建：合并索引 + 摘要 → public/data.json
├── translator.py            # 翻译层：支持 aliyun / claude / deepl 三引擎
├── config.json              # 运行配置（来源开关、翻译引擎、模型）
├── article_index.json       # 全量文章索引（URL → 标题/日期/来源/是否已处理）
│
├── fetchers/                # 各来源的发现层（只返回文章列表，不做翻译）
│   ├── anthropic_blog.py    # 解析 sitemap.xml，覆盖 /news/ 和 /research/
│   ├── red_team.py          # 解析红队博客首页卡片
│   ├── claude_blog.py       # 解析 claude.com/blog 多种卡片格式
│   ├── alignment.py         # 解析对齐科学博客（distill.pub 风格）
│   ├── engineering.py       # 解析工程博客（Next.js 页面）
│   ├── cookbook.py          # 解析 Cookbook 卡片（description 直接用于翻译）
│   └── transformer.py       # 解析 transformer-circuits.pub 文章链接
│
├── output/                  # 每日中文日报（本地产物，不上传 Vercel）
│   └── YYYY-MM-DD/
│       └── digest.md        # 当日中文摘要（Markdown）
│
├── public/                  # Vercel 部署目录
│   ├── index.html           # 前端页面（纯 HTML/CSS/JS，无框架）
│   └── data.json            # 由 build_data.py 生成，前端 fetch 加载
│
├── .github/workflows/
│   └── daily-fetch.yml      # GitHub Actions cron 工作流
│
└── docs/                    # 项目文档
    ├── overview.md          # 本文件：仓库概要
    └── code_review.md       # Code review 结果
```

---

## 数据流

```
每日 07:30 (UTC+8)
       │
       ▼
GitHub Actions cron
       │
       ├── python3 main.py --lookback 3
       │         │
       │         ├── 各 fetcher.fetch_article_list()    →  文章 URL 列表
       │         ├── 对比 article_index.json            →  筛出新文章
       │         ├── fetch_content()                    →  抓正文 + 提取真实日期
       │         ├── translator.translate()             →  中文摘要
       │         └── 写 output/YYYY-MM-DD/digest.md     →  日报文件
       │                   + 更新 article_index.json
       │
       ├── python3 build_data.py
       │         │
       │         ├── 读 article_index.json（全量元数据）
       │         ├── 读 output/*/digest.md（所有摘要）
       │         └── 写 public/data.json                →  前端数据
       │
       └── git commit & push
                 │
                 ▼
           Vercel 自动部署
                 │
                 ▼
           public/index.html + data.json 上线
```

---

## 关键文件详解

### `article_index.json`

全量文章索引，格式 `{url: {title, date, source, processed}}`：

```json
{
  "https://www.anthropic.com/news/xxx": {
    "title": "Article Title",
    "date": "2026-04-13",
    "source": "anthropic_news",
    "processed": true
  }
}
```

- `processed: true` → 已翻译，不再重复处理
- `date` → 真实发布日期（不是 sitemap lastmod），由 `fetch_article_content()` 回填
- 作用：幂等性保障 + 全量归档索引

### `public/data.json`

由 `build_data.py` 生成，前端 JavaScript 通过 `fetch('./data.json')` 加载：

```json
{
  "generated_at": "2026-04-13",
  "lookback_days": 30,
  "digests": [
    {
      "date": "2026-04-13",
      "articles": [
        {
          "url": "...", "title_en": "...", "title_zh": "...",
          "summary_zh": "...", "source": "Anthropic News",
          "source_key": "anthropic_news", "date": "2026-04-13"
        }
      ]
    }
  ],
  "all_urls": { "anthropic_news": [...], ... },
  "archive_order": ["anthropic_news", ...]
}
```

### `.github/workflows/daily-fetch.yml`

关键配置：
- **触发时间**：`cron: '30 23 * * *'`（UTC 23:30 = 北京 07:30）
- **权限**：`contents: write`（允许 push 到仓库）
- **Secrets**：`ALIYUN_ACCESS_KEY_ID`、`ALIYUN_ACCESS_KEY_SECRET`

---

## 如何运行

### 首次部署

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置环境变量（本地测试）
export ALIYUN_ACCESS_KEY_ID=xxx
export ALIYUN_ACCESS_KEY_SECRET=xxx

# 3. 初始化文章索引（将现有文章全部标记为已知，避免首次运行全量翻译）
python3 main.py --init

# 4. 手动运行一次
python3 main.py --lookback 30

# 5. 生成前端数据
python3 build_data.py
```

### 日常调试

```bash
# 模拟指定日期运行
python3 main.py --date 2026-04-09

# 向前看 7 天内的新文章
python3 main.py --lookback 7

# 强制重新翻译（忽略 processed 标记）
python3 main.py --lookback 7 --force

# 限制单次处理数量（测试时用）
python3 main.py --limit 3
```

### 切换翻译引擎

编辑 `config.json`：

```json
{
  "translate_engine": "claude",          // aliyun | claude | deepl
  "translate_mode": "summary",           // summary | full
  "claude_model": "claude-haiku-4-5-20251001"
}
```

切换为 Claude 引擎时需额外设置 `ANTHROPIC_API_KEY`。

---

## 已知限制

| 问题 | 原因 | 状态 |
|------|------|------|
| alignment 文章日期精度只到月 | 页面只显示 "March 2026" | 已知限制，月份中点兜底 |
| Cookbook/Transformer 无发布日期 | 来源页面不含日期信息 | 仅在首次发现时翻译 |
| Anthropic sitemap 用 lastmod 非发布日期 | Anthropic CMS 特性 | 已通过 fetch_article_content 修复 |
| claude.com/blog 使用 Webflow 动态渲染 | 多种卡片格式 | 已兼容三种卡片结构 |

---

## TODO

- [ ] **X（Twitter）推送定时爬取**：Anthropic 官方 X 账号发布的内容往往早于官网文章，可用 Twitter API v2 或 nitter 镜像做补充来源
- [ ] **Telegram/邮件通知**：每日日报生成后推送到 Telegram Bot 或邮件列表
- [ ] **全文翻译模式**：目前 summary 模式只取前 500 字，后续可切换 `translate_mode: full` + Claude 引擎做高质量全文翻译
- [ ] **文章内容缓存**：将翻译结果缓存到 `article_index.json` 的 `summary_zh` 字段，避免重复翻译
- [ ] **前端分页**：近 30 天文章量增大后，考虑初始只渲染最近 7 天，点击加载更多
- [ ] **RSS 输出**：生成 `public/feed.xml`，让用户可订阅
- [ ] **更多来源**：`alignment.anthropic.com` 月份日期精度待改进；考虑接入 Anthropic YouTube 字幕摘要
