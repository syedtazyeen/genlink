from pydantic import BaseModel


class StringResponse(BaseModel):
    value: str


class BooleanResponse(BaseModel):
    value: bool


class IntegerResponse(BaseModel):
    value: int


class FloatResponse(BaseModel):
    value: float
