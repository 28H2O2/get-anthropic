# Anthropic 每日简报 2026-11-26

> 共 **1** 篇中文摘录

---

### [将我们的消息 API 迁移到Rust](https://www.anthropic.com/research/migrating-api-to-rust)

**来源**: Engineering Blog

**发布日期**: 2026-11-25

**原文**: https://www.anthropic.com/research/migrating-api-to-rust

**中文摘录**：

我们如何使用现有消息 API 来验证新消息，由 Claude 代理组成的团队跟踪并修复Python和Rust版本之间的差异。许多问题都存在生成器—验证者差距：通常，验证一个解是否正确要比构造出这样一个解容易得多。数独是一个经典例子。验证解法很简单（只需统计每一行、每一列和每一个宫格中的数字个数），但要找到这个解法却可能需要很长时间。许多雄心勃勃的 Claude 项目都依赖于这一差距: 形式化数学证明或迁移大型、经过良好测试的代码库是 Claude 可以承担的任务，只要它有可靠的方法来验证其工作。

---
