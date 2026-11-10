# Anthropic 每日简报 2026-11-10

> 共 **4** 篇中文摘录

---

### [Claude 可以从头到尾设计电子原型](https://www.anthropic.com/research/claude-electronics-design)

**来源**: Anthropic Research

**发布日期**: 2026-11-09

**原文**: https://www.anthropic.com/research/claude-electronics-design

**中文摘录**：

我们要求 Claude 设计三种电子设备: 免提电话、语音助手集线器和手持虚拟宠物。原型在没有任何电路修复的情况下工作。大约一年多前，我们开始测试Claude设计基本电子电路的能力。我们与设计和制造电路板的公司Diode Computers 1合作，对 Claude 进行简单任务的培训-例如，阅读芯片的数据表并确定芯片需要哪些部分才能运行。我们当时试验的模型无法可靠地布局电路板; 他们还努力设计适合在一起的组件。现在，Claude 可以从头到尾设计和原型电子硬件。

---

### [JPMorganChase将 Claude 代码扩展到更多员工](https://claude.com/resources/articles/jpmorganchase-expands-claude-code)

**来源**: Claude Blog

**发布日期**: 2026-11-09

**原文**: https://claude.com/resources/articles/jpmorganchase-expands-claude-code

**中文摘录**：

JPMorganChase正在整个公司向工程师以外的更多员工推出 Claude。在商业和投资银行中，工作进入生产的速度更快，公司根据其业务优先事项重新部署了这种能力。团队正在对其他遗留系统进行现代化改造，工程师正在构建自己的代理，包括拉取请求审查和自我修复代理，并共享有效的代理。基础设施和运营团队使用 Claude 代码 (在新选项卡中打开) 进行监控、警报和根本原因分析。该公司的安全团队使用我们的前沿模型来更快地发现和修复漏洞，这是我们在Project Glasswing (在新选项卡中打开) 中首次描述的工作。最接近企业的人也在用 Claude 建造。

---

### [安全扩展多代理团队与 Claude 寓言5.2/claude.Dev博客](https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2)

**来源**: Claude Blog

**发布日期**: 2026-11-09

**原文**: https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2

**中文摘录**：

一支由1000名工作人员组成的团队，在运行Claude Fable 5.2早期版本的环境下，借助通用工具、共享数据库以及多层安全防护机制，成功复现了费马大定理的形式化证明。多智能体团队能够解决具有挑战性的长周期问题。今年九月，我们发表了费马大定理的首个端到端形式化证明，该证明由数十个智能体在内部研究模型上完成，该模型大致相当于Claude Fable 5.1。该项工作依托于Prove2Me——一个用于形式化数学的平台——以及一位研究人员的指导。在一项新的玩具实验中，由1000个智能体组成的团队运行了Claude《寓言》5.2的早期版本，在没有Prove2Me提供的支撑框架、也未接受研究人员指导的情况下，重现了该证明。

---

### [您应该使用哪种 Claude 模型进行构建？寓言，Opus, Sonnet, 或 Haiku/claude.Dev博客](https://claude.dev/blog/which-claude-model-should-you-build-with)

**来源**: Claude Blog

**发布日期**: 2026-11-09

**原文**: https://claude.dev/blog/which-claude-model-should-you-build-with

**中文摘录**：

当前的 Claude 阵容有四种通用型号: Claude Haiku 5.5，Claude Sonnet 5.5，Claude Opus 5.5和 Claude 寓言5.2。Claude Mythos 5.2是我们最有能力的网络安全和生命科学研究模型，可通过我们的验证计划获得。如果您在 Claude 平台上构建或使用 Claude 代码，您可能想知道使用哪种模型来完成常见任务。这篇文章将帮助回答这个问题，以及如何思考权衡。简而言之，您应该将大多数工作在 Opus 5.5上以默认的中等努力程度开始。它之所以成为 Claude Code中的默认模型，是有原因的。每个输入和输出令牌的成本是寓言5.2的一半，这是我们建议从大多数编码和知识工作开始的模型。

---
