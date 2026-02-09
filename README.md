**Currency Application**

Микросервис для загрузки, хранения и анализа курсов валют Национального Банка РБ.
Позволяет получать курс на конкретную дату, вычислять тренд изменения по сравнению с предыдущим днем и подписывает ответы CRC32 хешем для контроля целостности.

**Инструкция запуска:**

1. Клонируем репозиторий и создаем .env:

```bash
git clone https://github.com/MaslovskiyNikita/currency_application 
cd currency_application
cp .env.example .env
```

2. Поднимаем приложение:
```bash
docker-compose up --build
```
**Документация API**
Swagger UI: http://127.0.0.1:8000/api/docs/

1. Загрузка данных за дату (POST) http://127.0.0.1:8000/api/v1/rates/load/  
Формат: { "date": "2023-10-25" }

2. Получение курса и аналитики (GET) http://127.0.0.1:8000/api/v1/rates/rate/?date=2023-10-25&code=USD 


**Tests**

```bash
docker-compose exec web pytest -v
```

