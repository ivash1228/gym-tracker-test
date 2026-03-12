.PHONY: test test-headed install docker-up docker-down fetch-spec parse-spec generate-tests generate-exploratory test-api test-exploratory

fetch-spec:
	curl -s http://localhost:8080/v3/api-docs -o api/spec/openapi.json

parse-spec:
	python -m api.generator.parse_spec

generate-tests:
	python -m api.generator.generate_tests

generate-exploratory:
	python -m api.generator.generate_exploratory

test-api:
	pytest api/ -v

test-exploratory:
	pytest api/tests/test_client_controller_exploratory.py -v

install:
	pip install -r requirements.txt
	playwright install chromium

docker-up:
	docker compose up -d

docker-down:
	docker compose down

test:
	cd ui && pytest -v

test-headed:
	cd ui && HEADED=true pytest -v
