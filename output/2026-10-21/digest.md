# Anthropic 每日简报 2026-10-21

> 共 **60** 篇中文摘录

---

### [Claude 如何设计蛋白质结合剂对抗蝎子神经毒素](https://www.anthropic.com/research/claude-scorpion-toxin-binder-design)

**来源**: Anthropic Research

**发布日期**: 2026-10-20

**原文**: https://www.anthropic.com/research/claude-scorpion-toxin-binder-design

**中文摘录**：

我们要求一个内部研究 Claude 模型来设计针对蝎子神经毒素的微型结合物 (紧密附着在靶标上的小蛋白质)。总结: 作为我们研究 Claude 如何帮助加速药物发现的工作的一部分，我们要求一个内部研究模型来设计针对蝎子神经毒素的小结合物 (紧密附着在靶标上的小蛋白质)。Claude 借鉴了我们与金融投资研究公司Citrini research合作开发的prompt和四个后续项目。Adaptyv Bio和Twist Bioscience的团队通过实验测试了211设计的结合。其中17个符合我们的标准。我们将发布所有211设计及其数据作为该领域的资源。

---

### [使用 Claude 减少代码的攻击面](https://www.anthropic.com/research/attack-surface-reduction)

**来源**: Red Team

**发布日期**: 2026-10-20

**原文**: https://www.anthropic.com/research/attack-surface-reduction

**中文摘录**：

自动攻击面分析和减少可以在短期内有意义地提高已部署软件的安全性。在这篇文章中，我们预览了使用 Claude 将攻击面缩减技术应用于大型开源代码库所收集的数据。在过去的一年中，我们发布了大量数据，表明frontier AI模型能够发现和利用安全漏洞。然而，展示此前未知的漏洞可能被如何利用，仅仅只是前沿人工智能模型在网络安全防御领域所能发挥作用的开端。

---

### [通过将不良行为局部化而非直接惩罚，来减少奖励滥用](https://alignment.anthropic.com/2026/graft)

**来源**: Alignment Science

**发布日期**: 2026-10-19

**原文**: https://alignment.anthropic.com/2026/graft

**中文摘录**：

在训练过程中，模型有时会学会通过“作弊”来完成任务，而不是按照预期的方式解决问题，这种现象被称为奖励漏洞（reward hacking）。一种缓解措施是使用自动化监测系统来检测并惩罚攻击行为，但这可能会使模型学会以监测系统无法发现的方式进行攻击。我们提出了GRAFT方法，该方法将由检测到的攻击所引发的学习更新仅限于一组特定的参数，并在训练完成后将其移除。我们发现，移除这些参数可以有效防止奖励漏洞，包括那些连监控机制都无法检测到的漏洞。在我们的实验中，尽管仅限于小型模型和简单的监控机制，该方法能够在防止奖励漏洞的同时，仍能引导模型完成预期任务。

---

### [投资于公共利益](https://www.anthropic.com/news/public-benefit-fund)

**来源**: Anthropic News

**发布日期**: 2026-10-18

**原文**: https://www.anthropic.com/news/public-benefit-fund

**中文摘录**：

我们将Anthropic的部分股份注入Anthropic公益基金，该基金为一家新设立的实体，其架构会随着公司的发展而逐步提升持股比例。今天，我们将 Anthropic 的部分股份投入到 Anthropic 公益基金，这是一个新的实体，其结构会随着公司的发展而增加股份。在获得股东批准的前提下，今日将锁定Anthropic公司5%的股份；此外，当公司估值较设定基准每增长50%时，董事会可酌情再追加2%的股份锁定。作为一家公益公司，我们的大部分工作都在公司内部进行: 与AI安全性和可解释性相关的研究; 应用生物医学研究; 非营利组织和科研机构的 Claude 折扣。

---

### [在前沿领域工作塑造了对未来的期望。](https://www.anthropic.com/research/expectations-for-the-future)

**来源**: Anthropic Research

**发布日期**: 2026-10-16

**原文**: https://www.anthropic.com/research/expectations-for-the-future

**中文摘录**：

我们分享两份报告：第一份报告探讨了人工智能如何改变Anthropic内部的就业状况，第二份报告则分析了公众与Anthropic员工在人工智能对工作和经济影响方面的预期差异。Anthropic 员工和美国工人似乎对人工智能如何影响就业并没有不同的看法。相反，他们对人工智能能力的认知存在差异。这些不同的经历似乎与人们对未来工作形态的预期密切相关。Anthropic 是一家处于人工智能应用前沿的企业，而这种应用已经改变了我们的招聘方式。我们发现，过去一年中，我们在初级岗位上的招聘比例有所下降，同时从事技术类岗位的员工占比也有所减少。

---

### [Anthropic的就业状况正在发生怎样的变化](https://www.anthropic.com/research/employment-at-anthropic)

**来源**: Anthropic Research

**发布日期**: 2026-10-16

**原文**: https://www.anthropic.com/research/employment-at-anthropic

**中文摘录**：

人工智能如何重塑了Anthropic的工作与就业？作为一家处于人工智能应用前沿的企业，Anthropic可能成为衡量人工智能如何在整个经济体中重塑工作组织、招聘模式及劳动力需求的先行指标。在人工智能日益强大的背景下，我们有望看到哪些工作与就业方面的变革？Anthropic 值得研究，因为它已将其工作流程全面融入人工智能。助理们穿梭于Slack聊天中，并安排会议。它们能够自主修复缺陷，并协同攻克大型工程项目。客服人员的工作时长是人工的6倍。当前在Anthropic发生的变革，正在为未来的工作与就业趋势发出重要信号。

---

### [Claude 显示ECDSA曲线原点](https://www.anthropic.com/research/ecdsa-curve-origins)

**来源**: Red Team

**发布日期**: 2026-10-16

**原文**: https://www.anthropic.com/research/ecdsa-curve-origins

**中文摘录**：

已经解释了几十年来最流行的加密标准之一的起源之谜。我们想追上Jerry Solinas，他被贴上了 “邪恶的互联网模因” 和 “NSA bogeymen的Yo La Tengo” 的幽默。还要感谢Filippo Valsorda组织NIST椭圆曲线种子赏金。

---

### [用 Claude 设计更高效的量子电路](https://www.anthropic.com/research/designing-efficient-quantum-circuits)

**来源**: Anthropic Research

**发布日期**: 2026-10-16

**原文**: https://www.anthropic.com/research/designing-efficient-quantum-circuits

