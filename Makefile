build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

migrations:
	docker-compose run --rm web python manage.py makemigrations
	docker-compose run --rm web python manage.py migrate

superuser:
	docker-compose run --rm web python manage.py createsuperuser

shell:
	docker-compose run --rm web python manage.py shell

init-project:
	docker-compose run --rm web django-admin startproject config .
