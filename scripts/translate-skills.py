#!/usr/bin/env python3
"""Translate skill titles and descriptions to Chinese."""

import re
from pathlib import Path

BLOG_DIR = Path("/Users/ocean/Documents/Ocean个人主页/ocean-blog/src/content/skills")

# Chinese translations: slug → (title_zh, description_zh)
TRANSLATIONS = {
    "agent-native-architecture": ("Agent 原生架构", "构建以 Agent 为核心的应用架构，设计自主代理、创建 MCP 工具、实现自修改系统"),
    "anndata": ("AnnData 数据分析", "单细胞分析中注释矩阵的数据结构，处理 .h5ad 文件和基因表达数据"),
    "ansible-validator": ("Ansible 验证器", "验证、审查和调试 Ansible Playbook、角色、清单和集合"),
    "astropy": ("AstroPy 天文计算", "Python 天文学和天体物理学综合库，天体坐标、光谱分析和宇宙学计算"),
    "benchling-integration": ("Benchling 集成", "Benchling 研发平台集成，访问 DNA、蛋白质注册表和实验室工作流"),
    "biopython": ("BioPython 分子生物学", "分子生物学综合工具包，序列操作、BLAST 搜索和蛋白质结构分析"),
    "cirq": ("Cirq 量子计算", "Google 量子计算框架，针对 Google 量子硬件的量子电路设计和模拟"),
    "citation-management": ("学术引文管理", "学术研究的全面引文管理，搜索 Google Scholar、PubMed 等数据库"),
    "clinical-decision-support": ("临床决策支持", "生成专业临床决策支持文档，涵盖诊断路径和治疗方案建议"),
    "clinical-reports": ("临床报告撰写", "撰写全面的临床报告，包括病例报告（CARE 指南）和系统评价"),
    "code-documenter": ("代码文档生成器", "专业的代码文档生成工具，分析代码库并自动生成文档"),
    "comfyui-gateway": ("ComfyUI 网关", "ComfyUI 服务器的 REST API 网关，工作流管理和任务队列"),
    "command-development": ("Claude Code 命令开发", "创建 Claude Code 斜杠命令的指南，涵盖结构、前置信息和动态功能"),
    "create-agent-skills": ("创建 Agent 技能", "创建 Claude Code 技能和斜杠命令的专家指导"),
    "create-hooks": ("创建 Hooks", "创建、配置和使用 Claude Code Hooks 的专家指导"),
    "create-mcp-servers": ("创建 MCP 服务器", "创建 Model Context Protocol (MCP) 服务器，暴露工具、资源和提示"),
    "create-meta-prompts": ("创建元提示", "为 Claude 管道创建优化提示，包含研究和结构化输出"),
    "create-plans": ("创建项目计划", "创建针对单人 Agent 开发优化的分层项目计划"),
    "create-subagents": ("创建子代理", "创建和使用 Claude Code 子代理的专家指导"),
    "dask": ("Dask 分布式计算", "超大规模 Pandas/NumPy 工作流的分布式计算框架"),
    "dhh-rails-style": ("DHH Rails 风格", "David Heinemeier Hansson 的 Ruby on Rails 编程风格和最佳实践"),
    "dnanexus-integration": ("DNAnexus 集成", "DNAnexus 基因组学平台集成，大规模生物信息学数据处理"),
    "dockerfile-generator": ("Dockerfile 生成器", "生成安全、高效、生产就绪的多阶段 Dockerfile"),
    "dspy-ruby": ("DSPy Ruby", "Ruby 中的 DSPy 框架实现，用于编程式 LLM 管道"),
    "etetoolkit": ("ETE Toolkit 系统发育", "Python 系统发育分析工具包，进化树构建和可视化"),
    "exploratory-data-analysis": ("探索性数据分析", "使用 Python 进行全面的探索性数据分析，统计概述和可视化"),
    "fda-database": ("FDA 数据库查询", "查询 FDA 数据库，包括药品、设备、食品召回和不良事件报告"),
    "fred-economic-data": ("FRED 经济数据", "美联储经济数据库查询，宏观经济指标和时间序列分析"),
    "geomaster": ("地理空间分析", "全面的地理空间分析和地图可视化工具"),
    "github-actions-generator": ("GitHub Actions 生成器", "生成 CI/CD 工作流配置的 GitHub Actions YAML 文件"),
    "github-actions-validator": ("GitHub Actions 验证器", "验证和优化 GitHub Actions 工作流配置"),
    "gitlab-ci-generator": ("GitLab CI 生成器", "生成 GitLab CI/CD 管道配置文件"),
    "graphql-architect": ("GraphQL 架构师", "设计和实现 GraphQL API 架构，Schema 设计和性能优化"),
    "helm-generator": ("Helm Chart 生成器", "生成 Kubernetes Helm Chart 模板和配置"),
    "helm-validator": ("Helm Chart 验证器", "验证和审查 Helm Chart 配置的正确性和安全性"),
    "imaging-data-commons": ("医学影像数据", "NCI 医学影像数据公共资源，癌症影像数据分析"),
    "iphone-apps": ("iPhone 应用开发", "iOS 应用开发全栈指南，SwiftUI、UIKit 和应用架构"),
    "jenkinsfile-validator": ("Jenkinsfile 验证器", "验证和优化 Jenkins 管道配置文件"),
    "kubernetes-specialist": ("Kubernetes 专家", "Kubernetes 集群管理、部署策略和云原生架构设计"),
    "lamindb": ("LaminDB 生物数据", "生物数据管理平台，实验数据追踪和版本控制"),
    "latex-posters": ("LaTeX 海报制作", "使用 LaTeX 创建学术会议海报和科研展示"),
    "loki-mode": ("Loki 日志系统", "Grafana Loki 日志聚合系统配置和查询优化"),
    "macos-apps": ("macOS 应用开发", "macOS 原生应用开发，SwiftUI、AppKit 和系统集成"),
    "market-research-reports": ("市场研究报告", "生成全面的市场研究报告，行业分析和竞争格局评估"),
    "matlab": ("MATLAB 科学计算", "MATLAB 科学计算和工程仿真，信号处理和数值分析"),
    "microservices-architect": ("微服务架构师", "设计和实现微服务架构，服务拆分、通信和部署策略"),
    "ml-pipeline": ("机器学习管道", "构建端到端机器学习管道，数据处理、模型训练和部署"),
    "modal": ("Modal 云计算", "Modal 无服务器云平台，GPU 计算和分布式任务执行"),
    "networkx": ("NetworkX 网络分析", "Python 网络分析库，图论算法和复杂网络可视化"),
    "neurokit2": ("NeuroKit2 神经信号", "神经生理信号处理工具包，ECG、EEG 和 EMG 分析"),
    "neuropixels-analysis": ("Neuropixels 分析", "Neuropixels 神经探针数据分析，高密度电生理记录处理"),
    "omero-integration": ("OMERO 生物影像", "OMERO 生物影像平台集成，显微镜图像管理和分析"),
    "pandas-pro": ("Pandas 高级用法", "Pandas 高级数据处理技巧，性能优化和大数据集处理"),
    "pathml": ("PathML 病理分析", "计算病理学机器学习工具包，组织切片图像分析"),
    "pennylane": ("PennyLane 量子ML", "量子机器学习框架，量子电路和经典神经网络混合计算"),
    "plugin-structure": ("Claude Code 插件结构", "Claude Code 插件的标准化目录结构和开发规范"),
    "polars": ("Polars 高性能数据", "Rust 驱动的高性能数据框架，比 Pandas 快 10-100 倍"),
    "prompt-engineer": ("提示工程", "LLM 提示词工程最佳实践，优化提示设计和输出质量"),
    "promql-generator": ("PromQL 生成器", "生成 Prometheus 查询语言表达式，监控指标查询和告警规则"),
    "pufferlib": ("PufferLib 强化学习", "高效强化学习库，大规模并行环境训练和评估"),
    "pyhealth": ("PyHealth 医疗AI", "医疗健康数据的深度学习工具包，电子健康记录分析"),
    "pylabrobot": ("PyLabRobot 实验室", "实验室自动化机器人控制库，液体处理和实验流程自动化"),
    "pymatgen": ("Pymatgen 材料科学", "Python 材料基因组学库，晶体结构分析和材料性质计算"),
    "pyopenms": ("PyOpenMS 质谱分析", "质谱数据处理和蛋白质组学分析工具包"),
    "pytorch-lightning": ("PyTorch Lightning", "PyTorch 高级训练框架，简化深度学习模型训练和部署"),
    "qiskit": ("Qiskit 量子计算", "IBM 量子计算 SDK，量子电路设计、模拟和真机执行"),
    "qutip": ("QuTiP 量子模拟", "开放量子系统动力学模拟工具包，量子光学和量子信息"),
    "rag-architect": ("RAG 架构师", "检索增强生成系统架构设计，向量数据库和语义检索优化"),
    "rdkit": ("RDKit 化学信息学", "化学信息学工具包，分子操作、相似性搜索和药物设计"),
    "react-native-best-practices": ("React Native 最佳实践", "React Native 移动应用开发最佳实践，性能优化和跨平台策略"),
    "render-deploy": ("Render 部署", "Render 云平台部署配置，Web 服务和数据库托管"),
    "research-grants": ("科研基金申请", "科研基金申请撰写指导，研究计划书和预算编制"),
    "rowan": ("Rowan 化学计算", "Python 计算化学库，量子化学计算和分子模拟"),
    "salesforce-developer": ("Salesforce 开发", "Salesforce 平台开发，Apex 编程和 Lightning 组件构建"),
    "sanity-best-practices": ("Sanity CMS 最佳实践", "Sanity 内容管理系统最佳实践，Schema 设计和 GROQ 查询"),
    "scientific-slides": ("科研演示文稿", "使用 LaTeX Beamer 创建专业科研演示文稿和学术报告"),
    "scientific-writing": ("科研写作", "科研论文和学术文档写作指导，符合期刊投稿规范"),
    "scikit-learn": ("Scikit-learn 机器学习", "Python 经典机器学习库，分类、回归、聚类和降维算法"),
    "scvi-tools": ("scvi-tools 单细胞", "单细胞组学深度学习工具包，变分推断和数据集成"),
    "seaborn": ("Seaborn 数据可视化", "Python 统计数据可视化库，美观的统计图表和探索性分析"),
    "security-best-practices": ("安全最佳实践", "软件安全最佳实践，漏洞防御、认证授权和安全编码"),
    "sentry-dotnet-sdk": ("Sentry .NET SDK", "Sentry 错误监控 .NET SDK 集成，异常追踪和性能监控"),
    "sentry-nextjs-sdk": ("Sentry Next.js SDK", "Sentry 错误监控 Next.js SDK 集成，服务端和客户端错误追踪"),
    "sentry-react-native-sdk": ("Sentry React Native SDK", "Sentry 错误监控 React Native SDK 集成，移动端崩溃追踪"),
    "sentry-react-sdk": ("Sentry React SDK", "Sentry 错误监控 React SDK 集成，前端异常和性能监控"),
    "sharp-edges": ("Sharp 边缘处理", "Node.js 高性能图像处理库 Sharp 的高级用法和优化"),
    "shopify-expert": ("Shopify 开发专家", "Shopify 电商平台开发，主题定制、App 开发和 Liquid 模板"),
    "spark-engineer": ("Spark 工程师", "Apache Spark 大数据处理，分布式计算和数据管道优化"),
    "statsmodels": ("Statsmodels 统计建模", "Python 统计建模库，回归分析、时间序列和假设检验"),
    "sympy": ("SymPy 符号计算", "Python 符号数学库，代数运算、微积分和方程求解"),
    "terraform-generator": ("Terraform 生成器", "生成 Terraform 基础设施代码，云资源配置和模块化设计"),
    "terraform-validator": ("Terraform 验证器", "验证和审查 Terraform 配置的安全性、合规性和最佳实践"),
    "transformers": ("Transformers 深度学习", "Hugging Face Transformers 库，预训练模型微调和推理部署"),
    "treatment-plans": ("治疗方案设计", "制定循证医学治疗方案，个体化治疗计划和随访策略"),
    "ui-styling": ("UI 样式设计", "用户界面样式设计系统，组件库、设计令牌和响应式布局"),
    "vaex": ("Vaex 大规模数据", "处理十亿级数据行的惰性计算数据框架，内存映射和流式处理"),
    "venue-templates": ("场地模板设计", "活动场地布局设计模板，会议、展览和演出场地规划"),
    "vue-expert": ("Vue.js 专家", "Vue.js 框架高级开发，组合式 API、状态管理和性能优化"),
    "whatsapp-cloud-api": ("WhatsApp Cloud API", "WhatsApp 商业 API 集成，消息发送、模板管理和 Webhook"),
    "wordpress-pro": ("WordPress 专业开发", "WordPress 高级开发，主题和插件开发、性能优化和安全加固"),
}

updated = 0
for md_file in sorted(BLOG_DIR.glob("*.md")):
    slug = md_file.stem
    if slug not in TRANSLATIONS:
        print(f"SKIP (no translation): {slug}")
        continue

    title_zh, desc_zh = TRANSLATIONS[slug]
    content = md_file.read_text(errors="replace")

    # Replace title
    content = re.sub(
        r'^title: ".*?"',
        f'title: "{title_zh}"',
        content,
        count=1,
        flags=re.MULTILINE
    )

    # Replace description
    content = re.sub(
        r'^description: ".*?"',
        f'description: "{desc_zh}"',
        content,
        count=1,
        flags=re.MULTILINE
    )

    md_file.write_text(content)
    updated += 1

print(f"\nUpdated: {updated} / 100")
