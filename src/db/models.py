from dataclasses import dataclass

@dataclass
class UserHistory:
    description: str
    task_type: str
    matrix: str
    alpha_value: float = None
    c_value: float = None
