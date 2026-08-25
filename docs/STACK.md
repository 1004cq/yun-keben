# 前端选型

## 现在

- 语言：**JavaScript**（浏览器直接跑）
- 框架：**不用**
- 阅读器：**PDF.js**
- 构建：**无**，Actions 发布 `web/`

TypeScript 是带类型的 JS，浏览器不认 `.ts`，要先编译。第一期一个页面，上 TS 只会多一道 Vite。

## 下一步（可选）

列表、进度、路由开始乱时：

- **Vue 3 + Vite + Vue Router**
- 不要 Nuxt / React / 重型组件库 / Pinia

Actions 改为：

```yaml
- run: npm ci && npm run build
- uses: actions/upload-pages-artifact@v3
  with:
    path: dist
```

资源继续用相对路径，适配 `https://用户名.github.io/yun-keben/`。

## 不是前端能解决的

PDF 走 COS、拆分文件先合并、防盗链、版权声明。换框架解决不了这些。
