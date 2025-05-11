from typing import Callable
from fastapi import APIRouter


class DefaultByAliasFalseRouter(APIRouter):
    """
    Default FastAPI router with `response_model_by_alias=False`.
    """

    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        response_model_by_alias: bool = False,
        **kwargs
    ):
        super().__init__(
            path=path,
            endpoint=endpoint,
            response_model_by_alias=response_model_by_alias,
            **kwargs
        )