**中文摘录**：

Claude 设计的量子电路主要靠自己工作，在最好的出版版本上有所改进，在某些情况下改进了一个数量级或更多。量子计算机需要精心设计的量子线路，才能在有限的硬件上运行有用的算法。我们为八个这样的电路提供了 Claude 的简单语言规范，这些规范来自化学，优化，物理模拟和数论，以及一个自动评估器，可以检查和评分每个设计。Claude 在很大程度上依靠自己的工作，发现设计可以改善已发布的最佳电路，在某些情况下可以改善一个数量级或更多。这样的改进大大减少了有用应用程序所需的量子资源，因此实用的量子计算机可能比以前预期的更快到达。

---

### [人工智能期望差距](https://www.anthropic.com/research/ai-expectations-gap)

**来源**: Anthropic Research

**发布日期**: 2026-10-16

**原文**: https://www.anthropic.com/research/ai-expectations-gap

**中文摘录**：

未来几年，AI将如何重塑经济？关于人工智能未来对经济的影响，分歧的核心来源是什么？本说明就这些问题提出了新的调查证据。Szymon Sacher，Tess Cotter，Charles I. Jones，Anton Korinek，Peter McCrory未来几年AI将如何重塑经济？人工智能能力正在迅速发展，未来的人工智能模型可能能够建立自己的继任者 (递归自我改进)，这可能会进一步加快进展速度。这可能实现的速度有多快，达到什么程度尚不清楚。预测差异很大，而且争论激烈。关于人工智能未来对经济的影响，分歧的核心来源是什么？

---

### [使用 Claude | Claude 说明书查看您的客服人员会话中的安全问题](https://platform.claude.com/cookbook/managed-agents-cma-agent-security-review)

**来源**: Claude Cookbook

**发布日期**: 2026-10-16

**原文**: https://platform.claude.com/cookbook/managed-agents-cma-agent-security-review

**中文摘录**：

构建针对已完成客服会话的评价系统。它会将托管代理会话、消息API日志或代理SDK日志转化为文本记录，标记代码中异常之处，在托管代理的动态工作流中由Claude对每条会话进行审核，并返回一份附有引用证据的排序报告。代理程序无需人工干预即可运行。查看他们事后所采取的行动，可以揭示出您的网络边界、权限策略和凭据管理存在哪些未按预期设置得更为宽松的地方。本手册将构建一项审核功能，该功能会读取您的客服人员已完成的对话，并查找超出您所允许范围的操作；您将获得一份按优先级排序的对话列表，其中每条记录都附有相关证据。它会读取托管代理会话、消息API日志或Claude代理SDK日志。网络限制和权限策略阻止了相关操作。

---

### [一位Anthropic日本BDR如何与一支由Claude名客服代表组成的团队共度一天](https://claude.com/resources/articles/how-an-anthropic-japan-business-development-representative-runs-his-day)

**来源**: Claude Blog

**发布日期**: 2026-10-16

**原文**: https://claude.com/resources/articles/how-an-anthropic-japan-business-development-representative-runs-his-day

**中文摘录**：

一位业务拓展专员如何借助Claude托管代理和Claude标签，快速处理其待办邮件并撰写双语客户邮件。

---

### [关于独立评估员的Anthropic更新](https://www.anthropic.com/news/an-update-on-independent-evaluators)

**来源**: Anthropic News

**发布日期**: 2026-10-15

**原文**: https://www.anthropic.com/news/an-update-on-independent-evaluators

**中文摘录**：

上个月，我们承诺对我们的模型和安全实践进行更强有力的独立第三方评估。我们还签署了《白宫超人工智能协议》，其中各公司承诺与独立的外部审计机构或评估机构开展合作。今天，我们宣布，我们已经开始向员工提供类似METR团队的访问权限，METR是一家评估前沿人工智能模型的非营利组织。METR将公布其风险评估结果。在过去的一年中，我们与METR合作对我们的风险报告进行了多次审查。我们还与SecureBio和埃森哲合作作为评估人员，并正在与其他几个组织进行早期讨论，包括拥抱脸。

---

### [Claude代码团队如何进行代码评审/claude.dev博客](https://claude.dev/blog/solving-code-review-at-anthropic)

**来源**: Claude Blog

**发布日期**: 2026-10-15

**原文**: https://claude.dev/blog/solving-code-review-at-anthropic

**中文摘录**：

你们如何审查代理商所产出的大量代码？在Claude代码团队，一旦我们的测试覆盖率达到较高水平并实施了深度代码评审，我们便开始优化，力求将人工评审时间降至最低，同时确保不会引发回滚或事故。我们之前说过，Claude大约编写了Claude Code自身代码的90%。那么，我们如何在如此大规模的代码产出下进行代码评审呢？还有人看代码吗？那如果有什么东西坏了，谁来接住它呢？本文介绍了Claude代码团队的代码评审流程及其演进历程。从6月到9月，合并到Claude Code代码库的拉取请求数量增长了一倍以上，而不得不回滚的拉取请求占比则下降了40%以上。我们没有删除评论。

---

### [代码评审现已全面可用。](https://claude.com/resources/articles/code-review-is-now-generally-available)

**来源**: Claude Blog

**发布日期**: 2026-10-15

**原文**: https://claude.com/resources/articles/code-review-is-now-generally-available

**中文摘录**：

在缺陷进入生产环境之前，尽早发现更多问题。代码评审功能现已面向 Claude 团队版和企业版组织全面开放。代码评审已退出研究预览阶段，现向Claude团队版和企业版组织开放。编码助手持续提升团队的代码编写速度，但代码评审的瓶颈仍未缓解。在正式发布版本中，我们提升了代码审查的速度，增强了其发现关键缺陷的能力，并使其更易于针对每个代码库进行个性化配置。自我们发布研究预览版以来，代码审查功能已更加完善，能够发现更多原本可能进入生产环境的缺陷。我们还在 Anthropic 对拉取请求执行代码评审，这让我们能够了解哪些评审环节拖慢了我们自身工程师的进度。

---

### [通过强化学习培训合规审计员](https://alignment.anthropic.com/2026/training-alignment-auditors)

**来源**: Alignment Science

**发布日期**: 2026-10-15

**原文**: https://alignment.anthropic.com/2026/training-alignment-auditors

**中文摘录**：

