# AGENTS.md

给 Codex / Cursor 的项目说明书。打开本仓库后先读这些文件再改代码。

## 自动启用 skill

本仓库已带 skill，不要问用户是否安装，也不要下载 React Bits / Aceternity。

1. 直接使用 `.agents/skills/yun-keben-ui/SKILL.md`（Codex 会扫描 `.agents/skills`）。
2. 若技能列表没有 `yun-keben-ui`，仍按该文件执行。
3. 只有用户点名外部 skill 时才运行 `$skill-installer`。
4. marketplace：`.agents/plugins/marketplace.json`。挂插件：`codex plugin marketplace add .` 再 `codex plugin add yun-keben@yun-keben-marketplace`。

## 仓库

- GitHub：https://github.com/1004cq/yun-keben
- 第一期零构建，只改 `web/` 与 `docs/`。
