import asyncio

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState, ColumnInfoState, TableInfoState, MetricInfoState
from langgraph.runtime import Runtime

from app.core.log import logger
from app.entities.column_info import ColumnInfo
from app.entities.metric_info import MetricInfo
from app.entities.table_info import TableInfo
from app.entities.value_info import ValueInfo


async def merge_retrieved_info(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "合并召回信息"
    writer({"type": "progress", "step": step, "status": "running"})

    try:
        retrieved_column_infos: list[ColumnInfo] = state['retrieved_column_infos']
        retrieved_metric_infos: list[MetricInfo] = state['retrieved_metric_infos']
        retrieved_value_infos: list[ValueInfo] = state['retrieved_value_infos']

        meta_mysql_repository = runtime.context['meta_mysql_repository']

        # 1. 处理表信息
        # 1.1 将指标信息的相关字段信息添加到字段信息中
        retrieved_column_info_map: dict[str, ColumnInfo] = {retrieved_column_info.id: retrieved_column_info for
                                                            retrieved_column_info in retrieved_column_infos}
        for retrieved_metric_info in retrieved_metric_infos:
            for relevant_column in retrieved_metric_info.relevant_columns:
                if relevant_column not in retrieved_column_info_map:
                    column_info: ColumnInfo = await meta_mysql_repository.get_column_info_by_id(relevant_column)
                    retrieved_column_info_map[relevant_column] = column_info

        # 1.2 将字段取值加入到其所属字段的examples中
        for retrieved_value_info in retrieved_value_infos:
            value = retrieved_value_info.value
            column_id = retrieved_value_info.column_id

            # 确保字段信息已存在
            if column_id not in retrieved_column_info_map:
                column_info: ColumnInfo = await meta_mysql_repository.get_column_info_by_id(column_id)
                retrieved_column_info_map[column_id] = column_info

            # 将字段取值加入字段的examples中
            if value not in retrieved_column_info_map[column_id].examples:
                retrieved_column_info_map[column_id].examples.append(value)

        # 1.3.1 按照表对字段信息进行分组
        table_to_columns_map: dict[str, list[ColumnInfo]] = {}
        for column_info in retrieved_column_info_map.values():
            table_id = column_info.table_id
            # 确保表信息已存在
            if table_id not in table_to_columns_map:
                table_to_columns_map[table_id] = []
            # 将字段信息加入表信息中
            table_to_columns_map[table_id].append(column_info)

        # 1.3.2 强制为每个表添加主外键字段
        for table_id in table_to_columns_map.keys():
            # 获取表主外键字段
            key_columns: list[ColumnInfo] = await meta_mysql_repository.get_key_columns_by_table_id(table_id)
            # 获取表已有字段
            column_ids = [column_info.id for column_info in table_to_columns_map[table_id]]
            # 将表中还没有的主外键字段加入表中
            for key_column in key_columns:
                if key_column.id not in column_ids:
                    table_to_columns_map[table_id].append(key_column)

        # 1.3.3将表信息整理成目标格式
        table_info_states: list[TableInfoState] = []
        for table_id, column_infos in table_to_columns_map.items():
            table_info: TableInfo = await meta_mysql_repository.get_table_info_by_id(table_id)

            column_info_states: list[ColumnInfoState] = [ColumnInfoState(
                name = column_info.name,
                type = column_info.type,
                role= column_info.name,
                examples = column_info.examples,
                description= column_info.name,
                alias = column_info.name
            ) for column_info in column_infos]

            table_info_state = TableInfoState(
                name = table_info.name,
                role= table_info.role,
                columns = column_info_states,
                description = table_info.name,
            )

            table_info_states.append(table_info_state)

        # 2. 处理指标信息
        metric_info_states: list[MetricInfoState] = [MetricInfoState(
            name = retrieved_metric_info.name,
            description = retrieved_metric_info.description,
            relevant_columns = retrieved_metric_info.relevant_columns,
            alias = retrieved_metric_info.alias
        ) for retrieved_metric_info in retrieved_metric_infos]

        writer({"type": "progress", "step": step, "status": "success"})
        # logger.info(f'合并后的字段信息：{table_info_states}')
        return {
            'table_info_states': table_info_states,
            'metric_info_states': metric_info_states
        }
    except Exception as e:
        logger.error(f"合并召回信息失败：{e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
