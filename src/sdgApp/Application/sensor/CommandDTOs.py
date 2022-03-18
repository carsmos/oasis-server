from pydantic import BaseModel, Field


class SensorCreateDTO(BaseModel):
    name: str = Field(..., example="RGB Camera")
    type: str = Field(..., example="sensor.camera.rgb")
    desc: str
    param: dict


class SensorUpdateDTO(SensorCreateDTO):
    ...




