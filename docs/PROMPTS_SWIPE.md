# 滑动选书提示词

对标短视频：上半大封面，下半横滑海报条；点小封面切换，再点进入 PDF。
一次一条，只改 `web/index.html`，不上 React / Aceternity / React Bits。

## 1. 结构

```
按「蜚蛙侠主题站」选片交互改 web/index.html，视觉仍用 docs/SKILLS.md 纸色 token。
上 58%：当前课本大封面 + 书名 + 「阅读」
下 42%：横向海报条，scroll-snap，一屏 4～5 本，两侧露出半本
点海报设为当前本；再点同一本或点「阅读」打开 PDF.js
原生 HTML/CSS/JS。禁止 npm 与粒子。
```

## 2. 手感

```
海报宽约 22vw，最小 92px，高 3/4.2
scroll-snap-align: center；左右 padding 半屏
当前 scale(1)，其余 scale(.88) opacity .7，180ms
滚动结束用中线 nearest 更新大封面
左右方向键切本；prefers-reduced-motion 时取消 scale
```

## 3. 封面

```
没有电影海报，用书脊假封面。禁止外链图。
科目色循环 #6b3a22 #2f4a3c #3a3f63 #5a3d2b #1f4a5a #4a2f3e
大封面与小海报同一个绘制函数。
```

## 4. 验收

```
1 手指能甩动海报条，停下来有一本对准
2 对准的本同步到上方大封面
3 点击进入阅读器，不新开标签
4 筛选后轨道回第一本
5 手机竖屏不出现整页横滚
```
