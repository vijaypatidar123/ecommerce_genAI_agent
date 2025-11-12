from typing import Optional, Any, Dict
from dataclasses import dataclass, field

@dataclass
class GraphState:
    user_query: str = ""
    schema_md: Optional[str] = None
    sql_query: Optional[str] = None
    sql_valid: bool = False
    sql_result: Optional[Any] = None
    answer_valid: bool = False
    answer_feedback: Optional[str] = None
    summary: Optional[str] = None
    external_info: Optional[str] = None
    iteration_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def df(self):
        """Alias for backward compatibility"""
        return self.sql_result
