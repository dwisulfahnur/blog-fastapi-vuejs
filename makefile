up:
		docker-compose up -d --build

down:
		docker-compose down

down-all:
		docker-compose down -v --remove-orphans

logs:
		docker-compose logs -f

logs-backend:
		docker-compose logs -f backend

test-backend:
		docker-compose exec backend pytest