# 云课本 Cursor / Codex 提示词

把下面整段复制进 Cursor Agent / Codex。一次只用一条。  
仓库约定：前端在 `web/`，脚本在 `scripts/`，不提交任何 PDF。  
源仓：`https://github.com/TapXWorld/ChinaTextbook`。

---

## 提示词 A · 生成 catalog

```
你在仓库 yun-keben 里工作。目标：写 scripts/build_catalog.py，从 GitHub API 生成 web/catalog.json。

要求：
1. 请求 GET https://api.github.com/repos/TapXWorld/ChinaTextbook/git/trees/master?recursive=1
2. Header 带 User-Agent；若环境变量 GITHUB_TOKEN 存在则带 Authorization: Bearer
3. 只收 type=blob 且文件名匹配 /\.pdf(\.\d+)?$/i 的节点
4. 把 书.pdf.1、书.pdf.2 合并为一条教材：
   - path / name 用「书.pdf」
   - split=true
   - parts 为分片路径数组，按数字排序
   - size 为各分片 size 之和
5. 从路径解析 stage/subject/edition；第一段以「学数学」开头则 stage=习题
6. 输出 JSON：source, branch, generatedAt(ISO), count, stages, books[]
7. books 字段：id, name(去.pdf), file, path, stage, subject, edition, size, split, parts
8. 按 stage 自定义顺序 + subject + edition + name 排序
9. truncated=true 时打印警告
10. 用标准库，不要第三方依赖
11. 写 scripts/README.md 说明用法：python3 scripts/build_catalog.py

不要下载任何 PDF。写完后说明如何运行。
```

---

## 提示词 B · 静态云课本前端

```
在 yun-keben 实现可部署静态站，目录 web/。

文件：web/config.js、web/index.html。catalog.json 不存在时显示演示数据并提示先跑 build_catalog.py。

config.js 必须包含 title/subtitle/storage(github|jsdelivr|cos)/cosBase/github/official/sourceRepo。

功能：学段与科目 chip、搜索、卡片、阅读（PDF.js viewer.html?file=）、GitHub 链接。
cos 模式用合并后 path。split=true 且非 cos 时禁用阅读。
页脚版权。米纸风、移动端优先、零构建、中文。
```

---

## 提示词 C · 合并分片并同步 COS

```
在 yun-keben/scripts 增加 merge_pdfs.py 与 sync_to_cos.sh。
merge：按 *.pdf.<数字> 分组拼接；目标已存在且体积够则跳过；--delete-parts 可删分片；仅标准库。
sync：sparse clone → merge → rclone copy 示例；环境变量 REPO_URL WORKDIR COS_REMOTE SPARSE_PATH；不写密钥。
scripts/README.md 补充 CORS、Range、防盗链、不要在 1C1G 上全量 clone。
```

---

## 提示词 D · 阅读体验

```
在现有 web/index.html 上增强：localStorage 进度与最近阅读、分页/加载更多、iframe 失败提示改 cos。不要推翻重写，保持零依赖。
```

---

## 提示词 E · 部署

```
写 docs/DEPLOY.md：站点域名与文件 CDN 分开、Caddyfile、COS 静态站、CORS、防盗链（微信内置浏览器空 Referer）、备案与故障表。中文。
```

---

## 提示词 F · 第一期缩围

```
build_catalog.py 增加 --stage --edition-substr。默认只留小学/初中主科 + 人教/统编。README 写清全量 42GB vs 第一期数 GB。
```

---

## Agent 总约束（User Rules）

```
- 不把 PDF 或任何 >5MB 二进制提交进 git
- 不在代码里写 COS SecretId/SecretKey
- 所有对外页面必须有版权声明和 official 链接
- 中文 UI，移动端可用
- 先跑通小学数学人教版一本未拆分 PDF，再扩范围
```
