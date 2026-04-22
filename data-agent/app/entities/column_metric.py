from dataclasses import dataclass


@dataclass
class ColumnMetric:
    """列指标关联业务实体类"""
    column_id: str
    metric_id: str
