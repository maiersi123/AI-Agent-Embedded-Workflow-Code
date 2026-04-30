from pathlib import Path
from typing import Dict, Any
import pandas as pd
from .agent_core import BaseAgent, AgentMessage


class ReportAgent(BaseAgent):
    """
    报告生成Agent：
    汇总各Agent输出，并生成Markdown报告和CSV表格。
    """

    def __init__(self, output_dir: str = "outputs"):
        super().__init__("ReportAgent")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, context: Dict[str, Any]) -> AgentMessage:
        report_path = self.output_dir / "agent_report.md"
        csv_path = self.output_dir / "test_summary.csv"

        requirement_text = context.get("requirement_text", "")
        code_text = context.get("code_text", "")
        test_text = context.get("test_text", "")
        test_summary = context.get("test_summary", {})

        report = "\n\n".join([
            "# AI Agent 嵌入式研发辅助报告",
            "## 1. 项目概述",
            "本报告由 Agent 工作流自动生成，用于展示 AI Agent 在需求拆解、代码任务生成、测试日志分析和文档整理中的应用。",
            requirement_text,
            code_text,
            test_text,
            "## 5. 结论",
            "该流程能够将分散的项目需求、测试日志和代码任务整理为结构化成果，适用于课程设计、论文材料、测试分析和项目申报。"
        ])

        report_path.write_text(report, encoding="utf-8")

        df = pd.DataFrame([{
            "test_name": test_summary.get("test_name"),
            "start_time": test_summary.get("start_time"),
            "end_time": test_summary.get("end_time"),
            "duration_seconds": test_summary.get("duration_seconds"),
            "request_count": len(test_summary.get("requests", [])),
            "response_count": len(test_summary.get("responses", [])),
            "verdict": test_summary.get("verdict"),
        }])
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        content = "\n".join([
            "## 报告生成完成",
            f"- Markdown报告：{report_path}",
            f"- 测试结果表格：{csv_path}",
        ])

        return AgentMessage(
            role=self.name,
            content=content,
            metadata={
                "report_path": str(report_path),
                "csv_path": str(csv_path),
            },
        )
