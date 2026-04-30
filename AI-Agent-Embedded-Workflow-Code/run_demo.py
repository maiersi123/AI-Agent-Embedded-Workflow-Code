from pathlib import Path

from src.requirement_agent import RequirementAgent
from src.code_agent import CodeAgent
from src.test_log_agent import TestLogAgent
from src.report_agent import ReportAgent


def main():
    project_brief = Path("examples/project_brief.md").read_text(encoding="utf-8")
    test_log = Path("examples/canoe_log_sample.txt").read_text(encoding="utf-8")

    context = {
        "project_brief": project_brief,
        "test_log": test_log,
    }

    # 1. 需求分析
    requirement_agent = RequirementAgent()
    requirement_msg = requirement_agent.run(context)
    context["modules"] = requirement_msg.metadata["modules"]
    context["requirement_text"] = requirement_msg.content

    # 2. 代码任务生成
    code_agent = CodeAgent()
    code_msg = code_agent.run(context)
    context["code_text"] = code_msg.content

    # 3. 测试日志分析
    test_agent = TestLogAgent()
    test_msg = test_agent.run(context)
    context["test_text"] = test_msg.content
    context["test_summary"] = test_msg.metadata["test_summary"]

    # 4. 报告输出
    report_agent = ReportAgent(output_dir="outputs")
    report_msg = report_agent.run(context)

    print("=" * 80)
    print(requirement_msg.content)
    print("=" * 80)
    print(code_msg.content)
    print("=" * 80)
    print(test_msg.content)
    print("=" * 80)
    print(report_msg.content)
    print("=" * 80)


if __name__ == "__main__":
    main()
