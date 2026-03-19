# Ocean's Blog

Ocean 的个人博客网站。找到一个最长的雪坡，滚雪球。

## 关于

这是一个基于 Astro 构建的静态博客，设计风格追求温暖、克制、编辑感 — 让排版和内容本身成为设计。

**在线访问**：待部署

## 内容分类

- **Perp DEX** — 永续合约与 DEX 相关研究
- **预测市场** — 预测市场平台与机制分析
- **产品与增长** — 电商运营、产品策略和商业思考
- **Web3 综合** — 区块链生态、项目分析和行业观察
- **AI 探索** — AI 工具、Vibe Coding 和技术实践
- **故事集** — 对话、人物和校园故事
- **旅居和探索** — 东南亚旅居、城市观察和文化随笔
- **个人思考** — 职业、成长、阅读和生活感悟

## 技术栈

| 技术 | 用途 |
|------|------|
| [Astro](https://astro.build) 6 | 静态站点框架 |
| [Tailwind CSS](https://tailwindcss.com) 4 | 样式系统 |
| MDX | 文章内容格式 |
| [Shiki](https://shiki.matsu.io) | 代码语法高亮 |
| RSS | 内容订阅 |

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

开发服务器默认运行在 `http://localhost:4321`

## 项目结构

```
src/
├── components/     # 组件 (导航栏、侧边栏、卡片、Footer)
├── content/
│   ├── posts/      # 博客文章 (.md)
│   └── projects/   # 代码库项目数据
├── i18n/           # 国际化翻译文件
├── layouts/        # 页面布局模板
├── pages/          # 路由页面
└── styles/         # 全局样式和设计系统
```

## 写文章

在 `src/content/posts/` 下创建 `.md` 文件：

```markdown
---
title: "文章标题"
description: "文章描述"
category: "web3"
date: 2026-03-19
---

正文内容...
```

可用分类：`perp-dex` / `prediction-market` / `product-growth` / `web3` / `ai` / `stories` / `travel` / `reflections`

## 部署

项目配置为部署到 Vercel（静态 SSG 模式）。连接 GitHub 仓库后自动部署。

## 作者

**Ocean 倪钰桐**

- 𝕏：[@Ocean_Jackon](https://x.com/Ocean_Jackon)
- GitHub：[Oceanjackson1](https://github.com/Oceanjackson1)
