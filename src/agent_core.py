from dataclasses import dataclass, field
from typing import Any, Dict, List
import datetime


@dataclass
class AgentMessage:
    """Agent之间传递的中间结果。"""
    role: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent:
    """所有Agent的基础类。"""

    def __init__(self, name: str):
        self.name = name

    def run(self, context: Dict[str, Any]) -> AgentMessage:
        raise NotImplementedError("Subclasses must implement run().")

    def _now(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
