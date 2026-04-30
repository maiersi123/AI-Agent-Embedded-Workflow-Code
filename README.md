# AI-Agent-Embedded-Workflow-Code

这是一个用于展示 **AI Agent 驱动嵌入式项目研发、测试日志分析与文档生成** 的示例代码仓库。  
项目重点不是连接真实大模型 API，而是展示可运行的 Agent 工作流框架：需求拆解、代码任务生成、CAN/CANoe 日志分析、测试表格输出和 Markdown 报告生成。

## 项目亮点

- 面向嵌入式研发流程，而不是普通聊天机器人
- 支持 Buck 驱动电路、ESP32/STM32、CAN/UDS 测试等项目场景扩展
- 可解析测试日志，提取请求帧、响应帧、测试结论和耗时
- 自动生成结构化 Markdown 报告
- 代码结构清晰，适合放到 GitHub 作为 Agent 项目成果展示

## 目录结构

```text
AI-Agent-Embedded-Workflow-Code
├── README.md
├── requirements.txt
├── run_demo.py
├── src
│   ├── agent_core.py
│   ├── requirement_agent.py
│   ├── code_agent.py
│   ├── test_log_agent.py
│   └── report_agent.py
├── examples
│   ├── project_brief.md
│   └── canoe_log_sample.txt
└── outputs
```

## 快速运行

```bash
pip install -r requirements.txt
python run_demo.py
```

运行后会在 `outputs/` 目录中生成：

```text
agent_report.md
test_summary.csv
```

## Agent 工作流

```text
项目需求输入
    ↓
RequirementAgent：拆解需求、功能模块和验收指标
    ↓
CodeAgent：生成代码任务、模块边界和伪代码建议
    ↓
TestLogAgent：解析 CANoe / 刷写 / 测试日志
    ↓
ReportAgent：生成 Markdown 项目报告和 CSV 表格
```

## 适用场景

- 嵌入式课程设计
- 智能门禁系统项目
- Buck 驱动电路论文
- CAN / UDS 诊断测试
- 测试日志分析
