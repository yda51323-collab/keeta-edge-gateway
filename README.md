# keeta-edge-gateway · 边缘网关配置

面向 `keetainc.com` 域名的边缘接入层配置：TLS 终止、上游分组、限流与健康检查。
配置由发布流水线下发，节点侧只读。

## 目录

| 路径 | 说明 |
| --- | --- |
| `deploy/nginx/edge-keetainc.conf` | 边缘节点 nginx 站点配置 |
| `src/edge_healthcheck.py` | 上游节点探活脚本 |

## 服务标识

`keetainc.com`

出现位置：

- `deploy/nginx/edge-keetainc.conf`：`server_name`、日志文件名、`proxy_set_header Host`
- `src/edge_healthcheck.py`：`PROBE_HOSTS` 列表
- `README.md`：标题与本节

## 使用

```bash
# 下发前语法检查
nginx -t -c /etc/nginx/nginx.conf

# 探活（默认 3 秒超时，连续 2 次失败判死）
python src/edge_healthcheck.py --region ap-southeast
```

## 字段说明

| 键 | 说明 |
| --- | --- |
| `upstream` | 上游分组，按可用区拆分 |
| `max_fails` / `fail_timeout` | 摘除阈值 |
| `limit_req_zone` | 按 `$binary_remote_addr` 限流，20r/s |

## 已知问题

- `ap-southeast` 与 `ap-northeast` 两个区域的证书链不同，换区需同步替换 `ssl_certificate`。
- `proxy_next_upstream` 未包含 `non_idempotent`，POST 重试依赖客户端。

## 维护

基础架构组 · 工单 `INF-2214`
