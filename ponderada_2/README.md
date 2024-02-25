# Documentação do Simulador IoT

Este repositório contém um simulador de dispositivos IoT desenvolvido como parte da atividade de aprendizado. O simulador envia dados para um broker MQTT, e este documento fornece instruções sobre como instalar, configurar e validar o funcionamento do simulador utilizando testes automatizados.

## Instalação

Para instalar e executar o simulador IoT e os testes associados, siga estas etapas:

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Broker MQTT (Mosquitto, HiveMQ, etc.)

### Configuração do Ambiente

1. Clone o repositório:

    ```bash
    git clone https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO.git m9-p
    cd m9-p/ponderada_2
    ```

2. Instale as dependências:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -e .
    pip install -e ".[test]"
    ```

## Uso do Simulador

Para executar os testes do simulador IoT, utilize o seguinte comando:

```bash
pytest
```
## Testes
### Teste de Publicação

Este teste verifica a funcionalidade de publicação de uma classe `Publisher` em Python. Usamos a biblioteca `pytest` para definir os testes e `unittest.mock` para criar objetos simulados (mocks) que substituem dependências durante o teste.

### Código - `test_broker_publisher.py`
```python 
import pytest
from unittest.mock import MagicMock
from mypkg.broker.publisher import Publisher


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def mock_qos():
    return 1


@pytest.fixture
def publisher(mock_client, mock_qos):
    return Publisher(mock_client, mock_qos)


def test_publish(publisher, mock_client, mock_qos):
    topic = "test/topic"
    payload = "test message"
    publisher.publish(topic, payload)
    mock_client.publish.assert_called_once_with(topic, payload, qos=mock_qos)
```

### Fixtures

- `mock_client`: Cria um cliente simulado usando `MagicMock`.
- `mock_qos`: Define o Quality of Service (QoS) como 1 para as mensagens MQTT.
- `publisher`: Cria uma instância da classe `Publisher` usando o `mock_client` e `mock_qos` como argumentos.

### Finalidade

- `test_publish`: Verifica se o método `publish` da classe `Publisher` é chamado corretamente com os argumentos esperados: `topic`, `payload` e `qos`.
  - `topic`: Define o tópico da mensagem como "test/topic".
  - `payload`: Define o conteúdo da mensagem como "test message".
  - O teste confirma se `mock_client.publish` é chamado uma vez com os argumentos `topic`, `payload` e `qos`.

Este teste garante que a classe `Publisher` interaja corretamente com o cliente MQTT simulado, respeitando o QoS definido.


### Teste de Inscrição

Este teste avalia a funcionalidade de inscrição de uma classe `Subscriber` em Python. Utilizamos a biblioteca `pytest` para organizar os testes e `unittest.mock` para criar objetos simulados (mocks), que atuam como substitutos das dependências reais durante os testes.

### Código - `test_broker_subscriber.py`
```python
import pytest
from unittest.mock import MagicMock
from mypkg.broker.subscriber import Subscriber

@pytest.fixture
def mock_client():
    return MagicMock()

@pytest.fixture
def mock_qos():
    return 1

@pytest.fixture
def subscriber(mock_client, mock_qos):
    return Subscriber(mock_client, mock_qos)

def test_subscribe(subscriber, mock_client, mock_qos):
    topic = "test/topic"
    subscriber.subscribe(topic)
    mock_client.subscribe.assert_called_once_with(topic, mock_qos)
```

### Fixtures

- `mock_client`: Gera um cliente MQTT simulado utilizando `MagicMock`.
- `mock_qos`: Estabelece o Quality of Service (QoS) em 1, indicando a garantia de entrega das mensagens MQTT.
- `subscriber`: Constrói uma instância da classe `Subscriber`, passando `mock_client` e `mock_qos` como parâmetros, preparando-a para o teste.

### Objetivo

- `test_subscribe`: Verifica se o método `subscribe` da classe `Subscriber` é executado corretamente com os parâmetros esperados, `topic` e `qos`.
  - `topic`: Determina o tópico ao qual a inscrição deve ser feita, neste caso, "test/topic".
  - O teste assegura que `mock_client.subscribe` seja chamado uma única vez com `topic` e `mock_qos` como argumentos, garantindo que a inscrição seja feita adequadamente com o nível de QoS especificado.

Este teste confirma a correta funcionalidade da classe `Subscriber` ao interagir com um cliente MQTT simulado, respeitando o nível de QoS estabelecido para a inscrição.

### Testes de QoS em Publisher e Subscriber

Estes testes verificam a funcionalidade de Quality of Service (QoS) tanto para a classe `Publisher` quanto para a `Subscriber` em Python, utilizando a biblioteca `pytest` para a definição dos testes e `unittest.mock` para a criação de objetos simulados (mocks).

### Código - `test_broker_qos.py`
```python
import pytest
import json
from unittest.mock import MagicMock
from mypkg.broker.publisher import Publisher
from mypkg.broker.subscriber import Subscriber

