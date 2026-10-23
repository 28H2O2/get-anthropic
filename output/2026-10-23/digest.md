# Anthropic 每日简报 2026-10-23

> 共 **6** 篇中文摘录

---

### [向Agentic AI基金会捐赠代理技能](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation)

**来源**: Anthropic News

**发布日期**: 2026-10-22

**原文**: https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation

**中文摘录**：

我们正在向Agentic AI基金会捐赠代理技能，这是为AI代理提供专业知识和工作流程的开放标准。自2025年12月发布标准以来，包括 ChatGPT, Cursor，GitHub Copilot和VS Code在内的70多个代理平台已经集成了代理技能。今天，我们向Agentic AI基金会 (AAIF) 捐赠Agent Skills，这是一个为AI代理提供专业知识和工作流程的开放标准。自2025年12月发布标准以来，包括 ChatGPT, Cursor，GitHub Copilot和VS Code在内的70多个代理平台已经集成了代理技能。技能是一个包含skill.md文件的文件夹，该文件向代理教授特定的任务或域，以及它需要的任何脚本或参考资料。

---

### [生命科学领域客座调查员的公开电话](https://www.anthropic.com/news/open-call-guest-investigators-life-sciences)

**来源**: Anthropic News

**发布日期**: 2026-10-22

**原文**: https://www.anthropic.com/news/open-call-guest-investigators-life-sciences

**中文摘录**：

今天，我们邀请生命科学界的成员申请与我们合作开展特殊项目。我们正在寻找学术机构，非营利组织或政府实验室的主要研究人员及其研究小组的建议，他们希望使用 Claude 调查因果人类生物学，结构和计算分子生物学，药物化学，药物发现和临床科学中的关键问题。在8-12周的时间里，客座调查员将直接与 Anthropic 研究人员就感兴趣的问题进行合作，并产生对他们的工作最有帮助的分析、工件和工具。我们的团队将免费运行我们的模型和线束。我们将共同努力发布这些输出，并开源附带的数据和代码。

---

### [LLMs正在使正式软件验证在更大的范围内变得可行](https://www.anthropic.com/research/formal-verification)

**来源**: Red Team

**发布日期**: 2026-10-22

**原文**: https://www.anthropic.com/research/formal-verification

**中文摘录**：

Claude 在123个开源库的编译代码中正式证明了其安全属性。在此过程中，它发现了多年来一直未被察觉的漏洞。Keane Lucas, Aengus Lynch, Luna Tong, Luke Champine, Zygi Straznickas, Dino Distefano, Harshikaa Agrawal Evyatar Ben Asher, Ava Howell, Sami Jawhar, Chris Rohlf, Nickolai Zeldovich Nicholas Carlini, Rajashree Agrawal, Jason Gross Most software is riddled with bugs, which AI can now easily find and exploit.应对网络攻击的常规防御措施已不再足够：我们需要能够证明代码无漏洞的方法。形式化软件验证可以提供这一保证，但传统上需要耗费多年的专家精力，因此对于大多数实际项目而言并不具有可行性。

---

### [构建代理: 何时将子代理折叠到主代理循环中](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)

**来源**: Claude Blog

**发布日期**: 2026-10-22

**原文**: https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop

**中文摘录**：

何时考虑使用更少的子代理以及如何将迁移到主循环中。在 Claude 平台中构建代理时，使用较少的子代理来支持逐步公开的上下文和工具可以提高质量，同时降低成本和延迟。以下是何时以及如何迁移。

---

### [Claude 平台现已在Google Cloud上可用](https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed)

**来源**: Claude Blog

**发布日期**: 2026-10-22

**原文**: https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed

**中文摘录**：

使用Google Cloud上的 Claude 模型 (Anthropic 托管) 访问具有Google Cloud身份验证、计费和承诺停用功能的 Claude 平台。

---

### [Red-Teaming自动模式: 针对恶意编码代理改进阻止分类器](https://alignment.anthropic.com/2026/red-teaming-auto-mode)

**来源**: Alignment Science

**发布日期**: 2026-10-22

**原文**: https://alignment.anthropic.com/2026/red-teaming-auto-mode

**中文摘录**：

We red-team production blocking monitor (Claude 代码中的自动模式，OpenAI 法典中的Guardian)，在实验环境中使用对抗剂，目的是提高编码剂的安全性。我们最有效的攻击策略使用针对监视器的代理生成的提示注入，多代理攻击或恶意压缩来绕过监视器。我们尝试通过提高工具覆盖率，成绩单格式和使用代理监控阶段来提高自动模式的鲁棒性。我们发现，以可接受的成本稳健地防止多上下文攻击仍然是一个开放的问题。编码代理现在可以在很少或没有人工参与的情况下运行数天，端到端地完成软件任务 (Kwa等人，2025)。

---
