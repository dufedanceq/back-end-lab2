# Лабораторна робота №3. Аутентифікація та JWT

**Виконав:** Никифоров Артем Михайлович  
**Група:** ІМ-34

REST API для обліку витрат з підтримкою валют, бази даних PostgreSQL та JWT-авторизації.

## Інсталяція та запуск локально

### 1. Клонування репозиторію

```bash
git clone https://github.com/dufedanceq/back-end-lab1
cd expense-tracker-api
```

### 2. Налаштування віртуального середовища
Створіть та активуйте venv:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 4. Запуск Бази Даних (Docker)
```bash
docker-compose up -d
```

### 5. Міграції (Створення таблиць)
```bash
flask db upgrade
```

### 6. Запуск сервера
```bash
python app.py
```
Сервер запуститься за адресою: `http://127.0.0.1:5000`

## Ендпоінти

###  Авторизація (Auth)
*   `POST /register` — Реєстрація користувача (поля: `name`, `password`, `default_currency_id`).
*   `POST /login` — Вхід (повертає `access_token`).

###  Валюта (Currency)
*   `GET /currency` — Отримати список валют.
*   `POST /currency` — Створити нову валюту (наприклад, USD).

###  Категорії (Categories) — *Потрібен токен*
*   `GET /category` — Список категорій.
*   `POST /category` — Створити категорію.

###  Витрати (Records) — *Потрібен токен*
*   `POST /record` — Створити запис (поля: `user_id`, `category_id`, `amount`, `currency_id`).
*   `GET /record` — Отримати записи (фільтри: `?user_id=...&category_id=...`).

## Деплой

Проект успішно задеплоєно на платформі **Render**:
*   **Live URL:** [https://back-end-lab2-bdjl.onrender.com](https://back-end-lab2-bdjl.onrender.com)
*   **Swagger Docs:** [https://back-end-lab2-bdjl.onrender.com/swagger-ui](https://back-end-lab2-bdjl.onrender.com/swagger-ui)
