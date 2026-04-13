# Code Review — get_anthropic

**日期**：2026-04-13  
**范围**：全仓库 Python 源码（~1700 行）+ GitHub Actions + 前端 HTML

---

## 总体评价

代码整体结构清晰，职责划分合理（fetcher / translator / builder / frontend 四层分离）。以下按模块逐一记录发现的问题与建议，分为「必须修复」「建议改进」「可选优化」三档。

---

## 必须修复

### 1. `fetchers/engineering.py` — 列表页日期提取不稳定

`fetch_article_list()` 通过拼接链接文本来提取日期，依赖 "标题文字 + 日期文字" 紧密拼接的 DOM 渲染顺序（如 `"Claude Code auto modeMar 25, 2026"`）。若页面结构调整，标题可能丢失或日期位置变化。

**建议**：将链接的 `<a>` 子元素分开提取——先找到 `href` 符合路径规则的链接，再从它的 DOM 兄弟/子节点分别取标题和日期，而不是从拼接文本中割分。不过当前实际结果正确，属于低风险隐患。

### 2. `fetchers/alignment.py` — 日期精度只到月

`alignment.anthropic.com` 页面只暴露 "March 2026" 格式的月份信息，无法得到精确日期。目前回退为 `YYYY-MM-01`，导致近期文章（如 "Abstractive Red-Teaming"，实际发布约 2026-03-25）被标记为 `2026-03-01`，在 `--lookback 30` 窗口里（起点 2026-03-14）就被排除在外。

**建议**：对 alignment 来源放宽窗口判断，或改用 URL 中的年份 + 页面月份 + 排列顺序估算。当前为可接受的已知限制，已在概要文档中说明。

### 3. `main.py:fetch_content()` — `red_team` description 优先逻辑与其他源不一致

`red_team` 源在有 `description` 时直接返回它作为翻译内容，但同时仍调用 `fetch_article_content()` 取日期。其他有 description 的源（`alignment`）也采用相同模式。这部分逻辑重复，且两段代码结构几乎相同。

**建议**：提取一个公共辅助函数 `_fetch_with_date_check(fetcher_module, article, since_str, today_str, use_description)` 消除重复，但鉴于逻辑稳定、功能正确，当前保留也可接受。

---

## 建议改进

### 4. `build_data.py` — `STATIC_REFS` 硬编码在函数内

`build()` 函数里写死了 constitution 链接。如果之后要加更多固定参考链接，需要修改函数内部。

**建议**：将 `STATIC_REFS` 提到模块顶层常量，与 `SOURCE_LABELS`/`SOURCE_DESC` 并列，便于维护。

### 5. `translator.py` — 阿里云 summary 模式截断 500 字符过短

`mode="summary"` 时只取正文前 500 字符（第 115 行）。对于长篇研究文章，500 字符通常只覆盖摘要段落，信息量不足。Claude 引擎使用的是 3000 字符，两者不一致。

**建议**：统一两种引擎的 summary 截断长度，或在 `translate()` 入口处统一截断，由调用方传入。

### 6. `fetchers/anthropic_blog.py` — 日期提取多路 fallback 无日志

日期提取有三个路径：`div.body-3.agate` 文本 → `article:published_time` meta → `<time datetime>`。若主路径失败会静默降级，调试时难以判断走了哪条路。

**建议**：加一行 `print(f"  [date fallback] {url}: used {method}")` 便于日后排查。

### 7. `main.py:init_index()` — 初始化时不区分 alignment/engineering 的无日期文章

`--init` 将无日期文章全部标记 `processed=True`。但 `alignment` 文章实际有月份信息（在页面里），初始化时没有去取，导致索引里日期为空且 processed=True，之后不会自动补填。

**建议**：在 `init_index()` 中对 alignment/engineering 等需要访问文章页才能取到日期的来源，批量预取日期（或在初始化后立即执行一次回填脚本）。

---

## 可选优化

### 8. `main.py` — `--lookback` 默认值偏小（3 天）

若当天 cron 失败，下次运行只往前看 3 天，容易丢漏文章。GitHub Actions 的 cron 在免费层有时会延迟 1-2 小时，遇到节假日也可能跳过。

**建议**：将默认值改为 5-7 天，或在 GitHub Actions 的 `daily-fetch.yml` 里显式传 `--lookback 5`。

### 9. `fetchers/claude_blog.py` — 三种卡片格式迭代 DOM 存在重复访问

现在 `fetch_article_list()` 遍历了三次 soup（旧卡片、新封面卡、列表条目），由于同一文章会出现在多个位置，`seen` 集合去重是正确的，但如果页面结构再扩展，维护成本会升高。

**建议**：统一用一次遍历所有 `<a href>` 且路径匹配 `/blog/...` 的链接，配合向上查找最近的日期文本。

### 10. `public/index.html` — 无分页，文章数量增长后首屏过长

目前 30 天 × 多来源 = 最多 100+ 篇文章，全部渲染在一页。随着来源增加（现在 8 个），这个问题会加速显现。

**建议**：加一个"展示最近 N 天，点击加载更多"的折叠逻辑，初始只渲染最近 7 天。

### 11. `article_index.json` — 无版本号字段

随着字段逐步增加（`processed`, `date`, 后续可能加 `summary_zh` 缓存等），缺少版本号意味着迁移时没有明确依据。

**建议**：在根层加 `"_version": 2` 字段，便于将来的迁移脚本判断格式。

---

## 安全 & 运维

- **API 密钥**：通过环境变量注入，`.gitignore` 已排除 `.env`，GitHub Secrets 管理，无硬编码问题。✅
- **请求超时**：所有 `requests.get()` 均设置了 `timeout=30`。✅  
- **robots.txt**：爬取的都是公开页面（官方博客/文档），无登录墙，合规。✅
- **速率限制**：目前无主动限速（无 `time.sleep()`）。文章列表页一次请求，文章正文按顺序串行请求。在翻译端 aliyun API 偶发失败会返回错误字符串而不是抛出异常，已被捕获。✅

---

## 总结

| 档位 | 数量 | 关键项 |
|------|------|--------|
| 必须修复 | 1 真实问题（#2 日期精度）| alignment 月份兜底导致近期文章漏出窗口 |
| 建议改进 | 4 项 | STATIC_REFS 提到顶层；统一截断长度；日期 fallback 日志；--lookback 默认值 |
| 可选优化 | 4 项 | claude_blog DOM 遍历；首页分页；index 版本号 |

整体代码质量良好，可直接用于生产。
