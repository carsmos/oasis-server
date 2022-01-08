from pydantic.typing import Optional, List
from pydantic import BaseModel, Field

class CarModel(BaseModel):
    type: str = Field(..., example="vehicle.tesla.model3")
    id: str = Field(..., example="ego_vehicle")
    light_state: str = "None"
    vehicle_color: List = Field(..., example=[
    0,
    0,
    255
  ])

class CarPhysicsControl(BaseModel):
    torque_curve: List[str] = Field(..., example=[
      "carla.Vector2D(x=0, y=400)",
      "carla.Vector2D(x=1300, y=600)"
    ])

class CarWheel(BaseModel):
    front_left_wheel: List[dict] = Field(..., example=[
        {
          "tire_friction": 2.0
        },
        {
          "damping_rate": 1.5
        },
        {
          "max_steer_angle": 70.0
        },
        {
          "long_stiff_value": 1000
        }
      ])
    front_right_wheel: List[dict] = Field(..., example=[
        {
          "tire_friction": 2.0
        },
        {
          "damping_rate": 1.5
        },
        {
          "max_steer_angle": 70.0
        },
        {
          "long_stiff_value": 1000
        }
      ])
    rear_left_wheel: List[dict] = Field(..., example=[
        {
          "tire_friction": 2.0
        },
        {
          "damping_rate": 1.5
        },
        {
          "max_steer_angle": 70.0
        },
        {
          "long_stiff_value": 1000
        }
      ])
    rear_right_wheel: List[dict] = Field(..., example=[
        {
          "tire_friction": 2.0
        },
        {
          "damping_rate": 1.5
        },
        {
          "max_steer_angle": 70.0
        },
        {
          "long_stiff_value": 1000
        }
      ])

class CarSensor(BaseModel):
    param: dict = Field(..., example={
            "type": "sensor.other.radar",
            "id": "front",
            "x": 2.0, "y": 0.0, "z": 1.5, "roll": 0.0, "pitch": 0.0, "yaw": 0.0,
            "horizontal_fov": 30.0,
            "vertical_fov": 10.0,
            "points_per_second": 1500,
            "range": 100.0
        })


class CarCreateDTO(BaseModel):
    name: str = Field(..., example="car_1")
    desc: Optional[str]
    autosys: Optional[str]
    model: Optional[CarModel]
    physics: Optional[CarPhysicsControl]
    wheels: Optional[CarWheel]
    sensors: Optional[List[CarSensor]]

class CarUpdateDTO(CarCreateDTO):
    ...
