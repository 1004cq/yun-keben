# Agent Skill 流水线

云课本按 **四条 skill 分工**，一次只跑一条。

| 顺序 | Skill | 负责 | 不负责 |
|---|---|---|---|
| 1 | **ui-ux-pro-max** | 定设计系统：风格、色板、字体、间距、组件谱 | 不打磨像素、不加花活 |
| 2 | **impeccable** | 按已定系统打磨质感：层级、对比、留白、去 slop | 不改品牌方向、不新加依赖 |
| 3 | **react-bits** | 动效预算：过渡、列表入场、阅读器 fade | 不装整库；第一期用 CSS |
| 4 | **Karpathy** | 规范精简：少依赖、小函数、CLI 清楚 | 不借精简毁掉设计系统 |

顺序：定系统 → 打磨 → 动效 → 删肥。

## 1. ui-ux-pro-max

方向：教育阅读工具，editorial paper（纸、墨、一枚暖强调色）。
禁止：Inter+紫渐变、玻璃拟态、仪表盘侧栏、营销落地页。

```css
:root {
  --bg: #f4f1ea;
  --paper: #fffdf8;
  --ink: #1c1915;
  --muted: #6b6458;
  --line: #e6dfd2;
  --accent: #c45c26;
  --accent-soft: #f3e0d2;
  --ok: #2f6b4f;
  --space-1: 8px;
  --space-2: 12px;
  --space-3: 16px;
  --space-4: 24px;
  --radius-card: 16px;
  --radius-pill: 999px;
  --font: "Noto Sans SC", system-ui, sans-serif;
}
```

组件谱：顶栏、搜索、chip、书卡、空状态、阅读器遮罩、页脚声明。移动优先，触控 ≥ 44px。

## 2. impeccable

polish / quieter / distill / audit。
质感来自层级、对齐、留白、一种强调色。不加第二套字体或 UI 库。

## 3. react-bits

第一期无 React：偷原则不装包。
允许 150–220ms 的 opacity + translateY(8px)、遮罩 fade。
禁止粒子、3D 翻书、GSAP、整份组件库、超 300ms 或无限循环。

## 4. Karpathy

`scripts/` 只标准库；`web/` 第一期无 npm。
小函数、错误信息可执行、config 有注释。能 yoink 十行就不装包。

## Cursor

一次只贴一段：「只启用 ui-ux-pro-max，落 token」→ impeccable 打磨 → react-bits 动效预算 → Karpathy 审计删肥。
