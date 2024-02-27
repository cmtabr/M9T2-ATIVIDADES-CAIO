import pytest
import json
from mqtt.generator.fake_data import SensorDataGenerator


@pytest.fixture
def sensor_data_generator():
    return SensorDataGenerator()


def test_fake_sensor_data_structure_and_values(sensor_data_generator):
    result = sensor_data_generator.fake_sensor_data()
    data = json.loads(result)

    assert 'name' in data
    assert 'latitude' in data
    assert 'longitude' in data
    assert 'date' in data
    assert 'sensor_data' in data
    sensor_keys = [
                'carbon_monoxide_ppm', 'nitrogen_dioxide_ppm',
                'hydrogen_ppm', 'methane_ppm'
            ]
    for key in sensor_keys:
        assert key in data['sensor_data']

    assert isinstance(data['name'], str)
    assert isinstance(data['latitude'], float)
    assert isinstance(data['longitude'], float)
    assert isinstance(data['date'], str)
    for key in sensor_keys:
        assert isinstance(data['sensor_data'][key], float)

    assert 1 <= data['sensor_data']['carbon_monoxide_ppm'] <= 1000
    assert 0.05 <= data['sensor_data']['nitrogen_dioxide_ppm'] <= 10
    assert 1 <= data['sensor_data']['hydrogen_ppm'] <= 1000
    assert 1000 <= data['sensor_data']['methane_ppm'] <= 300000

    from datetime import datetime
    try:
        datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        date_format_is_correct = True
    except ValueError:
        date_format_is_correct = False
    assert date_format_is_correct
