from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ColumnInfo:
    """列信息业务实体类"""
    id: str
    name: Optional[str] = None
    type: Optional[str] = None
    role: Optional[str] = None
    examples: Optional[dict | list] = None
    description: Optional[str] = None
    alias: Optional[dict | list] = None
    table_id: Optional[str] = None
