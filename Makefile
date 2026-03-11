.PHONY: test test-headed install docker-up docker-down

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