@pytest.fixture
def config():
    with open('simulator_config.json', 'r') as f:
        return json.load(f)

@pytest.fixture
def mock_qos(config):
    return config['mqtt']['qos']

@pytest.fixture
def mock_client():
    return MagicMock()

@pytest.fixture
def publisher(mock_client, mock_qos):
    return Publisher(mock_client, mock_qos)

@pytest.fixture
def subscriber(mock_client, mock_qos):
    return Subscriber(mock_client, mock_qos)

def test_publisher_qos(publisher, mock_client, mock_qos):
    publisher.publish("test/topic", "test message")
    mock_client.publish.assert_called_with("test/topic", "test message", qos=mock_qos)

def test_subscriber_qos(subscriber, mock_client, mock_qos):
    subscriber.subscribe("test/topic")
    mock_client.subscribe.assert_called_with("test/topic", mock_qos)
```

### Fixtures

- `config`: Carrega a configuração do simulador de um arquivo JSON, incluindo o QoS.
- `mock_qos`: Extrai o valor de QoS da configuração carregada.
- `mock_client`: Cria um cliente MQTT simulado.
- `publisher`: Instancia a classe `Publisher` com `mock_client` e `mock_qos`.
- `subscriber`: Instancia a classe `Subscriber` com `mock_client` e `mock_qos`.

### Objetivos

- `test_publisher_qos`: Verifica se o método `publish` da classe `Publisher` utiliza o QoS correto ao publicar uma mensagem.
- `test_subscriber_qos`: Assegura que o método `subscribe` da classe `Subscriber` utilize o QoS correto ao se inscrever em um tópico.

Estes testes garantem que tanto o publisher quanto o subscriber respeitam o nível de QoS definido na configuração.


### Teste de Estrutura e Valores de Dados de Sensores Falsos

Este teste avalia a `SensorDataGenerator`, uma classe em Python projetada para gerar dados falsos de sensores. Utilizamos `pytest` para a estruturação do teste e `json` para manipulação de dados no formato JSON.

### Código - `test_sensor_data_generator.py`
```python
import pytest
import json
from mypkg.generator.fake_data import SensorDataGenerator

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
```

### Fixture

- `sensor_data_generator`: Cria uma instância da `SensorDataGenerator` para ser usada nos testes.

### Objetivo

O teste `test_fake_sensor_data_structure_and_values` verifica se a estrutura e os valores gerados pela `SensorDataGenerator` estão corretos, incluindo:

- Presença de chaves esperadas (`name`, `latitude`, `longitude`, `date`, `sensor_data`) no JSON gerado.
- Tipos de dados corretos para cada campo.
- Valores dentro dos intervalos especificados para os dados dos sensores.
- Formato correto da data.

Este teste assegura que os dados falsos gerados pela `SensorDataGenerator` sejam consistentes e válidos para simulações ou testes que dependam deles.


### Teste de Integração entre Publisher e Subscriber MQTT

Este teste avalia a integração entre as classes `Publisher` e `Subscriber` em um cenário real de publicação e subscrição utilizando o protocolo MQTT. A biblioteca `pytest` é usada para estruturar o teste, e a biblioteca `paho.mqtt.client` é utilizada para interagir com o broker MQTT.

### Código - `test_pub_sub_integration.py`
```python
import pytest
import paho.mqtt.client as mqtt
from mypkg.broker.publisher import Publisher
from mypkg.broker.subscriber import Subscriber
import time

BROKER = 'broker.hivemq.com'
PORT = 1883
QOS = 1

@pytest.fixture
def client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "R2-D2")
    client.connect(BROKER, PORT, 60)
    return client

def test_pub_sub_integration(client):
    subscriber = Subscriber(client, QOS)
    publisher = Publisher(client, QOS)

    test_topic = "test/integration"
    test_payload = "Hello MQTT"

    received_messages = []

    def on_message(client, userdata, message):
        received_messages.append(message)

    client.on_message = on_message
    subscriber.subscribe(test_topic)

    client.loop_start()
    time.sleep(5)

    publisher.publish(test_topic, test_payload)
    time.sleep(5)

    client.loop_stop()

    assert len(received_messages) > 0

    message = received_messages[0]
    assert message.topic == test_topic
    assert message.payload.decode() == test_payload
    assert message.qos == QOS
```

### Fixture

- `client`: Cria e configura uma instância do cliente MQTT para se conectar ao broker especificado.

### Objetivo

O `test_pub_sub_integration` visa validar a funcionalidade de publicação e subscrição do MQTT em um ambiente integrado, garantindo que:

- Mensagens publicadas em um tópico sejam recebidas corretamente pelos inscritos no mesmo tópico.
- O payload e o QoS da mensagem recebida correspondam aos da mensagem enviada.

Este teste assegura a correta interação entre os componentes de publicação e subscrição do MQTT, utilizando um broker real para simular um cenário de uso prático.

## Validação


[m9-p2.webm](https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO/assets/99201276/cfd37385-d26b-4121-9c7f-ecc568224c79)
