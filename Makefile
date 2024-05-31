.PHONY: dev
dev:
	FLASK_APP=./app/api.py FLASK_ENV=Dev flask run

test:
	PYTHONPATH=. pytest -s

black:
	black --target-version=py39 .

db_prepare:
	FLASK_APP=./app/api.py flask db stamp head && flask db migrate

db_prepare_stg:
	FLASK_APP=./app/api.py FLASK_ENV=Stg flask db stamp head && flask db migrate

migrate_up:
	FLASK_APP=./app/api.py flask db upgrade

migrate_up_stg:
	FLASK_APP=./app/api.py FLASK_ENV=Stg flask db upgrade

migrate_down:
	FLASK_APP=./app/api.py flask db downgrade

migrate:
	FLASK_APP=./app/api.py flask db migrate