COMPOSE = docker compose

.PHONY: up down restart logs status

up:
	$(COMPOSE) up -d db

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f db

status:
	$(COMPOSE) ps
