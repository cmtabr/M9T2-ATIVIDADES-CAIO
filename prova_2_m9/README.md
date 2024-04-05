# Prova 2

## Informações do Aluno  
Aluno | Curso | Módulo | Turma
:---: | :---: | :---: | :---:
Caio Martins de Abreu | Engenharia da Computação | 9 | 2

## Introdução
Como pedido no enunciado da parte prática, o aluno deve integrar utilizar o kafka para realizar a distribuição de dados entre um produtor e um consumidor. O produtor deve enviar mensagens para o tópico `qualidadeAr` e o consumidor deve receber essas mensagens e imprimi-las no console.



## Funcionamento
Dado o objetivo proposto, vamos à explicação da tarefa. 

### Instalação 
```bash 
git clone https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO.git
cd prova_2_m9 
pip install -r requirements.txt
docker compose up -d --build --remove-orphans --force-recreate --wait
```

Então, gerando o producer e o consumer em terminais diferentes temos:  

1. 
```bash 
cd generator 
python kafka_consumer.py 
```
2. 
```bash 
cd generator 
python kafka_producer.py 
```

Dessa forma, será possível visualizar o arquivo `database.txt` sendo preenchido com as informações consumidas do Kafka

## Testes
Os testes para esta aplicação funcionam do seguinte modo:
1. 

2. 


## Demo

[Gravação de tela de 05-04-2024 10:52:44.webm](https://github.com/cmtabr/M9T2-ATIVIDADES-CAIO/assets/99201276/067ee6e0-108c-437f-bece-fb74e988b80e)



