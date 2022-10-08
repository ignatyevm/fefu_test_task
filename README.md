## Стек
* Python 3.10
* FastAPI
* SQLAlchemy

## Запуск
```bash
git clone https://github.com/ignatyevm/fefu_test_task fefu_test_task
cd fefu_test_task
docker-compose up
```
Эндпоинт сервиса ```http://localhost:8000/```


## Тесты
Запуск тестов 
```bash
docker-compose up api-service-tests-runner
```
Отчет по тестам в ```tests_report.html```

## Документация
https://app.swaggerhub.com/apis-docs/polyndrom/FefuTestTaskAPI/1.0.0
