from datetime import datetime
from pydantic import BaseModel, Field, PlainSerializer, BeforeValidator
from typing import Optional, Dict
from typing_extensions import Annotated
from uuid import uuid4

# region DateTime Custom Type
DateTimeType = Annotated[ 
    datetime, 
    BeforeValidator(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")),
    PlainSerializer(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
]
# endregion

# region Generic Data Custom Type
PayloadType = Dict[str, Optional[float]]
# endregion

# region Generic Sensor Parameters
class Sensor(BaseModel):
    id: str = Field(
                    default_factory=lambda: uuid4().hex,
                    description="Represents the unique identifier of the sensor"
                )
    name: Optional[str] = Field(
                            None, 
                            description="Represents the name of the sensor"
                        )
    latitude: float = Field(description="Represents the latitude of the sensor")
    longitude: float = Field(description="Represents the longitude of the sensor")
    date: DateTimeType = Field(
        description="Represents the date and time of the sensor reading"
    )
# endregion

# region MiCS6814 Sensor
class MiCS6814(Sensor):
    sensor_data: PayloadType = Field(
        ..., 
        description="Information collected by the MiCS6814 sensor"
    )
#endregion
