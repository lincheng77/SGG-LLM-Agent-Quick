import asyncio
from typing import Optional

from sqlalchemy import text
from sqlalchemy.engine import cursor
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from app.conf.app_config import DBConfig, app_config


class MysqlClientManager:
    def __init__(self, db_config: DBConfig):
        self.db_config = db_config
        self.engine: Optional[AsyncEngine] = None
        self.session_factory = None

    def _get_url(self):
        return (f"mysql+asyncmy://{self.db_config.user}:"
                f"{self.db_config.password}@{self.db_config.host}:"
                f"{self.db_config.port}/{self.db_config.database}?charset=utf8mb4")

    def init(self):
        self.engine = create_async_engine(self._get_url(),
                                          pool_size=10,
                                          pool_pre_ping=True)              # 连接前检测：每次从连接池取连接时先 ping 一下
        self.session_factory = async_sessionmaker(self.engine,
                                                  autoflush=True,          # 自动 flush：执行查询前自动把内存中的改动写入数据库
                                                                           # 👉 保证查询能看到最新数据

                                                  expire_on_commit=False,  # 提交后是否让对象“失效”
                                                                           # False：提交后对象还能直接访问（推荐，避免重新查询）
                                                                           # True：提交后访问属性会重新触发 DB 查询

                                                  autobegin=True)          # 自动开启事务（SQLAlchemy 2.x 行为）
                                                                           # 只是开启，还需要手动提交
    async def close(self):
        await self.engine.dispose()


dw_mysql_client_manager = MysqlClientManager(app_config.db_dw)
meta_mysql_client_manager = MysqlClientManager(app_config.db_meta)

if __name__ == '__main__':
    meta_mysql_client_manager.init()


    async def test():
        async with meta_mysql_client_manager.session_factory() as session:
            result = await session.execute(text("select * from table_info limit 10"))
            rows = result.fetchall()
            print(rows)



    asyncio.run(test())

    
