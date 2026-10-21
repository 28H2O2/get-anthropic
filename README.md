# Anthropic 资讯日报

**简体中文** | [English](README.en-US.md)

从 8 个 Anthropic 官方来源发现文章，核验发布日期，生成阿里云机器翻译中文摘录，并发布近 30 天内容及历史原文归档。

## 运行

```bash
pip install -r requirements.txt
# 在当前 shell 设置 ALIYUN_ACCESS_KEY_ID / ALIYUN_ACCESS_KEY_SECRET
python3 -m unittest discover -s tests -v
python3 main.py                  # 默认近30天；失败记录可再次尝试
python3 build_data.py            # 仅在所有启用来源发现成功、数据验证通过时更新前端
python3 main.py --check-health   # 部分翻译失败时返回非零
```

首次发现基线可用 `python3 main.py --init`，保留已有索引但不批量翻译。
升级后执行一次 `python3 main.py --repair-recent`，核验近30天日期并补查 Cookbook、Alignment、Transformer 的历史日期缺口。只翻译真实近期文章与首次发现的无日期文章，不全量翻译历史归档。
`--limit 5` 限制翻译数量；`--force` 重做窗口内摘录；`--date YYYY-MM-DD` 用于调试。`run.sh` 使用当前环境变量，将失败退出状态传给调用方。

## 数据与状态

- `article_index.json` 是文章元数据和中文摘录的唯一事实源。`date` 为真实发布日期，`date_precision` 保留日/月/年精度；`sitemap_lastmod` 只用于发现更新。
- 日期未经详情页核验的旧记录不进入近期列表。仅知月份或年份的文章保留在归档，日期不补成某一天；新发现但无日期的文章单独标识。
- `summary_status` 为 `pending` / `ready` / `failed`。只有有效中文摘录才能标记 `processed: true`，HTTP 和翻译分别最多尝试3次。
- 首次迁移从历史日报导入最新有效摘录，之后以文章记录为准。`output/YYYY-MM-DD/digest.md` 是当日成功摘录的派生文档，不再反向覆盖新结果。
- `fetch_status.json` 记录来源发现数和最近成功时间；`public/data.json` 输出文章状态、覆盖率和来源健康度。密钥始终只通过环境变量注入。
- 阿里云模式翻译清理后的原文导语或摘要，正文最多约800英文字符并保留完整句子，标题单独翻译。它是中文摘录，并非生成式全文摘要。
- `summary_en` 保存官网正文中约800英文字符以内的完整句子，作为英文原文摘录；它与中文翻译状态独立，中文翻译失败时仍可阅读英文。近期旧文章缺少此字段时，下次运行会补取原文，不重复翻译有效中文摘录。

## 自动运行与部署

GitHub Actions 每日 UTC 23:30（UTC+8 次日07:30，实际启动可能延迟）运行，可手动勾选 `repair_recent` 补查。工作流依次执行测试、抓取、构建验证和提交，Vercel 发布 `public/`。

任一启用来源发现失败或返回0篇时，不构建、不提交数据，线上保留上一版；单篇翻译失败时发布其他有效内容并保存重试状态，最终健康检查使 Actions 显示失败。各来源数量和成功时间写入 Actions Job Summary，故障信息保留为 artifact。并发定时任务串行执行；推送发生冲突时失败，不自动覆盖远端。

来源：Anthropic News / Research、Claude Cookbook、Transformer Circuits、Frontier Red Team、Claude Articles、Alignment Science、Engineering。部分旧入口会重定向，依据 canonical 合并记录并保留 aliases，专门来源优先于通用 Research 分类。

日常发布前先同步远端自动数据，测试通过后构建并验证，提交范围限本次改动；上线后核对 `data.json` 覆盖率与源码版本。

## 网站界面与更新记录

`public/index.html` 是静态页面入口，样式与交互分别位于 `public/assets/style.css`、`public/assets/app.js`。`#latest` 展示近期中文摘录，`#archive` 提供按来源及关键词筛选的原文归档，`#updates` 展示网站自身的更新记录。来源筛选与搜索在切换阅读视图时保留。

页眉提供中文 / EN 切换，默认中文并记住选择；`?lang=en` 或 `?lang=zh` 可直接分享对应语言，优先于保存的偏好。英文模式显示英文原标题与原文摘录，导航、日期、来源说明、状态及更新记录同时切换，保留当前视图、来源和搜索词。

网站功能或体验变更记录在 `public/changelog.json`，按时间倒序排列，每条包含 `date`、`type`、`title` 与 `changes`，并通过 `type_en`、`title_en`、`changes_en` 提供英文；历史条目可保留 `description`。每日自动抓取不向此文件追加日志；文章刷新与网站版本更新分别展示。记录中的覆盖率属于对应修复时的快照，首页状态面板读取当前 `data.json`。

页脚 H2O2 署名沿用参考站的 Macintosh Skeletal Filled 字体。`public/assets/h2o2-mark.woff2` 仅包含署名所需字符，其他文字使用系统字体。
