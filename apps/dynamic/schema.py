from pydantic import BaseModel


class DynamicModel(BaseModel):
    name: str
    desc: str
    param: dict


