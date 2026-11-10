# 效果验证

测试预期与离线结果见 `examples/*.input.json`、同名 `*.output.json` 和 `examples/test-results.txt`。输出内 `trace` 即实际运行路径。

| 用例 | 预期 | 结果文件 |
| --- | --- | --- |
| 明确答案 | 引用 D03，回答 2GB | `clear.output.json` |
| 文档冲突 | 引用 D01、D02，追问适用制度 | `conflict.output.json` |
| 资料外 | `insufficient` | `outside.output.json` |
| 改写相似 | 定位 D03 | `paraphrase.output.json` |
| 上下文追问 | 结合历史定位 D03 | `followup.output.json` |
| 读取工具失败 | 不给未经核查的答案 | `failure.output.json` |

额外测试：将冲突语料换为仅含 D01 的 `single-document.json`，预期从 `conflict` 变为 `answered` 且答案为 30 天；一步上限返回 `incomplete`；伪造引用和忽略未读冲突候选均被拒绝。

测试结果仅覆盖离线 Mock 与程序校验。未提供 API 密钥，尚未实测真实模型的工具选择、改写理解或追问质量。实际运行环境与结果以 `examples/test-results.txt` 为准。

本次本机使用 Python 3.12.9 运行生成脚本，六套命令均以退出码 0 结束；11 项单元测试全部通过。离线路径分别为：明确答案 3 步、冲突 4 步、资料外 2 步、改写相似 3 步、上下文追问 3 步、工具失败 3 步。
