from pydantic import BaseModel, Field


class QuerySchema(BaseModel):
    query: str
