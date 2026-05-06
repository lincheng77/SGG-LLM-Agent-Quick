from dataclasses import asdict

from app.entities.metric_info import MetricInfo
from app.models.metric_info import MetricInfoMySQL


class MetricInfoMapper:

    @staticmethod
    def to_entity(metric_info_mysql: MetricInfoMySQL) -> MetricInfo:
        return MetricInfo(
            id=metric_info_mysql.id,
            name=metric_info_mysql.name,
            description=metric_info_mysql.description,
            relevant_columns=metric_info_mysql.relevant_columns,
            alias=metric_info_mysql.alias
        )

    @staticmethod
    def to_model(metric_info: MetricInfo) -> MetricInfoMySQL:
        return MetricInfoMySQL(**asdict(metric_info))
