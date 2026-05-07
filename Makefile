.DEFAULT_GOAL := help

.PHONY: help up down logs restart export import test clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

up:  ## Start Node-RED + Mosquitto
	docker compose up -d

down:  ## Stop everything
	docker compose down

logs:  ## Tail container logs
	docker compose logs -f

restart:  ## Restart Node-RED only
	docker compose restart node-red

export:  ## Pull live flows out of the container into git
	./scripts/export-flows.sh

import:  ## Push local flows.json into the container
	./scripts/import-flows.sh

test:  ## Run the JSON validation tests
	pytest

clean:  ## Stop and remove volumes (DESTRUCTIVE)
	docker compose down -v
	rm -rf mosquitto/data mosquitto/log
