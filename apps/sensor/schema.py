from pydantic import BaseModel, Field


class SensorModel(BaseModel):
    name: str = Field(..., example="RGB Camera")
    type: str = Field(..., example="sensor.camera.rgb")
    desc: str
    param: dict