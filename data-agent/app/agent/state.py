from typing import TypedDict

from app.entities.column_info import ColumnInfo
from app.entities.metric_info import MetricInfo

class ColumnInfoState(TypedDict):
    name: str
    type: str
    role: str
    examples: list[str]
    description: str
    alias: list[str]


class TableInfoState(TypedDict):
    name: str
    role: str
    description: str
    columns: list[ColumnInfoState]

class MetricInfoState(TypedDict):
    name: str
    description: str
    relevant_columns: list[str]
    alias: list[str]

class DataAgentState(TypedDict):
    query: str #
    keywords: list[str]
    retrieved_column_infos: list[ColumnInfo]
    retrieved_metric_infos: list[MetricInfo]
    retrieved_value_infos: list[MetricInfo]


    metric_info_states: list[MetricInfoState]
    table_info_states: list[TableInfoState]

    error: str # 校验SQL是否错误
