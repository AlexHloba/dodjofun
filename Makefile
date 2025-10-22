.PHONY: build up migrate test

build:
	docker compose build

up:
	docker compose up --build

migrate:
	docker compose run --rm web alembic upgrade head

test:
	docker compose run --rm web pytest -q
