# 云课本

把 [TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook) 做成可检索、可在线阅读的静态站。

本仓库只放 **网站、目录脚本、方案和提示词**，不放 PDF。教材文件在对象存储里。

[源教材仓](https://github.com/TapXWorld/ChinaTextbook) · [智慧教育平台（官方）](https://basic.smartedu.cn/tchMaterial) · [本仓](https://github.com/1004cq/yun-keben)

## 原则

**目录是网站，文件是对象存储。禁止把 42GB 源仓 clone 到网站机或打进 Git。**

上线路径：Trees API → catalog → 合并 PDF → COS/CDN → PDF.js。

## 当前选型

| 项 | 第一期 | 以后可以 |
|---|---|---|
| 语言 | JavaScript | TypeScript |
| UI | 无框架 | Vue 3 + Vite |
| 阅读 | PDF.js | PDF.js |
| Agent | [docs/SKILLS.md](docs/SKILLS.md) 四条流水线 | 同左 |

UI 工作顺序：ui-ux-pro-max 定系统 → impeccable 打磨 → react-bits 动效预算 → Karpathy 精简代码。

## 本地

```bash
git clone https://github.com/1004cq/yun-keben.git
cd yun-keben
GITHUB_TOKEN=ghp_xxx python3 scripts/build_catalog.py
python3 -m http.server -d web 8080
```

## 部署

Settings → Pages → GitHub Actions。地址：`https://1004cq.github.io/yun-keben/`
详见 [docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md)。

## 文档

- [docs/SKILLS.md](docs/SKILLS.md) 设计系统 / 质感 / 动效 / 精简
- [docs/STACK.md](docs/STACK.md) 语言和框架
- [docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md) Actions
- [docs/PROMPTS.md](docs/PROMPTS.md) Cursor 提示词
- [scripts/README.md](scripts/README.md) 命令
