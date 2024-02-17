# Ponderada 1 
## Informações do Aluno  
Aluno | Curso | Módulo | Turma
:---: | :---: | :---: | :---:
Caio Martins de Abreu | Engenharia da Computação | 9 | 2

## Descrição
Criar um simulador de dispositivos IoT utilizando o protocolo MQTT através do uso da biblioteca Eclipse Paho.

## Estrutura de Arquivos
ponderada-1
 ┣ sensor
 ┃ ┣ __init__.py
 ┃ ┣ fake_data.py
 ┃ ┗ model.py
 ┣ 📜README.md
 ┣ 📜main.py
 ┗ 📜requirements.txt

## Dependências
- Python 3.9 ou superior
- Mosquitto

## Instalação
Espera-se que o python já esteja instalado na máquina e o usuário esteja utilizando uma distro linux, nativamente (Ubuntu), através de uma máquina virtual ou do WSL.

Para fazer a instalação do mosquitto no linux, basta executar o comando:
```bash
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
```

## Execução
Para executar o projeto, basta seguir os passos abaixo:

Mosquitto: 
```bash
mosquitto -c mosquitto.conf
```

Execução do projeto:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mosquitto -c mosquitto.conf
python main.py
```

## Testes
Afim de validar o funcionamento do projeto, após fazer sua execução, utilizaremos o commando abaixo para se inscrever no tópico "data/mics6814" e receber as mensagens publicadas pelo projeto:
```bash
mosquitto_sub -h localhost -p 1891 -u Palpatine -v -t "data/mics6814" -q 0 
```

Este comando irá se inscrever no tópico "data/mics6814" que está sendo executado localmente (-h localhost) na porta 1891 (-p 1891), com o usuário "Palpatine" (-u Palpatine), de modo que possamos visualizar o topico inscrito (parametro -v), e irá receber as mensagens publicadas no tópico data/mics6814 (-t 'data/mics6814') com uma qualidade de service igual a 0 (-q 0).

Abaixo temos um vídeo exemplificando o funcionamento do projeto: 

