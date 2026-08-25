# 学习 GitHub Actions：把云课本自动部署上线

面向 `yun-keben` 的实战教程。读完应能看懂 workflow，并自己改触发条件、密钥和发布目标。

官方：[Actions](https://docs.github.com/actions) · [Pages + Actions](https://docs.github.com/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

---

## 1. 它是什么

GitHub Actions = 仓库里的 CI/CD 机器人。YAML 放进 `.github/workflows/`，GitHub 在虚拟机上拉代码、跑脚本、发布结果。

云课本适合自动化：生成 `catalog.json`、发布 `web/` 到 Pages、同步 `web/` 到 COS。

**不要** 用 Actions clone 42GB 教材或上传全部 PDF。

---

## 2. 三个名词

- **Workflow**：一个 `.yml`
- **Job**：一台虚拟机上的一组步骤，可用 `needs:` 串联
- **Step**：`uses:` 用现成 Action，`run:` 自己写 shell

---

## 3. 最小 YAML

见本仓 `.github/workflows/deploy-pages.yml`。

关键字段：

| 字段 | 作用 |
|---|---|
| `on.push` | 推到 main 就跑 |
| `paths` | 只有这些文件变了才跑 |
| `workflow_dispatch` | Actions 页手动按钮 |
| `permissions` | 限制 GITHUB_TOKEN |
| `concurrency` | 避免两次部署互相覆盖 |
| `runs-on` | 一般 `ubuntu-latest` |
| `${{ }}` | 读上下文、密钥、上一步输出 |
| `with.path: web` | 站点根目录 |

`cron` 是 UTC。中国时间减 8 小时。

---

## 4. 密钥

Settings → Secrets and variables → Actions。

COS 线需要：`COS_SECRET_ID` `COS_SECRET_KEY` `COS_BUCKET` `COS_REGION`。

YAML 里写 `${{ secrets.COS_SECRET_ID }}`，永远不要把密钥贴进文件。Fork PR 读不到你的 secrets。

---

## 5. 两条发布线

```
push main
  → deploy-pages.yml → https://1004cq.github.io/yun-keben/
  → deploy-cos.yml    → 腾讯云 COS（手动跑，要先配 Secrets）
```

Pages 只发 HTML/目录，不发 PDF。

---

## 6. 第一次跑通 Pages

1. Settings → Pages → Source = **GitHub Actions**
2. Actions 页打开 Deploy Pages → Run workflow
3. 等绿勾，地址一般是 `https://1004cq.github.io/yun-keben/`
4. 改 `web/` 再 push，应自动更新

404 常见原因：Source 还停在 branch；`path` 指错；资源用了绝对路径 `/config.js`（项目站根是 `/yun-keben/`，必须 `./config.js`）。

---

## 7. catalog 也可以在 Actions 里生

`deploy-pages.yml` 会跑 `scripts/build_catalog.py`，用 `GITHUB_TOKEN` 提高 API 限额。
生成结果打进 Pages 产物，**不 commit 回 main**，避免机器人刷 commit。

---

## 8. COS 线

`deploy-cos.yml` 默认只有 `workflow_dispatch`。配 Secrets 后手动跑。用子账号密钥，不要用主账号。

---

## 9. 调试

Actions → 点失败的 job 看日志 → Re-run。

| 现象 | 原因 |
|---|---|
| pages permission denied | 缺 `pages: write` / `id-token: write` |
| Artifact not found | path 为空或两个 workflow 没衔接 |
| 403 rate limit | 生成 catalog 没带 token |
| Secret 为空 | 名字拼错或在 fork PR 里跑 |

---

## 10. 练习顺序

1. 对照 `deploy-pages.yml` 逐行读
2. Pages Source 改成 Actions，手动跑一次
3. 改 index.html 一个字再 push，看是否自动变绿
4. 有 COS 后再启 `deploy-cos.yml`
