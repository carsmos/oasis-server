from fastapi import APIRouter, status
from sdgApp.Application.sensorlib import SensorReadDTO
from sdgApp.Application.sensorlib import SensorBaseCreateDTO
from sdgApp.Application.sensorlib import SensorCommandUserCase

router = APIRouter()

# @app.post(
#     "/sensors",
#     response_model= SensorReadDTO,
#     status_code=status.HTTP_201_CREATED,
#     responses={
#         status.HTTP_409_CONFLICT: {
#             "model": "",
#         },
#     },
# )
# def create_sensor(sensor_create_model:SensorBaseCreateDTO, sensor_usecase:SensorCommandUserCase):
#     try:
#         response = sensor_usecase.create_sensor(sensor_create_model)
#
