from faker import Faker 
from typing import Any

from .data_model import Sensor


class Generator:
    def __init__(self):
        self.faker = Faker()
        
    def data_generator(self) -> dict[str, Any]:
        sensor = Sensor(
            name='Sensor_' + self.faker.unique.bothify(text='???-###'),
            latitude=self.faker.latitude(),
            longitude=self.faker.longitude(),
            date=self.faker.date_time_this_month().isoformat(),
            temperature=self.faker.pyfloat(
                min_value=-10,
                max_value=40,
                right_digits=2
            ),
            humidity=self.faker.pyfloat(
                min_value=0,
                max_value=100,
                right_digits=2
            ),
            pressure=self.faker.pyfloat(
                min_value=760,
                max_value=1100,
                right_digits=2
            )
        ).model_dump(mode='json')
        return sensor