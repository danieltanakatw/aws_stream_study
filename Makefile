.PHONY: run_services
run_services: 
	docker-compose build
	docker-compose up -d

.PHONY: stop_all
stop_all:
	docker-compose down
