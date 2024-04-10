from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4


class Sensor(BaseModel):
    id: str = Field(
                default_factory=lambda: uuid4().hex,
                description="Represents the unique identifier of the sensor"
                )
    name: Optional[str] = Field(
                            None,
                            description="Represents the name of the sensor"
                        )
    latitude: float = Field(
        description="Represents the latitude of the sensor"
        )
    longitude: float = Field(
        description="Represents the longitude of the sensor"
        )
    date: str = Field(
        description="Represents the date and time of the sensor reading"
    )
    temperature: float = Field(
        description="Represents the temperature of the sensor reading"
    )
    humidity: float = Field(
        description="Represents the humidity of the sensor reading"
    )
    pressure: float = Field(
        description="Represents the pressure of the sensor reading"
    )
