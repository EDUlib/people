.DEFAULT_GOAL := test

.PHONY: help clean piptools requirements ci_requirements dev_requirements \
        validation_requirements doc_requirementsprod_requirements static shell \
        test coverage isort_check isort style lint quality pii_check validate \
        migrate html_coverage upgrade extract_translation dummy_translations \
        compile_translations fake_translations  pull_translations \
        push_translations start-devstack open-devstack  pkg-devstack \
        detect_changed_source_translations validate_translations

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

# Generates a help message. Borrowed from https://github.com/pydanny/cookiecutter-djangopackage.
help: ## display this help message
	@echo "Please use \`make <target>\` where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean: ## delete generated byte code and coverage reports
	find . -name '*.pyc' -delete
	coverage erase
	rm -rf assets
	rm -rf pii_report

piptools: ## install pinned version of pip-compile and pip-sync
	pip install -r requirements/pip-tools.txt

requirements: piptools dev_requirements ## sync to default requirements

ci_requirements: validation_requirements ## sync to requirements needed for CI checks

dev_requirements: ## sync to requirements for local development
	pip-sync -q requirements/dev.txt

validation_requirements: ## sync to requirements for testing & code quality checking
	pip-sync -q requirements/validation.txt

doc_requirements:
	pip-sync -q requirements/doc.txt

prod_requirements: ## install requirements for production
	pip-sync -q requirements/production.txt

static: ## generate static files
	python manage.py collectstatic --noinput

shell: ## run Django shell
	python manage.py shell

test: clean ## run tests and generate coverage report
	pytest

# To be run from CI context
coverage: clean
	pytest --cov-report html
	$(BROWSER) htmlcov/index.html

isort_check: ## check that isort has been run
	isort --check-only -rc people/

isort: ## run isort to sort imports in all Python files
	isort --recursive --atomic people/

style: ## run Python style checker
	pylint --rcfile=pylintrc people *.py

lint: ## run Python code linting
	pylint --rcfile=pylintrc people *.py

quality: style isort_check lint ## check code style and import sorting, then lint

pii_check: ## check for PII annotations on all Django models
	DJANGO_SETTINGS_MODULE=people.settings.test \
	code_annotations django_find_annotations --config_file .pii_annotations.yml --lint --report --coverage

validate: test quality pii_check ## run tests, quality, and PII annotation checks

migrate: ## apply database migrations
	python manage.py migrate

html_coverage: ## generate and view HTML coverage report
	coverage html && open htmlcov/index.html

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: piptools ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	# Make sure to compile files after any other files they include!
	pip-compile --upgrade -o requirements/pip-tools.txt requirements/pip-tools.in
	pip-compile --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --upgrade -o requirements/test.txt requirements/test.in
	pip-compile --upgrade -o requirements/doc.txt requirements/doc.in
	pip-compile --upgrade -o requirements/quality.txt requirements/quality.in
	pip-compile --upgrade -o requirements/validation.txt requirements/validation.in
	pip-compile --upgrade -o requirements/dev.txt requirements/dev.in
	pip-compile --upgrade -o requirements/production.txt requirements/production.in

extract_translations: ## extract strings to be translated, outputting .mo files
	python manage.py makemessages -l en -v1 -d django
	python manage.py makemessages -l en -v1 -d djangojs

dummy_translations: ## generate dummy translation (.po) files
	cd people && i18n_tool dummy

compile_translations: # compile translation files, outputting .po files for each supported language
	python manage.py compilemessages

fake_translations: ## generate and compile dummy translation files

pull_translations: ## pull translations from Transifex
	tx pull -af --mode reviewed

push_translations: ## push source translation files (.po) from Transifex
	tx push -s

start-devstack: ## run a local development copy of the server
	docker-compose --x-networking up

open-devstack: ## open a shell on the server started by start-devstack
	docker exec -it people /edx/app/people/devstack.sh open

pkg-devstack: ## build the people image from the latest configuration and code
	docker build -t people:latest -f docker/build/people/Dockerfile git://github.com/edx/configuration

detect_changed_source_translations: ## check if translation files are up-to-date
	cd people && i18n_tool changed

validate_translations: fake_translations detect_changed_source_translations ## install fake translations and check if translation files are up-to-date

# Docker commands below

# dev.provision:
# 	bash ./provision-people.sh

# dev.init: dev.up dev.migrate

# dev.makemigrations:
# 	docker exec -it people.people bash -c 'cd /edx/app/people/people && python3 manage.py makemigrations'

# dev.migrate: # Migrates databases. Application and DB server must be up for this to work.
# 	docker exec -it people.people bash -c 'cd /edx/app/people/people && make migrate'

# dev.up: # Starts all containers
# 	docker-compose up -d --build

# dev.down: # Kills containers and all of their data that isn't in volumes
# 	docker-compose down

# dev.destroy: dev.down #Kills containers and destroys volumes. If you get an error after running this, also run: docker volume rm portal-designer_designer_mysql
# 	docker volume rm enterprise-catalog_enterprise_catalog_mysql

# dev.stop: # Stops containers so they can be restarted
# 	docker-compose stop

# %-shell: ## Run a shell on the specified service container
# 	docker exec -it enterprise.catalog.$* bash

# %-logs: ## View the logs of the specified service container
# 	docker-compose logs -f --tail=500 $*

# attach:
# 	docker attach enterprise.catalog.app

# docker_build:
# 	docker build . --target app -t "openedx/enterprise-catalog:latest"
# 	docker build . --target newrelic -t "openedx/enterprise-catalog:latest-newrelic"

# travis_docker_auth:
# 	echo "$$DOCKER_PASSWORD" | docker login -u "$$DOCKER_USERNAME" --password-stdin

# travis_docker_tag: docker_build
# 	docker build . --target app -t "openedx/enterprise-catalog:$$TRAVIS_COMMIT"
# 	docker build . --target newrelic -t "openedx/enterprise-catalog:$$TRAVIS_COMMIT-newrelic"

# travis_docker_push: travis_docker_tag travis_docker_auth ## push to docker hub
# 	docker push "openedx/enterprise-catalog:latest"
# 	docker push "openedx/enterprise-catalog:$$TRAVIS_COMMIT"
# 	docker push "openedx/enterprise-catalog:latest-newrelic"
# 	docker push "openedx/enterprise-catalog:$$TRAVIS_COMMIT-newrelic"