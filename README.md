# 云课本

把 [TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook) 做成可检索、可在线阅读的静态站。

本仓库只放 **网站、目录脚本、方案和提示词**，不放 PDF。教材文件在对象存储里。

[源教材仓](https://github.com/TapXWorld/ChinaTextbook) · [智慧教育平台（官方）](https://basic.smartedu.cn/tchMaterial) · [本仓](https://github.com/1004cq/yun-keben)

## 原则

**目录是网站，文件是对象存储。禁止把 42GB 源仓 clone 到网站机或打进 Git。**

上线路径：

1. GitHub Trees API → `web/catalog.json`
2. 按需拉取 PDF，合并 `.pdf.1` / `.pdf.2`
3. 上传 COS + CDN（开 Range、防盗链）
4. 浏览器用 PDF.js 读 CDN 地址

GitHub Raw / jsDelivr 只给本地调试。

## 当前选型

| 项 | 第一期 | 以后可以 |
|---|---|---|
| 语言 | JavaScript | TypeScript |
| UI | 无框架，`web/index.html` | Vue 3 + Vite |
| 阅读 | PDF.js | 仍用 PDF.js |
| 托管 | GitHub Pages 演示 + COS 国内 | 同左 |
| CI | Actions 发 `web/` 或 `dist/` | 构建命令改一行即可 |

第一期不用 Vue / 不用 TS。列表和进度变乱后再上 Vue 3 + Vite（不要 Nuxt、不要 React）。

## 仓库结构

```
yun-keben/
  web/                    静态前端（Pages 发布这个目录）
    index.html
    config.js
    catalog.json          Actions 构建时生成，不要手改
  scripts/
    build_catalog.py      只拉文件树，不下载 PDF
  .github/workflows/
    deploy-pages.yml      自动发 GitHub Pages
    deploy-cos.yml        手动发 COS
  docs/
    GITHUB_ACTIONS.md
    PROMPTS.md
    STACK.md
```

## 本地

```bash
git clone https://github.com/1004cq/yun-keben.git
cd yun-keben
GITHUB_TOKEN=ghp_xxx python3 scripts/build_catalog.py
python3 -m http.server -d web 8080
```

存储开关在 `web/config.js`：`github` | `jsdelivr` | `cos`。

## 自动部署

1. Settings → Pages → Source 选 GitHub Actions
2. Actions 里跑 Deploy Pages
3. 地址一般为 `https://1004cq.github.io/yun-keben/`
4. 资源用相对路径 `./config.js`

国内站再用 Deploy COS（先配 Secrets）。教程见 [docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md)。不要用 Actions 同步 42GB PDF。

## 产品范围

做：浏览、搜索、翻页、第一期小学+初中人教/统编。  
不做：卖教材、当网盘、无声明的全量镜像。

阶段：P0 能打开 → P1 国内能读 → P2 进度 → P3 下架/登录下载。

## 数据与同步

分片 `.pdf.1` / `.pdf.2` 在 catalog 里合成一条。COS 只放合并后的完整文件。

```bash
git clone --filter=blob:none --sparse https://github.com/TapXWorld/ChinaTextbook.git
cd ChinaTextbook && git sparse-checkout set "小学/数学"
cat "书.pdf.1" "书.pdf.2" > "书.pdf"
rclone copy ./ cos:桶名/ChinaTextbook --exclude "*.pdf.[0-9]" --exclude ".git/**"
```

大硬盘机操作，不要用 1C1G。Windows 合并：[ChinaTextbook-tools](https://github.com/TapXWorld/ChinaTextbook-tools)

## 合规

版权在出版社。源仓不是教育部官方库。不要卖 PDF。国内对公网要 ICP。页脚留官方链接，投诉即下架。全库约 42GB，流量贵，必须防盗链。

## 文档

- [docs/README.md](docs/README.md) 索引
- [docs/STACK.md](docs/STACK.md) 语言和框架
- [docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md) 自动部署
- [docs/PROMPTS.md](docs/PROMPTS.md) Cursor 提示词 A–F（一次一条）
- [scripts/README.md](scripts/README.md) 命令
