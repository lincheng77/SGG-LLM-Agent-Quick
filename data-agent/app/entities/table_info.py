from dataclasses import dataclass
from typing import Optional


@dataclass
class TableInfo:
    """表信息业务实体类"""
    id: str
    name: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None