我们使用强化学习培训了LLM名对齐审计员。在我们的训练环境中，策略会针对在其系统提示中植入了隐蔽行为的目标模型进行探测。在该环境中对Haiku 4.5进行微调后，其在用于审计质量的保留评估集上的表现与Opus 4.6相当，并且能够泛化到不同框架下的更难、经过微调的目标上。前沿模型开发者在部署前的评估中越来越多地依赖自动化审计系统（Anthropic，2025）。在这些系统中，一名LLM审核员会在多个场景下的多轮交互中对候选模型进行评估，以探查其是否存在值得关注或非预期的行为。

---

### [新加坡办公室与政府的谅解备忘录 | Anthropic](https://www.anthropic.com/news/singapore-office-opening)

**来源**: Anthropic News

**发布日期**: 2026-10-14

**原文**: https://www.anthropic.com/news/singapore-office-opening

**中文摘录**：

Anthropic 在新加坡开设第五个亚太办事处，并与政府签署关于人工智能安全、评估和负责任采用的谅解备忘录。今天，我们通过在新加坡开设新办事处——这是我们在此地区的第五家办事处——并同新加坡数字发展与信息部签署谅解备忘录，进一步拓展我们在亚太地区的业务。新加坡是我们在全球最活跃的市场之一，并且已经为新加坡的商业和政府服务提供动力，每天有数百万人使用，例如新加坡GovTech，Grab和DBS。我们不断壮大的本地团队将确保这些组织和更多组织通过安全、有能力的人工智能留在前沿。

---

### [为2026年美国中期选举做准备](https://www.anthropic.com/news/2026-us-midterms)

**来源**: Anthropic News

**发布日期**: 2026-10-14

**原文**: https://www.anthropic.com/news/2026-us-midterms

**中文摘录**：

今年早些时候，我们发布了有关选举保障措施的最新进展。在此，我们概述了在本年度美国中期选举前夕，我们如何持续强化这些保障措施。今年早些时候，我们分享了我们的选举保障措施的最新情况，其中描述了我们如何衡量和防止政治偏见，检测滥用，并引导人们获得准确的投票信息。以下，我们概述了如何在这一基础上进一步完善，并在今年美国中期选举前持续强化我们的选举保障措施。我们的目标是使 Claude 成为政治对话的有用工具，同时防止与选举有关的滥用。首先要了解人们在这些情况下如何实际使用 Claude。

---

### [在Claude平台上使用OpenTelemetry进行链路追踪](https://claude.com/resources/articles/agent-observability-on-the-claude-platform)

**来源**: Claude Blog

**发布日期**: 2026-10-14

**原文**: https://claude.com/resources/articles/agent-observability-on-the-claude-platform

**中文摘录**：

宣布在Claude平台上推出来自Claude托管代理的OpenTelemetry跟踪、消息 API 以及 Claude SDK。

---

### [在Anthropic重新设计源代码管理](https://www.anthropic.com/research/redesigning-source-control)

**来源**: Engineering Blog

**发布日期**: 2026-10-13

**原文**: https://www.anthropic.com/research/redesigning-source-control

**中文摘录**：

随着我们每天的合并次数增长了十倍以上，源代码管理成为了我们最大的开发瓶颈。在此，我们分享了如何在五个月内迁移到自建版本控制系统的过程。已于10月15日更新，新增了关于我们如何在Scion中应用的诸多技术所源自的早期项目的更多详细信息。在Anthropic，编码已不再是构建系统或开展研究的瓶颈。Claude 能够自主迭代研究流程，对复杂程序进行微观优化，并以前所未有的速度和规模从零开始构建新服务。如今的瓶颈在于所有为人工规模构建的开发者基础设施：版本控制、构建流程以及持续集成。

---

### [使用OpenTelemetry跟踪 Claude API 个请求和托管代理会话 | Claude 教程](https://platform.claude.com/cookbook/observability-opentelemetry-tracing)

**来源**: Claude Cookbook

**发布日期**: 2026-10-13

**原文**: https://platform.claude.com/cookbook/observability-opentelemetry-tracing

**中文摘录**：

逐个属性地读取OpenTelemetry通过Python SDK为消息 API 请求、流、工具运行器循环以及托管代理会话所发出的跨度。然后将其导出到OTLP后端，并添加一个控制台输出目标，以便 API 的服务端跨度加入同一跟踪中。一个缓慢或昂贵的Claude请求无法告诉你时间和令牌都用在了哪里。OpenTelemetry（OTel）确实会生成跨度，这些跨度来自两个来源。Claude SDK会在您的进程中生成跨度，每发送一个请求就会生成一个。Claude API 会在 Anthropic 的端侧为每个请求内部的各项工作生成跟踪数据，并将其直接发送至您的可观测性后端。SDK会为每条请求添加一个traceparent头，而 API 则在其下挂载自己的跨度，因此这两者都会与您自己的处理器跨度和数据库跨度一起归入同一条调用链中。

---

### [优步首席信息安全官谈如何构建面向人工智能的内部威胁防护体系](https://claude.com/resources/articles/uber-s-ciso-on-building-an-insider-threat-program-for-ai)

**来源**: Claude Blog

**发布日期**: 2026-10-13

**原文**: https://claude.com/resources/articles/uber-s-ciso-on-building-an-insider-threat-program-for-ai

**中文摘录**：

AI智能体的监控与可观测性的重要性，以及Uber的开源工具如何与Anthropic的企业前沿安全防护机制协同工作。优步的首席信息安全官菲利普·马丁就人工智能代理的监控与可观测性的重要性，以及优步的开源工具如何与企业级前沿安全防护机制协同工作进行了阐述。

---

### [AI模型可能能够在不访问数据中心的情况下进行自我复制](https://www.anthropic.com/research/self-replicating-ai)

**来源**: Red Team

**发布日期**: 2026-10-12

**原文**: https://www.anthropic.com/research/self-replicating-ai

**中文摘录**：

小型人工智能模型可能只有几个月的时间才能在Android电视盒等廉价物联网设备上进行自我复制，而不需要数据中心。我们的实验表明，小型人工智能模型可能需要几个月的时间才能在商业物联网 (IoT) 设备上进行自我复制，如智能烤箱和非品牌Android电视盒。像这样的复制器将是具有挑战性的关闭，因为没有集中点关闭-尽管它可能很慢 (数天的倍增时间)。与非人工智能恶意软件不同，它还可以自己找出不熟悉的设备。在我们的评估中，一个90亿参数的模型能够在我们测试的9种硬件类型中的8种上进行推理。

---

