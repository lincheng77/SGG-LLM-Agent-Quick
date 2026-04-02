from contextvars import ContextVar


# 定义一个上下文变量
# 如果当前上下文还没设置 request_id
# 就返回 "1"
request_id_ctx_var = ContextVar("request_id", default="1")
