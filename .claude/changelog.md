# Changelog

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
