# Ponderada 5

## Informações do Aluno  
Aluno | Curso | Módulo | Turma
:---: | :---: | :---: | :---:
Caio Martins de Abreu | Engenharia da Computação | 9 | 2



### Configuração do Ambiente

1. Clone o repositório:

    ```bash
    cd ~
    git clone https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO.git m9-p
    cd m9-p/ponderada_6_7
    ```

Obs: Espera-se que o usuário possua o docker instalados em sua máquina. Caso não possua, siga as instruções de instalação no site oficial do [Docker](https://docs.docker.com/get-docker/).

## Execução
Para executar a aplicação, siga os passos abaixo:

Crie os arquivos:
1. confluent_kafka.env
    ```bash
    touch confluent_kafka.env
    ```

2. hive.env
    ```bash
    touch hive.env
    ```

3. mongo.env
    ```bash
    touch mongo.env
    ```

No arquivo confluent_kafka.env, adicione as seguintes variáveis de ambiente, com as credenciais da sua interface Kafka na Confluent Cloud:
```bash
    [default]
    KAFKA_BOOTSTRAP_SERVERS=seu-endereco-confluent-cloud:9092
    KAFKA_API_KEY=sua-chave-api
    KAFKA_API_SECRET=sua-chave-secreta
    KAFKA_SECURITY_PROTOCOL=SASL_SSL
    KAFKA_MECHANISM=PLAIN
    KAFKA_CLIENT_ID=seu-client-id
    KAFKA_GROUP_ID=seu-group-id

    [producer]

    [consumer]
    KAFKA_TOPIC=topico-criado-no-confluent-cloud
```

No arquivo hive.env, adicione as seguintes variáveis de ambiente com as credenciais do seu broker MQTT:
```bash
    BROKER=seu-endereco-broker
    PORT=8883
    PROFILE=seu-profile
    PASSWORD=senha-do-broker
    TOPIC=topic-qualquer
    CLIENT_ID=seu-client-id
    QOS=qos-do-topico
```

No arquivo mongo.env, adicione as seguintes variáveis de ambiente, com as credenciais do seu banco de dados MongoDB criado no Atlas:
```bash
    MONGO_USER=seu-usuario
    MONGO_PASSWORD=sua-senha
```

Para executar a aplicação, execute o comando:
```bash
docker compose up -d --build --wait
```

## Demonstração

[demo](https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO/assets/99201276/f1d41a1a-ceb5-4c36-b721-a8e252825d70)
