from typing import Dict, Any, List
from .agent_core import BaseAgent, AgentMessage


class CodeAgent(BaseAgent):
    """
    代码任务Agent：
    根据需求分析结果，生成嵌入式研发任务与模块边界。
    """

    def __init__(self):
        super().__init__("CodeAgent")

    def run(self, context: Dict[str, Any]) -> AgentMessage:
        modules: List[str] = context.get("modules", [])

        tasks = []
        for module in modules:
            if "STM32" in module:
                tasks.append("编写 STM32 外设初始化框架，包括 ADC、DMA、TIM、USART 等模块。")
            elif "ESP32" in module:
                tasks.append("设计 ESP32 Wi-Fi / MQTT 通信任务，支持数据上传和远程控制。")
            elif "CAN" in module or "诊断" in module:
                tasks.append("设计 CAN/UDS 日志解析模块，识别请求帧、响应帧、超时和测试结论。")
            elif "OLED" in module:
                tasks.append("设计 OLED 状态显示模块，用于显示系统状态、测试结果和异常提示。")
            elif "INA226" in module:
                tasks.append("设计 INA226 电压电流采样接口，输出电压、电流和功率数据。")
            elif "报告" in module or "文档" in module:
                tasks.append("设计 Markdown 报告生成模块，自动汇总需求、测试结果和结论。")
            else:
                tasks.append(f"围绕“{module}”建立独立任务与接口说明。")

        pseudo_code = self.build_pseudo_code()

        content = "\n".join([
            "## 代码Agent输出",
            "",
            "### 开发任务",
            *[f"- {task}" for task in tasks],
            "",
            "### 伪代码结构",
            "```c",
            pseudo_code,
            "```",
        ])

        return AgentMessage(
            role=self.name,
            content=content,
            metadata={
                "code_tasks": tasks,
                "pseudo_code": pseudo_code,
            },
        )

    def build_pseudo_code(self) -> str:
        return """void app_init(void) {
    system_clock_init();
    sensor_init();
    communication_init();
    display_init();
}

void app_loop(void) {
    read_sensor_data();
    update_control_state();
    analyze_test_status();
    publish_result();
    generate_log_record();
}"""
