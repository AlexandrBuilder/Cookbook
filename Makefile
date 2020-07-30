up:
	docker-compose up -d --build

down:
	docker-compose down

update-db:
	docker-compose exec web alembic upgrade head

bash:
	docker-compose exec web bash