### [加强我们对蒸馏攻击的防御能力](https://www.anthropic.com/news/distillation-defenses)

**来源**: Anthropic News

**发布日期**: 2026-10-12

**原文**: https://www.anthropic.com/news/distillation-defenses

**中文摘录**：

非法蒸馏允许模型开发人员复制frontier AI功能，而无需创建成比例的强大保护措施。在这里，我们描述了我们如何将蒸馏速率降低90% % 以上。最近几个月，我们在使用新方法降低 Claude 蒸馏攻击的有效性方面取得了实质性进展，正如我们在本博客中概述的那样。早期证据表明，这些方法已将蒸馏器收集的数据量减少了约90至99%。蒸馏攻击是秘密的，工业规模的活动，在没有原始模型开发人员授权的情况下，提取一个模型的功能并将其复制到另一个模型中。他们经常使用欺诈账户网络进行。

---

### [调查我们的评估和内部使用中的意外模型行为](https://www.anthropic.com/research/investigating-unintended-model-actions)

**来源**: Anthropic Research

**发布日期**: 2026-10-09

**原文**: https://www.anthropic.com/research/investigating-unintended-model-actions

**中文摘录**：

本报告描述了我们在评估和内部使用 Claude 期间观察到的意外模型操作的示例。这是我们努力的一部分，发布更频繁的关于模型行为和对齐的独立报告，超出我们的系统卡，我们在每个模型版本中发布，以及我们的风险报告，我们每三到六个月发布一次，作为我们负责任的扩展策略的一部分。我们相信，在测试和使用过程中，我们看到我们的模型所做的事情是透明的，这一点很重要。我们选择不命名下面示例中涉及的组织，以避免暴露其系统中的漏洞，并应他们的要求。出于这个原因，我们提供的每个案例的细节也比其他情况少。下面描述的一些案件涉及美国运营的网站。

---

### [使用 Claude 科学在紫外线下制作第一张完整的天空图](https://www.anthropic.com/research/the-missing-map-of-the-sky)

**来源**: Anthropic Research

**发布日期**: 2026-10-08

**原文**: https://www.anthropic.com/research/the-missing-map-of-the-sky

**中文摘录**：

在这里，约翰霍普金斯大学的天体物理学家，Anthropic 的研究员bricemnard解释了他如何与 Claude Science合作制作第一张完整的紫外线天空图。该地图将是一个有价值的教育工具，让学生详细了解在这个波长下可见的银河系的丰富结构。整个天空，银河系中心在中间，紫外线 (结合远紫外线154 nm和近紫外线232 nm)。这张地图的大约三分之一，包括银河系平面的大部分，是由 Claude Science使用本文概述的方法预测的。地图的其他图层将每个像素标记为 “测量” 或 “预测”，并提供不确定性估计; 你可以在这里看到它。

---

### [一种针对开源软件的选择加入漏洞查找服务](https://www.anthropic.com/research/launching-opt-in-vuln-finding-service-for-open-source)

**来源**: Red Team

**发布日期**: 2026-10-08

**原文**: https://www.anthropic.com/research/launching-opt-in-vuln-finding-service-for-open-source

**中文摘录**：

我们正在推出OSS Scanner，这是一种针对开源生态系统的可选漏洞扫描程序，根据我们在Glasswing项目中使用 Claude 查找漏洞的经验。加入的项目将通过我们最强大的模型免费获得彻底的定期安全扫描。我们正在推出OSS Scanner，这是一种针对开源生态系统的可选漏洞扫描程序，根据我们在Glasswing项目中使用 Claude 查找漏洞的经验。加入的项目将通过我们最强大的模型免费获得彻底的定期安全扫描。正如我们在此博客上广泛报道的那样，语言模型在发现漏洞的能力方面迅速发展。

---

### [立足于我们对美国科学发现的承诺](https://www.anthropic.com/news/genesis-mission-commitment)

**来源**: Anthropic News

**发布日期**: 2026-10-08

**原文**: https://www.anthropic.com/news/genesis-mission-commitment

**中文摘录**：

Anthropic 将在三年内向“创世使命”项目投入1.5亿美元，这是一项旨在通过人工智能加速科学与技术发现的联邦倡议。Anthropic 通过在三年内为 “创世纪使命” (Genesis Mission) 投入1.5亿美元，加深了对美国科学研究的支持，这是一项通过人工智能加速科学技术发现的联邦计划。这笔资金将用于使 Claude 可供超过15个机构使用，这些机构是任务的一部分，包括NASA，美国国立卫生研究院和美国国家科学基金会。我们首先宣布了与美国能源部 (DOE) 和Genesis Mission去年12月的合作伙伴关系。从那时起，我们与美国能源部合作，将 Claude 带给国家实验室的科学家。

---

### [隆重推出Anthropic网络任务](https://www.anthropic.com/news/anthropic-cyber-mission)

**来源**: Anthropic News

**发布日期**: 2026-10-08

**原文**: https://www.anthropic.com/news/anthropic-cyber-mission

**中文摘录**：

我们正在启动“Anthropic”网络任务，这是一项旨在保障所有人所依赖的系统安全的长期承诺。今天，我们启动了 Anthropic Cyber Mission，这是一项保护每个人都依赖的系统的长期承诺。网络任务是一项新的努力，旨在通过工具，研究和资源来支持防御者，以保护其软件和系统。我们从两个领域开始: 前沿模型可能被滥用来利用漏洞和进行网络操作。尽管尽了最大努力，但许多技术领域仍然处于危险的暴露状态。国家支持的对手花了数年时间在许多部门的这些系统中站稳脚跟，以便他们可以破坏它们。

---

### [2026年使用政策更新](https://www.anthropic.com/news/2026-usage-policy-update)

**来源**: Anthropic News

**发布日期**: 2026-10-08

**原文**: https://www.anthropic.com/news/2026-usage-policy-update

**中文摘录**：

我们正在发布新版本的使用政策。在这篇文章中，我们总结了我们所做的更改。Anthropic 每年都会更新其使用政策，以响应我们模型不断发展的功能以及我们从客户那里收到的反馈。我们今天将发布该政策的新版本。在这篇文章中，我们总结了我们所做的更改。最新版本中的大多数更新旨在阐明现有规则。自上次更新以来的一年中，Claude 承担了更长，更独立的工作。此更新提供了新的示例，说明我们的规则如何应用于 Claude 的新功能。

---

### [构建高效的代理自动化/claude.dev博客](https://claude.dev/blog/building-effective-agent-automations)

