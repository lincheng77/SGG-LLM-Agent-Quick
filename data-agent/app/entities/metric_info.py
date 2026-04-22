from dataclasses import dataclass
from typing import Optional


@dataclass
class MetricInfo:
    """指标信息业务实体类"""
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    relevant_columns: Optional[dict | list] = None
    alias: Optional[dict | list] = None
