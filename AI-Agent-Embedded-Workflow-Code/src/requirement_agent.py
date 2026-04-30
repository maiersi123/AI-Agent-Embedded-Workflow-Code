import re
from typing import Dict, Any, List
from .agent_core import BaseAgent, AgentMessage


class RequirementAgent(BaseAgent):
    """
    需求分析Agent：
    将项目brief拆解为模块、接口、风险点和验收指标。
    """

    KEYWORDS = {
        "STM32": "STM32主控/外设驱动",
        "ESP32": "ESP32物联网通信",
        "CAN": "CAN/UDS诊断测试",
        "MQTT": "MQTT云平台通信",
        "INA226": "电压电流采样",
        "OLED": "OLED本地显示",
        "Buck": "Buck驱动电路",
        "日志": "测试日志分析",
        "报告": "项目报告生成",
    }

    def __init__(self):
        super().__init__("RequirementAgent")

    def run(self, context: Dict[str, Any]) -> AgentMessage:
        brief = context.get("project_brief", "")
        modules = self.extract_modules(brief)
        acceptance = self.build_acceptance_criteria(modules)

        content = "\n".join([
            "## 需求分析结果",
            "",
            "### 功能模块",
            *[f"- {m}" for m in modules],
            "",
            "### 验收指标",
            *[f"- {a}" for a in acceptance],
        ])

        return AgentMessage(
            role=self.name,
            content=content,
            metadata={
                "modules": modules,
                "acceptance": acceptance,
            },
        )

    def extract_modules(self, text: str) -> List[str]:
        modules = []
        for key, value in self.KEYWORDS.items():
            if key.lower() in text.lower():
                modules.append(value)

        # 兜底模块，保证项目完整
        default_modules = [
            "需求拆解与任务规划",
            "代码结构设计",
            "测试数据分析",
            "技术文档生成",
        ]
        for item in default_modules:
            if item not in modules:
                modules.append(item)

        return modules

    def build_acceptance_criteria(self, modules: List[str]) -> List[str]:
        criteria = [
            "能够读取项目需求并输出结构化模块清单",
            "能够根据模块生成代码开发任务和接口建议",
            "能够解析测试日志并生成表格化结果",
            "能够输出Markdown格式项目报告",
        ]
        if any("CAN" in m or "诊断" in m for m in modules):
            criteria.append("能够识别UDS请求、正响应、测试结论和关键时间戳")
        if any("电压" in m or "Buck" in m for m in modules):
            criteria.append("能够辅助整理电压、电流、纹波和扰动实验描述")
        return criteria
