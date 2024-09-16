### ASYNC API

#### Асинхронный API для кинотеатра

[ССЫЛКА НА РЕПОЗИТОРИЙ](https://github.com/SmirnovaT/Async_API_sprint_2)

____________________________________________________________________________
Как запустить проект и проверить его работу
____________________________________________________________________________
 
Необходимо заполнить .env по шаблону .env_example

Запуск приложения с docker compose
```
cd tests/functional
cp .env_test_example .env
```
```
docker-compose up --build
or
docker-compose up --build -d
```
____________________________________________________________________________
Запуск приложения для локальной разработки
____________________________________________________________________________
```
1. cd fastapi-solutions

2. cp .env_example .env

3. python3.12 -m venv venv

4. source venv/bin/activate

5. pip3 install poetry

6. poetry install (or python -m poetry install)

7. docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" krissmelikova/awesome_repository:v1

8. docker run -p 6379:6379 redis:7.2.4-alpine
 
9. gunicorn src.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

10. cd tests/functional

11. cp .env_test_example .env

12. python3.12 -m venv venv

13. source venv/bin/activate

14. pip3 install poetry

15. poetry install (or python -m poetry install)

16. python3 -m pytest
```

____________________________________________________________________________
Тестирование
____________________________________________________________________________

Локальное тестирование

```
1. docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" krissmelikova/awesome_repository:v1

2. docker run -p 6379:6379 redis:7.2.4-alpine

3. (from fastapi-solutions directory) gunicorn src.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

4. cd tests/functional
```

Запустить все тесты
```
python3 -m pytest
```
Запустить все тесты в конкретном файле
```
python3 -m pytest src/<file with tests>
```

Запустить один конкретный тест
```
python3 -m pytest -k <test_name>
```

____________________________________________________________________________

Добработки по ETL

[Added ETL for persons](https://github.com/KrisMelikova/new_admin_panel_sprint_3/commit/fce4ba8595ed0ed0b20773bcc14cacd19a37e9ad)

[Added ETL for genres](https://github.com/KrisMelikova/new_admin_panel_sprint_3/commit/d6e4d749a94bcf7225e14fbbd33646c3c6999d58)
____________________________________________________________________________