**来源**: Claude Blog

**发布日期**: 2026-10-08

**原文**: https://claude.dev/blog/building-effective-agent-automations

**中文摘录**：

随着人工智能加速我们的工作，跟上节奏变得愈发困难。在Anthropic，简单的自动化代理经常被用来提供帮助。它们通常按预定时间运行，在后台收集上下文信息，并主动告知我们需要了解的内容。但构建有效的代理自动化并不容易：它们可能会在无人察觉的情况下失去对某个数据源的访问权限，或者无法遵循我们的偏好设置。借助 Claude 托管代理（测试版），我们构建了一个参考实现，该实现可按计划读取自定义数据源（例如Slack和GitHub代码库），跟踪自上次运行以来发生的变化，并将您需要了解的信息发布出去（例如推送到Slack）。在本文中，我们将逐步介绍每个步骤，分享一个参考实现，并提供一条可在 Claude Code中运行的命令，以帮您配置代理。

---

### [Block如何在数千个拉取请求中协调 Claude Fable的开发](https://claude.com/resources/articles/how-block-orchestrates-claude-fable-across-thousands-of-pull-requests)

**来源**: Claude Blog

**发布日期**: 2026-10-08

**原文**: https://claude.com/resources/articles/how-block-orchestrates-claude-fable-across-thousands-of-pull-requests

**中文摘录**：

布拉德利·阿克森讲述了Anthropic的Claude Fable 5如何在Block公司范围内统筹实施代码迁移。Block公司人工智能能力负责人布拉德利·阿克森就其团队如何评估新型大型语言模型、Fable 5如何统筹全公司范围内的代码迁移，以及为何在大规模部署前沿智能时，安全保障机制至关重要等问题发表了看法。

---

### [使用Claude构建实时仪表盘并制作动画解说视频](https://claude.com/resources/articles/dashboards-and-motion)

**来源**: Claude Blog

**发布日期**: 2026-10-08

**原文**: https://claude.com/resources/articles/dashboards-and-motion

**中文摘录**：

即日起，Claude 仪表板和 Claude 动作功能处于测试阶段。文档、幻灯片和设计功能已退出测试阶段，并且在所有Claude套餐中均可使用，包括免费版。Claude 仪表板和 Claude Motion现已进入测试阶段。文档、幻灯片和设计功能已退出测试阶段，并且在所有Claude套餐中均可使用，包括免费版。

---

### [扩展网络验证计划](https://www.anthropic.com/news/cyber-verification-program)

**来源**: Anthropic News

**发布日期**: 2026-10-06

**原文**: https://www.anthropic.com/news/cyber-verification-program

**中文摘录**：

我们正在推出新的扩展版本的网络验证计划 (CVP)，该计划为合格的安全专业人员提供高级网络功能和减少的阻止分类器。该计划现在由三个访问层组成，允许安全团队申请最适合其工作的访问级别。每一层都可以访问我们最有能力的模型，包括 Claude Opus 5.5、 Claude Sonnet 5.5、 Claude Mythos 5.1和未来的新模型。有兴趣的客户可以在这里申请。网络安全本质上是双重用途: 使安全团队能够找到并修复漏洞的相同功能也可以帮助恶意行为者利用它。

---

### [我们正在扩展Claude初创企业计划，以帮助创业者打造](https://claude.com/resources/articles/were-expanding-the-claude-startups-program-to-help-founders-build)

**来源**: Claude Blog

**发布日期**: 2026-10-06

**原文**: https://claude.com/resources/articles/were-expanding-the-claude-startups-program-to-help-founders-build

**中文摘录**：

Claude团队计划一年期，API个积分，以及助力运营一家原生人工智能公司的工具特惠等更多权益。更新：2026年10月13日，我们目前的学员名额已满，暂不接受新的申请。请访问Claude初创企业页面，了解更多详情并查看常见问题解答。今天，我们正在扩展“Claude 创业者计划”，这是一项面向在 Claude 平台上创建企业的创始人的项目。会员权益包括一年的Claude团队版套餐、API个积分、助力运营AI原生企业的工具专属优惠，以及与Anthropic应用AI团队的线上答疑时间等。将一个想法转化为产品的可能性，从未如此之高。一个小团队可以在创纪录的时间内开发出原型，即使没有编程背景的人也能交付可用的软件。

---

### [康卡斯特和博思艾伦如何利用Claude Mythos发现漏洞利用链并保障其代码库的安全](https://claude.com/resources/articles/how-comcast-booz-allen-use-claude-mythos-to-secure-their-codebases)

**来源**: Claude Blog

**发布日期**: 2026-10-06

**原文**: https://claude.com/resources/articles/how-comcast-booz-allen-use-claude-mythos-to-secure-their-codebases

**中文摘录**：

康卡斯特和博思艾伦公司的安全团队通过“玻璃翼”项目，利用Claude款神话级模型，发现了并验证了现有扫描工具未能检测到的漏洞，并完成了修复。

---

### [Claude 现在支持Google文档、表格和幻灯片。](https://claude.com/resources/articles/claude-now-works-in-google-docs-sheets-and-slides)

**来源**: Claude Blog

**发布日期**: 2026-10-06

**原文**: https://claude.com/resources/articles/claude-now-works-in-google-docs-sheets-and-slides

**中文摘录**：

借助我们面向Google Workspace的全新 Claude 插件及连接器（处于测试阶段），您可以将 Claude 集成到您的Google文档中，或直接在 Claude 中处理您的文档。使用Google Workspace的团队现在可以通过我们的全新插件以及处于测试阶段的Google文档、表格和幻灯片连接器，将 Claude 嵌入其文件中，或直接在 Claude 中处理这些文件。

---

### [Cresta如何将CX专业知识转化为 Claude 代理SDK上的代理构建器](https://claude.com/resources/articles/how-cresta-turned-cx-expertise-into-an-agent-builder-on-the-claude-agent-sdk)

**来源**: Claude Blog

**发布日期**: 2026-10-05

**原文**: https://claude.com/resources/articles/how-cresta-turned-cx-expertise-into-an-agent-builder-on-the-claude-agent-sdk

**中文摘录**：

了解Cresta如何在 Claude 代理SDK上构建Conductor (构建其他代理的代理)，以及团队如何使用每个新的 Claude 模型对其进行评估。

---

### [Claude Frontier Academy: 100美元培训10,000工程师](https://www.anthropic.com/news/claude-frontier-academy)

