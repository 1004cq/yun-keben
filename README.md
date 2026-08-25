# 云课本

把 [TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook) 做成可检索、可在线阅读的静态站。

本仓库只放 **网站、目录脚本、方案**，不放 PDF。

[源教材仓](https://github.com/TapXWorld/ChinaTextbook) · [智慧教育平台](https://basic.smartedu.cn/tchMaterial) · [本仓](https://github.com/1004cq/yun-keben)

## 原则

**目录是网站，文件是对象存储。禁止 clone 42GB 源仓到网站机。**

Trees API → catalog → 合并 PDF → COS/CDN → PDF.js。

## 选型

| 项 | 第一期 | 以后 |
|---|---|---|
| 语言 | JavaScript | TypeScript |
| UI | 无框架 | Vue 3 + Vite |
| 阅读 | PDF.js | PDF.js |
| Agent | frontend-design → impeccable → 本仓动效规则 → Karpathy | 见 [docs/SKILLS.md](docs/SKILLS.md) |

不用 ui-ux-pro-max、不装 react-bits。

## 本地

```bash
git clone https://github.com/1004cq/yun-keben.git
cd yun-keben
GITHUB_TOKEN=ghp_xxx python3 scripts/build_catalog.py
python3 -m http.server -d web 8080
```

## 部署

Settings → Pages → GitHub Actions · `https://1004cq.github.io/yun-keben/`

[docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md)

## 文档

- [docs/SKILLS.md](docs/SKILLS.md) skill 与 token
- [docs/STACK.md](docs/STACK.md) 语言框架
- [docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md)
- [docs/PROMPTS.md](docs/PROMPTS.md)
- [scripts/README.md](scripts/README.md)
