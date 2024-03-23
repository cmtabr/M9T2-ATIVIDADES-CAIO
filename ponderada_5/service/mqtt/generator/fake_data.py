import time
from faker import Faker
from faker.providers import BaseProvider
from typing import Any
from ..sensor.model import Sensor


class StarWarsProvider(BaseProvider):
    def star_wars_character(self):
        characters = [
            "Anakin Skywalker", "Obi-Wan Kenobi", "Luke Skywalker",
            "Leia Organa", "Han Solo", "Chewbacca", "Yoda",
            "Darth Vader", "Padme Amidala", "Mace Windu"
        ]
        return self.random_element(characters)


class SensorDataGenerator:
    def __init__(self) -> None:
        self.fake = Faker()
        self.fake.add_provider(StarWarsProvider)

    def fake_sensor_data(self) -> dict[str, Any]:
        sensor_data = Sensor(
                name=self.fake.star_wars_character(),
                latitude=self.fake.latitude(),
                longitude=self.fake.longitude(),
                date=time.strftime('%Y-%m-%d %H:%M:%S'),
                temperature=self.fake.pyfloat(
                    min_value=-40,
                    max_value=60,
                    right_digits=2
                ),
                humidity=self.fake.pyfloat(
                    min_value=0,
                    max_value=100,
                    right_digits=2
                ),
                pressure=self.fake.pyfloat(
                    min_value=800,
                    max_value=1200,
                    right_digits=2
                )
            ).model_dump(mode='json')
        return sensor_data
