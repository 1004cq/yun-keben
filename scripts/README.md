# scripts

## 生成目录

不下载 PDF，只请求源仓文件树。

```bash
GITHUB_TOKEN=ghp_xxx python3 scripts/build_catalog.py
```

写出 `web/catalog.json`。无 token 时 GitHub API 很容易 403。

Actions 里用自动注入的 `GITHUB_TOKEN` 跑同一条命令，产物打进 Pages，不 commit 回 `main`。

## 同步教材到 COS

在大硬盘机器上，不要在网站 VPS 或 GitHub runner 上全量 clone。

1. `git clone --filter=blob:none --sparse` 源仓
2. `git sparse-checkout set` 只要的学段目录
3. 合并 `*.pdf.1` + `*.pdf.2`
4. `rclone` / `coscli` 上传，排除 `.git` 和分片

密钥放本机或 Actions Secrets，不要写进仓库。
