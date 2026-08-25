# Agent Skill 流水线

云课本只用三条外部 skill + 一份本仓规则。不再用 ui-ux-pro-max（模板太全，容易漂成仪表盘）和 react-bits（React 展示库）。

| 顺序 | 用什么 | 负责 |
|---|---|---|
| 1 | **Anthropic frontend-design** | 定审美：纸、墨、一枚暖色；禁止 Inter / 紫渐变 |
| 2 | **impeccable** | 打磨层级、对齐、留白、触控面；不改 token |
| 3 | **本仓 docs/SKILLS.md 动效节** | 180ms fade / 上移；不装任何动效库 |
| 4 | **Karpathy minimalism** | 少依赖、小函数、错误可执行 |
| 门禁 | **web-design-guidelines**（可选） | 发布前查对比度、焦点、移动端；不参与造型 |

一次只跑一条。四条塞进同一条 prompt 会互相抢。

---

## Token（已锁死，skill 不得改色）

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
  --motion: 180ms ease;
}
```

组件谱：顶栏、搜索、chip、书卡、空状态、阅读器遮罩、页脚声明。
移动优先，触控 ≥ 44px。

禁止：仪表盘侧栏、营销落地页、玻璃拟态、粒子背景、第二套主色、第二套字体、shadcn / Tailwind / GSAP / react-bits 整包。

---

## 1. frontend-design

官方底线：https://github.com/anthropics/skills（`frontend-design`）

任务：在上述 token 内做出「教育阅读工具」的层次和排版，不要重新选品类风格。
输出前自查：是否又写成 Inter / 蓝紫渐变 / 三列 feature。

## 2. impeccable

在 token 已落地后用。

- polish：字号阶梯、行高 1.45–1.7、内边距统一
- quieter：减阴影、减边框、同屏只留一个强调
- distill：一卡 = 科目 + 书名 + 体积 + 两个按钮
- audit：对比度、焦点环、横屏、微信内置浏览器

## 3. 动效（本仓规则，不装库）

```css
@media (prefers-reduced-motion: no-preference) {
  .card { animation: rise var(--motion) both; }
}
@keyframes rise {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: none; }
}
```

阅读器遮罩只做 opacity。禁止：>300ms、无限循环、3D、粒子、文字打散。

## 4. Karpathy

| 区 | 允许 | 禁止 |
|---|---|---|
| scripts/ | Python 标准库 | requests、pandas |
| web/ 第一期 | 零构建 | Vue/React/Tailwind（第二期才 Vue） |
| 阅读 | PDF.js CDN | 再包一层 viewer |

能 20 行写清就不装包。错误要写下一步：`API 403，加 GITHUB_TOKEN`。

## 5. 可选门禁

Vercel `web-design-guidelines` 只在发布前跑一次，出检查清单，不连带改版式。

---

## Cursor 口令

```
只用 frontend-design。token 已在 docs/SKILLS.md 锁死。把 :root 落到 web/index.html，不要新建组件，不要换色。
```

```
只用 impeccable。quieter + distill 书卡和顶栏。不改色板，不加依赖。
```

```
按 docs/SKILLS.md 动效节，给卡片加 180ms rise，给阅读器加 fade。不装库。
```

```
只用 Karpathy minimalism。审计 web/ 与 scripts/，删掉多余代码和任何新依赖。
```
