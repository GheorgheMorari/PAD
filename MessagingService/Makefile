include .env

start_postgres:
	@ echo "Starting postgres database"
	@ docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -d postgres | true