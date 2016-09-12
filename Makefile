SHELL = /bin/bash
.PHONY: dev prod clean

prod:
	cd Docker/ && docker-compose up -d

dev:
# rabbitmq-dev exposes ip and port for management
# producer-dev runs producer_test.py -> check ./log/consumer.log \
# for messages send by producer and saved by consumer
	cd Docker/ && docker-compose -f docker-compose-dev.yml up

clean:
	cd Docker/ && docker-compose down
ifneq ($(shell docker volume ls -f dangling=true -q),)
	docker volume rm $$(docker volume ls -f dangling=true -q)
endif
