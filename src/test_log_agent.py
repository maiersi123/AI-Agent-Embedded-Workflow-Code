import re
from pathlib import Path
from typing import Dict, Any, List
from .agent_core import BaseAgent, AgentMessage


class TestLogAgent(BaseAgent):
    """
    测试日志Agent：
    解析 CANoe / UDS / 刷写日志，提取关键测试信息。
    """

    def __init__(self):
        super().__init__("TestLogAgent")

    def run(self, context: Dict[str, Any]) -> AgentMessage:
        log_text = context.get("test_log", "")
        summary = self.parse_log(log_text)

        lines = [
            "## 测试日志分析结果",
            "",
            f"- 测试名称：{summary.get('test_name', '未识别')}",
            f"- 开始时间：{summary.get('start_time', '未识别')}",
            f"- 结束时间：{summary.get('end_time', '未识别')}",
            f"- 测试耗时：{summary.get('duration_seconds', '未知')} s",
            f"- 请求帧数量：{len(summary.get('requests', []))}",
            f"- 响应帧数量：{len(summary.get('responses', []))}",
            f"- 测试结论：{summary.get('verdict', '未识别')}",
            "",
            "### 请求帧",
            *[f"- {x}" for x in summary.get("requests", [])],
            "",
            "### 响应帧",
            *[f"- {x}" for x in summary.get("responses", [])],
        ]

        return AgentMessage(
            role=self.name,
            content="\n".join(lines),
            metadata={"test_summary": summary},
        )

    def parse_log(self, text: str) -> Dict[str, Any]:
        result = {
            "test_name": None,
            "start_time": None,
            "end_time": None,
            "duration_seconds": None,
            "requests": [],
            "responses": [],
            "verdict": "unknown",
            "flash_info": {},
        }

        name_match = re.search(r"(Consecutive_Frame_Timeout_Test|[A-Za-z0-9_]+_Test)", text)
        if name_match:
            result["test_name"] = name_match.group(1)

        start_match = re.search(r"Test case begin:\s*([0-9\-: ]+)", text)
        end_match = re.search(r"Test case end:\s*([0-9\-: ]+)", text)
        if start_match:
            result["start_time"] = start_match.group(1).strip()
        if end_match:
            result["end_time"] = end_match.group(1).strip()

        timestamps = [float(x) for x in re.findall(r"(?m)^(\d+\.\d+)", text)]
        if len(timestamps) >= 2:
            result["duration_seconds"] = round(max(timestamps) - min(timestamps), 3)

        result["requests"] = re.findall(r"Request\s*\[([0-9A-Fa-f ]+)\]", text)
        result["responses"] = re.findall(r"(?:Response|Pos\.Response)\s*\[([0-9A-Fa-f ]+)\]", text)

        if re.search(r"\bpass\b", text, flags=re.IGNORECASE):
            result["verdict"] = "pass"
        if re.search(r"\bfail\b", text, flags=re.IGNORECASE):
            result["verdict"] = "fail"

        for key in ["StartAddr", "Length", "CheckSum", "VbfDataOffset"]:
            m = re.search(rf"{key}=([0-9A-Fa-fx]+)", text)
            if m:
                result["flash_info"][key] = m.group(1)

        return result
