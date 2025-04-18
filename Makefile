.PHONY: up down restart logs test clean

# Start all services
up:
	./run.sh

# Stop all services
down:
	docker-compose down --remove-orphans
	docker-compose -f docker-compose.frontend.yml down --remove-orphans

# Restart all services
restart: down up

# View logs
logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose -f docker-compose.frontend.yml logs -f frontend

logs-all:
	docker-compose logs -f

# Run backend tests
test:
	docker-compose exec backend pytest

# Clean up Docker resources
clean:
	docker-compose down -v --remove-orphans
	docker-compose -f docker-compose.frontend.yml down -v --remove-orphans
	docker system prune -f

# Build services
build:
	docker-compose build
	docker-compose -f docker-compose.frontend.yml build 