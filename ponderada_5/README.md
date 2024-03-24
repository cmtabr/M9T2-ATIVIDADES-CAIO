# Ponderada 5

## Informações do Aluno  
Aluno | Curso | Módulo | Turma
:---: | :---: | :---: | :---:
Caio Martins de Abreu | Engenharia da Computação | 9 | 2

## Descrição da Atividade
Com o intuito de fazer a integração do broker (hivemq) com o metabase, foi desenvolvida uma aplicação que faz a leitura de um tópico e grava os dados em um banco postgresql. A aplicação foi desenvolvida em python e utiliza a biblioteca paho-mqtt para a comunicação com o broker e a biblioteca psycopg2 para a comunicação com o banco de dados.

### Configuração do Ambiente

1. Clone o repositório:

    ```bash
    git clone https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO.git m9-p
    cd m9-p/ponderada_5
    ```

2. Instale as dependências:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -e .
    ```

Obs: Espera-se que o usuário possua o docker instalados em sua máquina. Caso não possua, siga as instruções de instalação no site oficial do [Docker](https://docs.docker.com/get-docker/).

## Execução
Para executar a aplicação, siga os passos abaixo:

```bash
docker compose up -d --build --wait
```
Para criar os containers do metabase e do postgresql.

```bash
cd ponderada_5/service 
python main.py
```
Para executar a aplicação.

## Demonstração

[p5.webm](https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO/assets/99201276/1aab4638-37a4-4116-8703-f218758951e4)
