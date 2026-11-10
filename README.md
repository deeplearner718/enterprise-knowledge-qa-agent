# 企业知识问答 Agent（小影校招题：企业知识问答）

帮助员工从带文档 ID、版本日期的合成制度与产品资料中找到可核查的答案。命令行返回答案、原文引用、资料缺口、状态和逐步 Trace。

## 运行

需要 Python 3.10+，无第三方依赖。在仓库根目录执行：

```powershell
python -m src.main --input examples/clear.input.json --mode mock
python -m src.main --input examples/conflict.input.json --mode mock
python -m unittest discover -s tests -v
python examples/generate.py
```

真实模型模式：设置 `OPENAI_API_KEY`、`OPENAI_MODEL`，可选 `OPENAI_BASE_URL`（须提供兼容聊天补全工具调用的服务）；然后运行：

```powershell
python -m src.main --input examples/conflict.input.json --mode llm
```

使用 [官方聊天补全工具调用接口](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)。不写入密钥。模型调用或工具故障会在输出中体现；模型真实效果必须由有凭据的评审另行实测。默认最大 8 步，可用 `--max-steps` 调整。达到上限返回 `incomplete`。

输入 JSON：`question` 必填；`history` 可选，格式为 `[{"role":"user","content":"..."}]`；`fail_tools` 仅用于故障注入，可选 `search_documents` 或 `read_document`。`--data` 可替换语料文件。业务结果以 JSON 输出且进程码为 0；输入配置错误进程码为 2。

## 评审入口

| 内容 | 文件 |
| --- | --- |
| 需求与标准 | [01-requirements.md](docs/01-requirements.md) |
| 决策循环与边界 | [02-solution.md](docs/02-solution.md) |
| 用例与实测 | [03-evaluation.md](docs/03-evaluation.md) |
| AI 使用记录 | [04-ai-usage.md](docs/04-ai-usage.md) |
| 复盘 | [05-retrospective.md](docs/05-retrospective.md) |
| 合成资料 | [documents.json](data/documents.json) |
| 测试 | [test_agent.py](tests/test_agent.py) |
| 实际输出和 Trace | [examples](examples/) |

`mock` 是按观察结果运行的确定性模拟器，仅验证工具接线、引用校验与状态，不代表真实 LLM 决策效果。真实模式由模型选择检索、读取或结束动作。测试中以替换语料验证冲突消失后答案随之改变。

## 提交

题号：企业知识问答 Agent。当前文件夹不是已发布 GitHub 仓库；请审阅文档中个人贡献和实测记录，补填实际用时，再创建自己的仓库并提交：

```powershell
git init
git add .
git commit -m "完成企业知识问答 Agent 笔试项目"
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
git rev-parse HEAD
```

向评审提交该 GitHub URL 和上述命令实际输出的最终 SHA；不要填入猜测值。私有仓库须按招聘方要求开放评审权限。
