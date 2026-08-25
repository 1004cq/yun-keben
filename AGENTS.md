# AGENTS.md

给 Codex / Cursor 的项目说明书。打开本仓库后先读这些文件再改代码。

## 仓库

- GitHub：https://github.com/1004cq/yun-keben
- 产品：云课本（静态站）。目录在 `web/`，文档在 `docs/`。
- 第一期：零构建。可改 `web/index.html`、`web/config.js`、`web/catalog.json`。不要为动效引入 React / Vue / Aceternity / React Bits。

## 必读文档（按这个顺序）

1. `README.md` — 目标与部署
2. `docs/SKILLS.md` — 设计系统、组件谱、动效预算
3. `docs/STACK.md` — 语言与框架决策
4. `docs/PROMPTS.md`、`docs/PROMPTS_SWIPE.md` — 分阶段提示词
5. `docs/GITHUB_ACTIONS.md` — Pages / COS 工作流

需求已写在上述 md 里。用户只说「按仓库做」时，按这些文件实现，不要另起视觉。

## 设计锁

- 纸色 token：`--bg #f4f1ea`、`--paper #fffdf8`、`--ink #1c1915`、`--accent #c45c26`
- 字体：Noto Sans SC
- 触控目标 ≥ 44px；尊重 `prefers-reduced-motion`
- 选书：大封面 + 底部横滑海报条；年级在学段和科目之间
- 进入阅读：CSS 3D 翻书后打开 PDF.js

## 验证

```bash
python3 -m http.server -d web 8080
```
