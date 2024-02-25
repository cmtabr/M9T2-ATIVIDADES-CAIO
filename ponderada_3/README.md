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

**R.:** Sim, o pilar de disponibilidade, pois o container pode ser facilmente derrubado por falta de recursos em uma eventual sobrecarga de mensagens. 

3. Já tentou fazer o Subscribe no tópico #? (sim, apenas a hashtag). O que acontece?

**R.:** O '#' é um wildcard multi-level, um método coringa que permite inscrever-se em todos os tópicos disponíveis. Isso pode ser perigoso, pois pode violar a confidencialidade das mensagens.

4. Sem autenticação (repare que a variável allow_anonymous está como true), como a parte de confidencialidade pode ser violada?

**R.:** Qualquer pessoa pode se conectar ao broker e ler mensagens de qualquer tópico, violando a confidencialidade destas. Além disso a integridade também é violada, pois qualquer pessoa pode publicar mensagens em qualquer tópico.

---

## Perguntas - Desenvolvimento
**Container ID:** 80bba2902865

### 1. Como você faria para violar a confidencialidade?

**R.:** Para violar a confidencialidade, eu poderia me inscrever em tópicos que transitam informações sensíveis, uma vez que o broker não possui uma lista de controle de acesso (ACL) para limitar o acesso a tópicos específicos. Uma vez que obtivesse quaisquer credenciais de acesso, poderia publicar e ler mensagens em tópicos que não deveria ter acesso.

> **Exemplo:**
>
> ```bash
> mosquitto_sub -h -u sheev -p palpatine localhost -t "topic/#" -p 1883
> ```

> [!NOTE]
> Neste caso o usuário sheev detém as credenciais de acesso para este broker, mas não deveria ter acesso ao tópico "topic/#", por exemplo.
> Uma vez que essa credencial fosse obtida por um usuário malicioso, seria possível violar a confidencialidade das mensagens.

### 2. Como você faria para garantir a integridade do broker MQTT?

**R.:** Para garantir a integridade dos dados além de credencias de acesso, cria uma lista de controle de acesso (ACL) para tópicos específicos, de forma a garantir que apenas usuários autorizados possam publicar mensagens em tópicos nestes evitando o compromentimento da integridade dos dados.

### 3. Como você faria para violar o pilar de disponibilidade?

**R.:** Para violar o pilar de disponibilidade da triade de segurança, tendo em vista a permissão de escrita no arquivo de configuração do broker `- ./config:/mosquitto/config:rw`, uma vez que um usuário malicioso consiga acesso root dentro do container explorando alguma vulnerabilidade do serviço, como o mount dos volumes reflete nos arquivos do host, seria possível realizar alterações que comprometessem a disponibilidade, seja por sobrescrever o arquivo de usuários permitidos, tornar o acesso ao broker público fazendo alterando o parâmetro `allow_anonymous` para `true` podendo realizar um ataque de negação de serviço (DoS) com o envio massivo de mensagens, apagar os arquivos de armazenamento de dados e logs ou trocar as portas de acesso do broker. 

Tendo esse quesito em vista, um contramedida é alterar as configurações do mount de volumes permitindo apenas leitura, ou seja, `- ./config:/mosquitto/config:ro` e alterando a permissão dos arquivos de armazenamento de dados e logs para escrita apenas, `- ./data:/mosquitto/data:ro` e `- ./log:/mosquitto/log:ro`. 

Além disso seria interessante criar perfis de segurança para o container, utilizando o SELinux ou AppArmor, para limitar o acesso do container ao host.


### Demontração
Para a demonstração havia elaborado um pequeno teste de carga utilizando threads em Python para publicar mensagens em um tópico específico, porém, ao tentar realizar o teste, não obtive sucesso, 
