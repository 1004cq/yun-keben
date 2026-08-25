# scripts

```bash
GITHUB_TOKEN=ghp_xxx python3 build_catalog.py
```

生成 `web/catalog.json`。不下载 PDF。

同步见 `sync_to_cos.sh`：sparse checkout → 合并分片 → rclone 上传 COS。
