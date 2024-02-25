# Ponderada 1 
## Informações do Aluno  
Aluno | Curso | Módulo | Turma
:---: | :---: | :---: | :---:
Caio Martins de Abreu | Engenharia da Computação | 9 | 2

## Descrição
Avaliar a tríade CIA em uma conexão com um broker MQTT.

## Perguntas - Roteiro
1. O que acontece se você utilizar o mesmo ClientID em outra máquina ou sessão do browser? Algum pilar do CIA Triad é violado com isso?

**R.:** Ele é desconectado da sessão anterior e conectado na nova sessão. O pilar de disponibilidade é violado, pois o cliente é desconectado sem aviso prévio.

2. Com os parâmetros de resources, algum pilar do CIA Triad pode ser facilmente violado?

```dockerfile
version: "3.7"
services:
  mqtt5:
    image: eclipse-mosquitto
    container_name: mqtt5
    ports:
      - "1883:1883" # Default MQTT port
      - "9001:9001" # Default MQTT port for WebSockets
    volumes:
      - ./config:/mosquitto/config:rw
      - ./data:/mosquitto/data:rw
      - ./log:/mosquitto/log:rw
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '0.01'
          memory: 100M

volumes:
  config:
  data:
  log:

networks:
  default:
    name: p3-network
```

**R.:** Sim, o pilar de disponibilidade, pois o container pode ser facilmente derrubado por falta de recursos. 

3. Já tentou fazer o Subscribe no tópico #? (sim, apenas a hashtag). O que acontece?

**R.:** O '#' é um wildcard multi-level, um método coringa que permite inscrever-se em todos os tópicos disponíveis. Isso pode ser perigoso, pois pode violar a confidencialidade das mensagens.

4. Sem autenticação (repare que a variável allow_anonymous está como true), como a parte de confidencialidade pode ser violada?

**R.:** Qualquer pessoa pode se conectar ao broker e ler mensagens de qualquer tópico, violando a confidencialidade destas. Além disso a integridade também é violada, pois qualquer pessoa pode publicar mensagens em qualquer tópico.

---

## Perguntas - Desenvolvimento
**Container ID:** 80bba2902865

1. Como você faria para violar a confidencialidade?

**R.:** Para violar a confidencialidade, eu poderia me inscrever em tópicos que transitam informações sensíveis, uma vez que não haja autenticação, e ler as mensagens que passam por eles. 

> **Exemplo:**
>
> ```bash
> mosquitto_sub -h localhost -t "topic/#" -p 1883
> ```


2. Como você faria para garantir a integridade do broker MQTT?

**R.:** Para garantir a integridade dos dados criaria credencias de acesso para tópico específicos, além de delimitar quem poderia se inscrever e publicar mensagens nestes.

3. Como você faria para violar o pilar de disponibilidade?

**R.:** Para violar o pilar de disponibilidade da triade de segurança, eu poderia criar um ataque de negação de serviço (DoS) ao broker MQTT, enviando uma quantidade massiva de conexões ou mensagens, de forma a sobrecarregar o servidor e derrubá-lo.


