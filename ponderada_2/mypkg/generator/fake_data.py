import json
import time
from faker import Faker
from faker.providers import BaseProvider

from ..sensor.mics6814 import MiCS6814


class StarWarsProvider(BaseProvider):
    def star_wars_character(self):
        characters = [
            "Anakin Skywalker", "Obi-Wan Kenobi", "Luke Skywalker",
            "Leia Organa", "Han Solo", "Chewbacca", "Yoda",
            "Darth Vader", "Padmé Amidala", "Mace Windu"
        ]
        return self.random_element(characters)


class SensorDataGenerator:
    def __init__(self) -> None:
        self.fake = Faker()
        self.fake.add_provider(StarWarsProvider)

    def fake_sensor_data(self) -> str:
        sensor_data = MiCS6814(
            name=self.fake.star_wars_character(),
            latitude=self.fake.latitude(),
            longitude=self.fake.longitude(),
            date=time.strftime('%Y-%m-%d %H:%M:%S'),
            sensor_data={
                'carbon_monoxide_ppm': self.fake.pyfloat(
                                                    min_value=1,
                                                    max_value=1000,
                                                    right_digits=2
                                                ),
                'nitrogen_dioxide_ppm': self.fake.pyfloat(
                                                    min_value=0.05,
                                                    max_value=10,
                                                    right_digits=2
                                                ),
                'hydrogen_ppm': self.fake.pyfloat(
                                            min_value=1,
                                            max_value=1000,
                                            right_digits=2
                                        ),
                'methane_ppm': self.fake.pyfloat(
                                            min_value=1000,
                                            max_value=300000,
                                            right_digits=2
                                        ),
                }
            ).model_dump()
        return json.dumps(sensor_data)
