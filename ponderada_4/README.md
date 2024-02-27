# Testes
- [x] Teste de Integração
- [x] Testes Unitários

## Demonstração
Seguindo a mesma premissa da ponderada anterior de testes, foram mantidos os testes unitários para publishers e subscribers, adcionando contudo o teste de integração do sistema com a HiveMq como segue no vídeo abaixo

[m9-p4.webm](https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO/assets/99201276/9ae3f380-5388-4f6c-a333-48499b956d73)

## Instalação

Para instalar e executar o simulador IoT e os testes associados, siga estas etapas:

### Pré-requisitos

- Python 3.10 ou superior
- Pip (gerenciador de pacotes Python)
- Broker MQTT (Mosquitto, HiveMQ, etc.)

### Configuração do Ambiente

1. Clone o repositório:

    ```bash
    git clone https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO.git m9-p
    cd m9-p/ponderada_4
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
pytest -v -p no:warnings 
# ou tox run-parallel
```

## Explicação
Este documento fornece uma visão geral e explicações detalhadas de um script de teste de integração para um sistema de publicação e subscrição (pub/sub) usando MQTT para conectar-se ao broker hivemq.

## Bibliotecas Utilizadas

- `pytest`: Uma framework para escrever testes pequenos em Python.
- `paho.mqtt`: Uma biblioteca cliente para comunicação com brokers MQTT.
- `decouple`: Utilizada para abstrair a configuração e os segredos do código, facilitando a gestão de configurações.
- `json`: Para codificação e decodificação de dados em JSON, um formato leve de troca de dados.
- `time`: Para adicionar atrasos no script, permitindo a comunicação assíncrona entre o publicador e o assinante.

## Configurações

As configurações como endereço do broker, porta, qualidade de serviço (QoS), usuário, senha, etc., são lidas do ambiente ou arquivos de configuração usando `decouple`. Isso torna o teste mais flexível e seguro, pois evita hardcoding de informações sensíveis no código.

## Fixtures do Pytest

- `client`: Cria uma instância do cliente MQTT com configurações necessárias, incluindo SSL/TLS para uma conexão segura.
- `mock_generator`: Simula um gerador de dados de sensor, criando um payload falso para ser publicado e testado.

## Teste de Integração Pub/Sub

O teste `test_pub_sub_integration` simula um cenário de publicação e subscrição onde:

1. Um `Publisher` publica dados falsos de sensor no tópico configurado.
2. Um `Subscriber` se inscreve no mesmo tópico e espera por mensagens.
3. Mensagens publicadas são capturadas pelo assinante, e o teste verifica se a mensagem recebida corresponde à mensagem enviada.

### Callbacks Importantes

- `on_connect`: Confirma se a conexão com o broker foi bem-sucedida.
- `on_publish`: Confirma se a mensagem foi publicada com sucesso.
- `on_message`: Captura e processa mensagens recebidas pelo subscriber.

### Assertivas

O teste verifica várias condições para garantir que a integração pub/sub funcione como esperado, incluindo:

- Se alguma mensagem foi recebida.
- Se os campos esperados estão presentes e não são nulos nas mensagens recebidas.
- Se os dados do sensor recebidos correspondem aos dados enviados.

## Conclusão

Este teste de integração é crucial para validar a funcionalidade básica do sistema pub/sub em um ambiente controlado, assegurando que os componentes do sistema possam comunicar-se eficientemente e corretamente entre si usando o protocolo MQTT.
