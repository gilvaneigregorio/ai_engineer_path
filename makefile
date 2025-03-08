.PHONY: help build run stop destroy sh logs lint add

# HELP COMMANDS
help:
	@echo ''
	@echo 'List of avaliable commands:'
	@echo '- make build - Build the docker containers'
	@echo '- make run - Run the docker containers'
	@echo '- make stop - Stop the docker containers'
	@echo '- make destroy - Destroy the docker containers'
	@echo '- make sh - Access the docker container'
	@echo '- make logs - Show the docker container logs'
	@echo '- make lint - Run the linters'
	@echo '- make install package=<package_name> - install a package to the project'
	@echo '- make run load_recipes.py - Run the load_recipes.py script'
	@echo ''

APP_NAME = app
EXEC = docker compose exec $(APP_NAME)

build:
	docker-compose build --no-cache
	docker-compose up

run:
	docker-compose up

stop:
	docker-compose stop

destroy:
	docker-compose down

sh: 
	@ $(EXEC) sh

logs:
	docker-compose logs -f $(APP_NAME)

lint:
	ruff check --fix . && ruff format .

add:
	uv add $(package)

load-recipes:
	$(EXEC) python src/load_recipes.py 