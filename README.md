# Wellness Multi-agent System

## Setup

Generate

Add mas user to the kafka cluster then retrieve the api key and secret for the user. These need to go in 
```bash
$ bin/kafka-configs.sh --bootstrap-server localhost:9092 --alter --add-config 'SCRAM-SHA-256=[password=<password>]' --entity-type users --entity-name <username>

$ bin/kafka-configs.sh --bootstrap-server localhost:9092 --describe --entity-type users --entity-name <username>
```


## Run
```bash
docker-compose up
```

```bash
$ docker exec mas_essentials curl -X POST -H "Content-Type: application/json" -d '{"sender":"@joan", "message":"wakeup"}' http://${MAS_ESSENTIALS_HOST}:${PORT}/api/messages
```