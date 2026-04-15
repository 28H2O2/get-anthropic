# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目用途

每天早上 7:30 自动从 4 个 Anthropic 信息源抓取新文章，翻译成中文，生成本地 Markdown 日报。

## 运行方式

```bash
# 首次使用：初始化索引（将现有文章全部标记为已知，避免首次运行刷屏）
python3 main.py --init

# 生产运行（读取 ~/.zshrc 里的环境变量）
bash run.sh

# 手动运行（需先 export 环境变量）
python3 main.py

# 模拟指定日期（调试/补跑）
python3 main.py --date 2026-04-09

# 调整时间窗口（默认 3 天，向前看 N 天内的文章）
python3 main.py --lookback 7

# 限制处理数量
python3 main.py --limit 5

# 强制重处理（忽略已处理记录）
python3 main.py --force

# 安装依赖
pip install -r requirements.txt
```

## 必需的环境变量

| 变量 | 用途 |
|------|------|
| `ALIYUN_ACCESS_KEY_ID` | 阿里云机器翻译 |
| `ALIYUN_ACCESS_KEY_SECRET` | 阿里云机器翻译 |

已写入 `~/.zshrc`，crontab 通过 `run.sh` 调用时自动 source。

## 架构

```
main.py          # 主协调器：调度 fetcher → 对比 state → 翻译 → 写日报
fetchers/        # 各信息源的发现层（只返回文章列表，不做翻译）
  anthropic_blog.py   # 解析 anthropic.com/sitemap.xml，过滤 /news/ 和 /research/ 路径
  cookbook.py         # 解析 platform.claude.com/cookbook 的卡片列表
  transformer.py      # 解析 transformer-circuits.pub 首页的文章链接
translator.py    # 翻译层，支持 aliyun / claude / deepl 三引擎
state.json       # 已处理文章 URL 集合（持久化，防重复）
config.json      # 运行配置
output/YYYY-MM-DD/digest.md  # 每日中文日报输出
logs/            # 运行日志（由 run.sh 生成）
```

## 文章索引（article_index.json）

维护全量文章元数据，结构为 `{url: {title, date, source, processed}}`：
- `processed: true` = 已翻译过，不再重复处理
- `processed: false` / 不存在 = 未处理
- 无日期文章（Cookbook/transformer）在 `--init` 时自动标记为 `processed: true`，之后只有新发现的才会处理

## 关键设计决策

- **Anthropic 博客无 RSS**：通过 `sitemap.xml` 检测新 URL，`fetch_article_content()` 返回 `(content, title)` 元组，在抓取正文的同时提取 `og:title`
- **Cookbook 是卡片布局**：不含日期，卡片内的 description 字段直接作为翻译输入（避免二次请求）
- **专有名词保护**：翻译前将 Claude/Sonnet/Haiku 等替换为占位符（NOUN00~），翻译后大小写不敏感还原，防止机器翻译乱译
- **state.json 幂等性**：每次运行对比已知 URL，只处理新增文章

## 配置说明（config.json）

```json
{
  "translate_engine": "aliyun",   // aliyun | claude | deepl
  "translate_mode": "summary",    // summary（前500字摘要）| full（全文）
  "claude_model": "claude-haiku-4-5-20251001",
  "sources": { ... }              // 各信息源的开关
}
```

切换为 Claude 翻译引擎时需额外设置 `ANTHROPIC_API_KEY`。

## Git 推送规范

GitHub Actions 每天自动运行，会向远端 `main` 提交新数据（`article_index.json`、`public/data.json` 等）。因此**每次 push 前必须先拉取远端变更**，否则会因 non-fast-forward 被拒绝：

```bash
git pull --rebase origin main && git push origin main
```
