# Anthropic 资讯日报

每天早上自动从 8 个 Anthropic 官方信息源抓取新文章，翻译成中文，生成本地 Markdown 日报，并构建静态前端展示近 30 天内容。

## 信息源

| 来源 | 内容 |
|------|------|
| [Anthropic News](https://www.anthropic.com/news) | 官方新闻与产品公告 |
| [Anthropic Research](https://www.anthropic.com/research) | 研究论文与技术博客 |
| [Claude Blog](https://www.anthropic.com/claude-blog) | 面向用户与企业的 Claude 博客 |
| [Alignment Science](https://alignment.anthropic.com) | 对齐科学专项博客 |
| [Engineering Blog](https://www.anthropic.com/engineering) | 工程实践博客 |
| [Red Team](https://red.anthropic.com) | 红队安全研究 |
| [Claude Cookbook](https://platform.claude.com/cookbook) | 官方开发示例与教程 |
| [Transformer Circuits](https://transformer-circuits.pub) | 可解释性研究 |

## 架构

```
main.py          # 主调度器：抓取 → 比对索引 → 过滤日期 → 翻译 → 写日报
fetchers/        # 各信息源的抓取层（只返回文章列表）
translator.py    # 翻译层，支持 aliyun / claude / deepl 三引擎
build_data.py    # 将日报和索引合并为前端 JSON（public/data.json）
public/          # 静态前端，可部署到 Vercel / GitHub Pages
article_index.json  # 全量文章索引（持久化，防重复处理）
output/          # 每日中文日报（output/YYYY-MM-DD/digest.md）
```

## 快速开始

**1. 安装依赖**

```bash
pip install -r requirements.txt
```

**2. 配置环境变量**（阿里云机器翻译）

```bash
export ALIYUN_ACCESS_KEY_ID=your_key
export ALIYUN_ACCESS_KEY_SECRET=your_secret
```

**3. 首次运行：初始化索引**（将现有文章全部标记为已知，避免首次运行大量处理历史文章）

```bash
python3 main.py --init
```

**4. 运行**

```bash
python3 main.py
```

日报输出到 `output/YYYY-MM-DD/digest.md`。

## 自动化（每日定时）

通过 crontab 每天 7:30 自动运行：

```bash
# crontab -e
30 7 * * * /path/to/get_anthropic/run.sh
```

`run.sh` 会依次执行 `main.py`（抓取翻译）和 `build_data.py`（更新前端数据）。

## 常用参数

```bash
python3 main.py --lookback 7   # 向前看 7 天（默认 3 天）
python3 main.py --limit 5      # 单次最多处理 5 篇
python3 main.py --force        # 忽略已处理记录，强制重新处理
python3 main.py --date 2026-04-09  # 模拟指定日期运行
```

## 翻译引擎切换

在 `config.json` 中修改 `translate_engine`：

| 引擎 | 所需环境变量 |
|------|-------------|
| `aliyun`（默认） | `ALIYUN_ACCESS_KEY_ID` / `ALIYUN_ACCESS_KEY_SECRET` |
| `claude` | `ANTHROPIC_API_KEY` |
| `deepl` | `DEEPL_API_KEY` |

`translate_mode` 可设为 `summary`（前 500 字摘要，默认）或 `full`（全文翻译）。

## 前端部署

```bash
python3 build_data.py   # 生成 public/data.json
```

将 `public/` 目录部署到 Vercel 或 GitHub Pages，即可在浏览器中浏览近 30 天文章。