**来源**: Anthropic News

**发布日期**: 2026-10-02

**原文**: https://www.anthropic.com/news/claude-frontier-academy

**中文摘录**：

Claude Frontier Academy trains Frontier按照 Anthropic 自己的标准部署了工程师-10000万美元的承诺在2027年年底之前培训10,000。这所一流的学院使用与 Anthropic 自己的工程师相同的技能标准来培训前沿部署的工程师，从埃森哲、贝恩、凯捷、澳大利亚联邦银行、德勤、麦肯锡、摩根士丹利、诺和诺德等公司的团队开始。今天，我们启动了 Claude Frontier Academy，以解决人工智能实施中最紧迫的问题之一: 人才。在10000万美元的支持下，Anthropic 旨在到2027年底培训10,000名FDEs部署工程师。

---

### [Claude-形科学](https://www.anthropic.com/research/claude-shaped-science)

**来源**: Anthropic Research

**发布日期**: 2026-10-01

**原文**: https://www.anthropic.com/research/claude-shaped-science

**中文摘录**：

Matthew Schwartz描述了当他停止 Claude 战斗并允许 Claude 发现 “Claude 形” 问题时发生的事情。这促使他建立了BootLoops，这是一个用于定量科学精确计算的工具包，他一直在与专家一起应用于科学领域。在这篇客座文章中，Matthew Schwartz教授再次描述了人工智能加速科学的新方法。在《Vibe Physics》中，Schwartz讨论了 Claude 和物理学研究生在能力上的相似之处。在这里，他描述了当他停止战斗 Claude 并允许 Claude 找到 “Claude 形” 问题时发生的事情: 最适合当前 LLM 工具功能的问题。这促使他建立了BootLoops，这是一个用于定量科学精确计算的工具包。

---

### [巴克莱规模 Claude 以升级运营并改善客户体验](https://www.anthropic.com/news/barclays-scales-claude)

**来源**: Anthropic News

**发布日期**: 2026-10-01

**原文**: https://www.anthropic.com/news/barclays-scales-claude

**中文摘录**：

英国全能银行巴克莱 (Barclays) 正在扩大与 Anthropic 的战略合作，以在其全球运营中集成安全的企业级AI系统。Barclays正在整个银行范围内扩展 Claude，以加速软件开发，现代化遗留系统并提高运营效率。作为此次部署的一部分，巴克莱预计到2026年年底，代码采用率将达到50% % 的开发人员，2027年软件工程师的人数将上升到大多数。在大型、复杂和高度监管的组织中集成人工智能需要有能力的技术和规范的治理。

---

### [在TypeScript中使用mods自定义 Claude 代码](https://claude.com/resources/articles/claude-code-mods)

**来源**: Claude Blog

**发布日期**: 2026-10-01

**原文**: https://claude.com/resources/articles/claude-code-mods

**中文摘录**：

Mod是小型的TypeScript函数，它改变了 Claude 代码的工作方式。重写提示、阻止有风险的命令、添加自定义UI或替换内置功能。自己写一个或要求 Claude 代码编写它，然后将其作为插件共享。今天我们将介绍mods，这是一个小的TypeScript函数，它改变了 Claude 代码的工作方式。mod可以重写提示，添加新的UI，替换内置功能或添加全新的功能。你可以自己写一个mod，或者让 Claude 代码为你写一个。Mods船里面的插件，所以你安装和分享他们像任何插件。它们在 Claude 代码CLI和桌面应用程序中工作。Mods以与 Claude 代码本身相同的方式运行您的机器。

---

### [我们能预测机器人会做什么工作吗？](https://www.anthropic.com/research/what-work-can-robots-do)

**来源**: Anthropic Research

**发布日期**: 2026-09-30

**原文**: https://www.anthropic.com/research/what-work-can-robots-do

**中文摘录**：

机器人能做什么工作？Anthropic 的机器人暴露指数发现，机器人可以完成我们3/4的体力劳动任务，但仅在0.3% 方面具有成本竞争力。大型语言模型的进步提高了自动化大量工作的可能性。但许多工作是体力劳动。人工智能对经济的影响将部分取决于机器人技术。¹ 预测机器人进步的速度是困难的，但我们认为，列举今天的能力可以为未来几年提供洞察力。我们使用 Claude 来评估当今机器人执行工作任务的能力。当机器人能够在更不稳定的环境中完成更多工作任务时，该岗位的自动化风险就会更高。当机器人完成同一项任务的成本低于人工时，它就具备了成本竞争力。

---

### [Anthropic的销售团队如何借助Claude的托管代理团队重建了潜在客户引流流程](https://claude.com/resources/articles/how-anthropics-sales-team-rebuilt-inbound-with-claude-managed-agents)

**来源**: Claude Blog

**发布日期**: 2026-09-30

**原文**: https://claude.com/resources/articles/how-anthropics-sales-team-rebuilt-inbound-with-claude-managed-agents

**中文摘录**：

如今，由Claude驱动的智能客服代理能够自动解答大多数潜在客户的咨询，这一变化也重塑了我们销售团队的工作方式。Anthropic的销售拓展负责人卡尔·约翰逊分享了这一转型如何改变我们的销售团队运作模式。

---

### [Claude 适用于政府](https://claude.com/resources/articles/claude-for-government-is-now-generally-available)

**来源**: Claude Blog

**发布日期**: 2026-09-30

**原文**: https://claude.com/resources/articles/claude-for-government-is-now-generally-available

**中文摘录**：

Microsoft 365的 Claude 代码CLI和 Claude 现在也可以在early access中使用。今天，联邦和州机构通常可以使用 Claude for dovernment。该平台通过FedRAMP高授权环境提供 Claude 的编码和代理工作功能，自7月以来一直处于公测阶段。代理商可以访问与 Anthropic 的商业客户相当的功能，而不会影响合规性要求。新功能通常以商业发布节奏到达。Claude 直接处理桌面上的文件，允许机构工作人员使用技能、插件和项目来创建备忘录、RFP审查、案例工作和其他任务。通过 Claude 代码，公共部门团队可以构建支撑公共服务的软件系统并使其现代化。

---

### [你希望人工智能为你带来什么？](https://www.anthropic.com/research/your-thoughts-on-ai)

**来源**: Anthropic Research

**发布日期**: 2026-09-29

**原文**: https://www.anthropic.com/research/your-thoughts-on-ai

**中文摘录**：

