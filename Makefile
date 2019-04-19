PROJECT_NAME=new_poster

# Common

all: run

run:
	@docker-compose up new_poster_app

stop:
	@docker-compose stop

clean:
	@docker-compose down

bash:
	@docker exec -it new_poster bash

# Docs

doc:
	cd docs && make html

# Linters & tests

mypy:
	@docker-compose run --rm $(PROJECT_NAME)_app mypy $(PROJECT_NAME)

lint:
	@docker-compose run --rm $(PROJECT_NAME)_app flake8 $(PROJECT_NAME)

_test:
	# todo: remove no:warnings
	@py.test -p no:warnings --cov

test: lint
	@docker-compose up test
	@docker-compose stop test
# Database

psql:
	@docker exec -it new_poster_postgres psql -U postgres

migrations:
	@docker exec -it new_poster alembic -n alembic:dev revision --autogenerate;

migrate:
	@docker exec -it new_poster alembic -n alembic:dev upgrade head;

run_production:
	@docker-compose -f docker-compose.yml -f docker-compose.production.yml up

adev: wait_resources 
	adev runserver ./new_poster/__main__.py -p 8080
wait_resources:
	python3 -m new_poster.utils.wait_script
