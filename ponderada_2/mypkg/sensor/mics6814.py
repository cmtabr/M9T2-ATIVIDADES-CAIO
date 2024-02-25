from pydantic import Field
from .model import Sensor, PayloadType


class MiCS6814(Sensor):
    sensor_data: PayloadType = Field(
        ...,
        description="Information collected by the MiCS6814 sensor"
    )