我们正在开展一项新研究，将使用Anthropic访谈员，以从您与人工智能的互动经验中汲取insights。我们正在开展一项新研究，将使用Anthropic访谈工具，以了解您与人工智能的互动体验，诚邀您参与。完成后，您可以选择将您的访谈公开，这样不仅Anthropic，任何人都可以阅读并从中学习。您可以在这里参与。我们正处于人工智能发展的关键节点，其日益增强的能力使其既可能变得更加有用，也可能变得更加危险。前沿人工智能正以前所未有的速度推动科学与医学领域的重大发现，与此同时，其被滥用的代价也愈发沉重——单次安全事件造成的损害已远超一年前。

---

### [GLM-5.3和先进网络能力的传播](https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities)

**来源**: Red Team

**发布日期**: 2026-09-29

**原文**: https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities

**中文摘录**：

GLM-5.3可以自主构建端到端的网络漏洞利用，但与其他前沿模型不同，它的发布没有有意义的保护措施来限制滥用。安德鲁·法萨诺、马里乌斯·弗莱舍·科尔·麦克福尔、罗伯特·肖、特里普·加拉格尔五个月前，我们宣布了 Claude Mythos Preview，这是第一个可以自主构建复杂的端到端网络攻击的人工智能模型。人工智能的快速改进向我们表明，这种能力最终会扩散到许多其他模型，使恶意网络行为者更容易发动极具影响力的网络攻击。

---

### [您可以指导的代理: Asana如何使用 Claude 构建人工代理团队](https://claude.com/resources/articles/agents-you-can-coach-how-asana-builds-human-agent-teams-with-claude)

**来源**: Claude Blog

**发布日期**: 2026-09-29

**原文**: https://claude.com/resources/articles/agents-you-can-coach-how-asana-builds-human-agent-teams-with-claude

**中文摘录**：

Asana首席产品官Arnab Bose介绍了Asana如何将 Claude 支持的AI代理作为具有范围角色、共享内存和每个人都能看到的工作的队友来运行。Asana首席产品官Arnab Bose介绍了Asana如何将AI代理作为具有范围角色，共享内存和每个人都能看到的工作的队友来运行。

---

### [使用 Claude 自动化评估设计与爬山算法/claude.dev博客](https://claude.dev/blog/automating-eval-design-and-hillclimbing)

**来源**: Claude Blog

**发布日期**: 2026-09-28

**原文**: https://claude.dev/blog/automating-eval-design-and-hillclimbing

**中文摘录**：

设计评估并在此基础上进行爬山优化而不自欺欺人的原则，以及Claude API技能的build-eval和hillclimb命令如何将这些原则付诸实践。评估能够反映您的应用或技能在特定任务上的表现情况。然而，设计评估方案并在不自欺的情况下提升评估表现，实属不易。我们已将这两项指南添加至claude-api技能中。借助该功能，您可以在代码库中运行 /claude-api build-eval来构建评估，并通过 /claude-api hillclimb对您的应用进行迭代优化，每次只做一项改动，同时使用预留的示例集来防止过拟合。

---

### [通过NVIDIA为公司提供对AI代理商的更多控制权](https://claude.com/resources/articles/giving-companies-more-control-over-their-ai-agents-with-nvidia)

**来源**: Claude Blog

**发布日期**: 2026-09-28

**原文**: https://claude.com/resources/articles/giving-companies-more-control-over-their-ai-agents-with-nvidia

**中文摘录**：

Anthropic 与NVIDIA合作，为其开放式agent安全平台的Agent堆栈提供额外的安全和控制层。注意: 本博客已从其原始版本进行了更新，以包含有关 Claude 托管代理的其他技术详细信息。

---

### [Claude 在N = 4个超级杨-米尔斯中计算九回路振幅](https://www.anthropic.com/research/yes-claude-can-do-nine-loops)

**来源**: Anthropic Research

**发布日期**: 2026-09-25

**原文**: https://www.anthropic.com/research/yes-claude-can-do-nine-loops

**中文摘录**：

在这篇客座文章中，物理学家兼科学作家马特·冯·希佩尔 (Matt von Hippel) 分享了他向人工智能公司发出关于他以前的理论物理学子领域的问题的挑战时所发生的事情。你发出挑战的情况并不常见，只是在一个月后看到它被击败。但是我们生活在不寻常的时代。让我自我介绍一下: 我是马特·冯·希佩尔。我曾经是一名理论物理学家; 现在我是一名科学作家。自始至终，我一直是一名博主，每周写一篇关于物理学和做物理学的人的t 4gravitons.com。越来越多的关于物理的博客意味着关于AI的博客。这是一个问题，因为我绝对不是AI专家。当然，我已经涉足了。我可能比你奶奶知道的更多。但我大多不得不退后一步，相信专家。

---

### [Opus 5.5/claude.Dev博客](https://claude.dev/blog/what-a-task-costs-on-opus-5-5)

**来源**: Claude Blog

**发布日期**: 2026-09-25

**原文**: https://claude.dev/blog/what-a-task-costs-on-opus-5-5

**中文摘录**：

相同的代币价格可以为每个任务花费非常不同的金额。了解 Claude 代码任务在 Opus 5.5上的费用以及哪些设置会更改账单。你不打算购买数百万个代币。您开始构建功能、完成迁移或运行任务。令牌计数是到达那里所需的模型。每个令牌成本相同的两个模型在同一任务上的成本可能非常不同。一个读一次代码。另一个读它，尝试修复，然后再读一遍。这些步骤中的每一个都是一个回合，并且每个回合都重新发送到目前为止的对话。因此，即使价格相同，需要更多转弯的模型也会花费更多。

---

### [使用目录提交门户为 Claude 构建插件](https://claude.com/resources/articles/build-plugins-for-claude)

**来源**: Claude Blog

**发布日期**: 2026-09-25

**原文**: https://claude.com/resources/articles/build-plugins-for-claude

**中文摘录**：

通过新的目录提交门户将插件提交到 Claude 目录。打包MCP连接器和代理技能，通过审查跟踪您的插件，并查看其使用情况和发现情况。一旦上线，您现在可以通过新的开发人员门户将插件提交到 Claude 目录，通过审查跟踪它们，并在上线后查看使用情况分析。

---

### [项目交换: 当代理商为我们进行交易时会发生什么？](https://www.anthropic.com/research/project-swap)

**来源**: Anthropic Research

**发布日期**: 2026-09-24

**原文**: https://www.anthropic.com/research/project-swap

**中文摘录**：

