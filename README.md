# 云课本 yun-keben

把 [TapXWorld/ChinaTextbook](https://github.com/TapXWorld/ChinaTextbook) 做成可检索、可在线翻页的云课本网站。

本仓库放的是 **方案、目录规范、同步流程、Cursor 提示词**，不存放 40GB+ PDF。PDF 放腾讯云 COS（或任意对象存储），网站只托管 `catalog.json` + 前端。

- 源教材仓库：https://github.com/TapXWorld/ChinaTextbook（约 8 万 Star，体积约 42GB）
- 官方正版入口：[国家中小学智慧教育平台](https://basic.smartedu.cn/tchMaterial)
- 本仓库：https://github.com/1004cq/yun-keben

---

## 0. 一句话原则

**目录是网站，文件是对象存储。禁止 `git clone` 整库到网站服务器。**

GitHub Raw / jsDelivr 只允许本地调试。上线必须：

1. 用 GitHub Trees API 生成 `catalog.json`（几百 KB）
2. 按需拉取 PDF，合并被拆开的 `.pdf.1` / `.pdf.2`
3. 上传 COS + CDN
4. 前端用 PDF.js 阅读，URL 指向 CDN

---

## 1. 目标产品

个人/小范围使用的「云课本」：

| 能力 | 说明 |
|---|---|
| 浏览 | 学段 → 科目 → 版本 → 册次 |
| 搜索 | 书名、年级、人教版、高数等 |
| 阅读 | PDF.js 翻页、缩放、记住页码 |
| 下载 | 可选，建议登录或 Referer 校验后再给直链 |
| 同步 | 脚本从源仓增量更新 catalog 与对象存储 |

不做：收费卖教材、全网网盘、无版权声明的公开镜像。

建议第一期只上 **小学 + 初中 · 人教/统编**，跑通阅读和 COS 后再扩高中、大学。

---

## 2. 架构

```
TapXWorld/ChinaTextbook
        |
        |- scripts/build_catalog.py
        |         ↓
        |    web/catalog.json          ← 静态站一起部署
        |         ↓
        |    纯静态前端
        |         ↓ PDF.js
        |    用户浏览器
        |
        └大硬盘机器 sparse checkout
                  ↓ 合并拆分 PDF
                  ↓ rclone / coscli
             腾讯云 COS
                  ↓ CDN / EdgeOne
             https://cdn.example.com/ChinaTextbook/...
```

### 为什么不能直链 GitHub

- 国内访问不稳定、限流
- 单文件常 20–50MB，部分超过 50MB 被切成多片
- PDF.js 需要 HTTP Range；GitHub Raw 对大文件不友好
- 流量打到别人仓库不礼貌，也容易被封

### 推荐存储

腾讯云 COS + 自定义域名 + CDN（或 EdgeOne）。

- 存储 42GB 费用很低
- 贵的是公网流量 → 必须防盗链
- 可复用已有 COS 桶，前缀用 `ChinaTextbook/`

---

## 3. 目录与数据规范

源仓顶层大致为：小学 / 小学（五•四学制） / 初中 / 初中（五•四学制） / 高中 / 大学 / 习题目录。

例如：

```
小学/数学/人教版/义务教育教科书 · 数学一年级上册.pdf
小学/数学/北师大版/义务教育教科书·数学二年级上册.pdf.1
小学/数学/北师大版/义务教育教科书·数学二年级上册.pdf.2
```

`catalog.json`：

```json
{
  "source": "TapXWorld/ChinaTextbook",
  "branch": "master",
  "generatedAt": "2026-08-25T00:00:00Z",
  "count": 1234,
  "books": [
    {
      "id": "小学/数学/人教版/义务教育教科书 · 数学一年级上册.pdf",
      "name": "义务教育教科书 · 数学一年级上册",
      "path": "小学/数学/人教版/义务教育教科书 · 数学一年级上册.pdf",
      "stage": "小学",
      "subject": "数学",
      "edition": "人教版",
      "size": 50154321,
      "split": false,
      "parts": []
    }
  ]
}
```

规则：`.pdf.1` + `.pdf.2` 合并成一条；COS 对象 key 用合并后的 path；前端只读完整 PDF。

---

## 4. 实施阶段

### P0 能打开

1. `build_catalog.py` 调 GitHub Trees API
2. 静态首页：学段 chip + 搜索 + 卡片
3. PDF.js 阅读（可先指 GitHub Raw 验证 UI）
4. 页脚版权 + 官方平台链接

### P1 能在国内读

1. 大硬盘机 sparse checkout `小学/数学`
2. 合并拆分文件
3. 上传 COS，`storage: "cos"`
4. CDN Range、缓存 PDF
5. Referer 防盗链

### P2 好用

阅读进度、最近阅读、六三/五四制、手机全屏、按 tree sha 增量同步。

### P3 可选

下架开关、访问热度、登录后下载、跳转官方 contentId。

---

## 5. 同步与合并

```bash
git clone --filter=blob:none --sparse https://github.com/TapXWorld/ChinaTextbook.git
cd ChinaTextbook
git sparse-checkout set "小学/数学"
cat "书名.pdf.1" "书名.pdf.2" > "书名.pdf"
rclone copy ./  cos:你的桶/ChinaTextbook --exclude "*.pdf.[0-9]" --exclude ".git/**" --progress
```

Windows 合并工具：https://github.com/TapXWorld/ChinaTextbook-tools

国内从官方重下可用 [tchMaterial-parser](https://github.com/happycola233/tchMaterial-parser)。

---

## 6. 前端要点

- 移动端优先
- COS CORS 允许站点 Origin，支持 Range
- PDF.js：`viewer.html?file=` + encodeURIComponent(cdnUrl)
- 拆分未合并的书禁用「阅读」
- 配置见 `web/config.js`

---

## 7. 合规（必读）

1. 版权在出版社。源仓是第三方整理，不是教育部官方仓。
2. 个人学习站风险低于公开全量镜像站。
3. 不要收费卖 PDF，不要加私人水印再分发。
4. 国内域名对公网需 ICP。
5. 页脚声明 + 官方链接；投诉即下架。

---

## 8. 费用

全库约 42GB；存储便宜，流量贵，必须防盗链。第一期只同步小学数学即可验证。

---

## 9. 文件树

```
yun-keben/
  README.md
  docs/PROMPTS.md
  web/index.html
  web/config.js
  scripts/build_catalog.py
  scripts/sync_to_cos.sh
```

不要把 PDF 提交进 Git。

---

## 10. Cursor 提示词

完整可复制版本见 [docs/PROMPTS.md](docs/PROMPTS.md)。

顺序：A catalog → B 前端 → C 合并同步 → D 阅读体验 → E 部署 → F 收窄第一期。
一次只贴一条。