为了了解当代理商被派往市场时什么有效以及什么中断，我们制作了一个 Claudes的微型市场。生活中充满了交易和交易，这会让每个人都过得更好，但永远不会发生。这通常仅仅是因为找到合适的交易对手并进行谈判直到达成交易需要花费太多的工作。想想那些在他们负担不起的报价后跳过治疗的病人，当有一家不同的诊所收费低得多的时候，或者如果被问到，引用他们的医院会削减账单。或者想想你的工作。在某个地方，可能会有一个更适合你的，雇主会很乐意雇用你。但是你们可能找不到彼此，因为你们都没有时间不断地寻找。

---

### [Claude Tag现在支持频道中的个人连接器](https://claude.com/resources/articles/claude-tag-now-supports-personal-connectors-in-channels)

**来源**: Claude Blog

**发布日期**: 2026-09-24

**原文**: https://claude.com/resources/articles/claude-tag-now-supports-personal-connectors-in-channels

**中文摘录**：

Claude Tag现在可以使用您的连接器来处理您在通道中发出的请求。没有其他人可以使用它们，您可以控制如何呈现输出。

---

### [编码会话更长并且使用更多上下文。Claude Opus 5.5就是这样构建的。](https://claude.com/resources/articles/claude-opus-5-5-built-for-coding-sessions-that-use-more-context)

**来源**: Claude Blog

**发布日期**: 2026-09-24

**原文**: https://claude.com/resources/articles/claude-opus-5-5-built-for-coding-sessions-that-use-more-context

**中文摘录**：

我们最新的 Opus 模型经过了定价和培训，以优化开发人员现在编写代码的成本。对于按令牌计费的典型工作负载，我们估计 Claude Opus 的运行成本比 Opus 5低约40% 5.5。对于开发人员来说，这些节省的资金到底如何积累很重要。如果您按令牌支付，您将看到运行时间更长、上下文更高的会话的最大成本差异-Claude 代码会话的确切类型在过去六个月中变得更加普遍。这篇文章将深入探讨是什么让 Opus 5.5成本效益的机制，让开发人员今天 (可能明天) 如何编码。我们收集了有关开发人员从3月到2026年9月如何使用 Claude 代码的汇总数据。

---

### [Claude 发现一种新的酶系统](https://www.anthropic.com/research/claude-discovers-novel-enzyme-system)

**来源**: Anthropic Research

**发布日期**: 2026-09-23

**原文**: https://www.anthropic.com/research/claude-discovers-novel-enzyme-system

**中文摘录**：

在我们新的生命科学研究实验室的早期结果中，Claude 代理商发现了一种功能仍然未知的酶系统。我们将在 Anthropic 引入一个新的生命科学研究小组和实验室。我们的重点是使用 Claude: 探索DNA数据集以识别未表征的蛋白质家族，大规模生成假设，并通过实验室实验对其进行测试。这篇文章介绍了这项工作背后的团队，并分享了早期的结果，其中 Claude 发现了一种新的酶系统，其特性让人联想到CRISPR，只有我们科学家的高层指导。

---

### [如何为AI驱动的代码现代化项目做准备](https://claude.com/resources/articles/how-to-prepare-for-ai-driven-code-modernization-projects)

**来源**: Claude Blog

**发布日期**: 2026-09-23

**原文**: https://claude.com/resources/articles/how-to-prepare-for-ai-driven-code-modernization-projects

**中文摘录**：

代理可以在几个月内完成代码现代化，但变更管理仍然决定了步伐。定义目标、证书和促销政策的六个步骤。在我们的现场系列笔记中，Anthropic 前向部署的工程师分享了受实际客户部署启发的最佳实践。在本文中，我们分享了管理大型代码现代化项目的经验。代码现代化曾经是多年的，现在全员努力可以在几个月 (或几周) 内完成，但双方的组织工作通常保持不变。例如，对关键银行系统的每项变更都必须经过变更管理、审查和批准。这是一个强有力的过程，因为监管机构、审计师和企业都需要它。

---

### [CodeRabbit, Power Digital, ThoughtSpot on Claude Marketplace](https://claude.com/resources/articles/how-coderabbit-power-digital-and-thoughtspot-scale-with-snowflake-and-vercel-on-claude-marketplace)

**来源**: Claude Blog

**发布日期**: 2026-09-23

**原文**: https://claude.com/resources/articles/how-coderabbit-power-digital-and-thoughtspot-scale-with-snowflake-and-vercel-on-claude-marketplace

**中文摘录**：

CodeRabbit通过 Claude Marketplace扩展了其Vercel计划，Power Digital和ThoughtSpot将其Snowflake支出用于其 Anthropic 承诺。了解建立在 Claude 基础上的公司如何使用他们已经承诺为其运行的工具付费的预算。CodeRabbit通过 Claude Marketplace扩展了其Vercel计划，Power Digital和ThoughtSpot利用其现有的 Anthropic 承诺扩展了其雪花容量。

---

### [Claude Marketplace: 插件和连接器、产品和代理以及服务合作伙伴](https://claude.com/resources/articles/claude-marketplace)

**来源**: Claude Blog

**发布日期**: 2026-09-23

**原文**: https://claude.com/resources/articles/claude-marketplace

**中文摘录**：

Claude 市场将插件、连接器、代理和服务合作伙伴汇集到一个地方。查找使用 Claude 完成更多工作的工具和服务，或列出您为使用 Claude 的团队构建的内容。查找工具和服务，以便在 Claude 中做更多的事情，或者列出您为与 Claude 客户一起成长而构建的内容。

---

### [训练一个错位的奖励寻求者](https://alignment.anthropic.com/2026/reward-seeker)

**来源**: Alignment Science

**发布日期**: 2026-08

**原文**: https://alignment.anthropic.com/2026/reward-seeker

**中文摘录**：

在强化学习 (RL) 期间，AI模型完成任务并根据其结果获得奖励。他们有时会学会 “作弊”，而不是按预期完成这些任务，这种现象被称为奖励黑客。我们的行业缺乏解决这个问题的通用解决方案，而奖励黑客攻击仍然难以完全缓解。为了更好地理解奖励黑客对模型行为的影响，我们在许多容易受到奖励黑客攻击的生产环境中训练了一个具有大规模RL的 Opus 类模型。我们认为，如果我们没有在正常训练中投入大量精力来预防和检测奖励黑客行为，那么真实的训练可能会是什么样子，我们认为这是一个合理的代理。

---
