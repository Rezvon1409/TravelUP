# 🌍 TravelUp Backend API

Backend API для тревел-платформы. Позволяет управлять пользователями, бронированиями, отзывами и платежами.

---

## 🛠 Технологии

- Python 3.11+
- FastAPI
- SQLAlchemy (sync)
- Alembic
- SQLite (dev) / PostgreSQL (prod)
- Pydantic v2
- JWT (access / refresh)
- Uvicorn

---

## 📂 Структура проекта
```
TravelUp/
├── api/               # Эндпоинты
├── core/              # Конфигурация, безопасность, права
├── models/            # Модели базы данных
├── schemas/           # Pydantic схемы
├── services/          # Бизнес-логика
├── alembic/           # Миграции
├── main.py            # Точка входа
├── database.py        # Подключение к БД
├── seeds.py           # Начальные данные
├── .env               # Переменные окружения
└── requirements.txt   # Зависимости
```

---

## ⚙️ Установка

### 1. Клонировать репозиторий
```bash
git clone https://github.com/username/TravelUp-Backend.git
cd TravelUp-Backend
```

### 2. Создать виртуальное окружение
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Создать `.env` файл
```
DATABASE_URL=sqlite:///./TravelUp.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5. Применить миграции
```bash
alembic upgrade head
```

### 6. Заполнить базу данных
```bash
python seeds.py
```

### 7. Запустить сервер
```bash
python main.py
```

---

## 📡 API Эндпоинты

### 🔐 Auth
| Метод | URL | Описание | Доступ |
|---|---|---|---|
| POST | `/auth/register` | Регистрация | Public |
| POST | `/auth/login` | Вход, получить токен | Public |
| POST | `/auth/refresh` | Обновить токен | Public |
| POST | `/auth/logout` | Выход | Public |

### 👤 Profile
| Метод | URL | Описание | Доступ |
|---|---|---|---|
| GET | `/profile` | Просмотр профиля | User |
| PATCH | `/profile/update` | Обновить профиль | User |
| PATCH | `/profile/theme` | Изменить тему | User |
| PATCH | `/profile/admin/update/{user_id}` | Обновить профиль пользователя | Admin |

### 🌏 Destinations
| Метод | URL | Описание | Доступ |
|---|---|---|---|
| GET | `/destinations` | Все места (с фильтром) | Public |
| GET | `/destinations/{id}` | Одно место | Public |
| POST | `/destinations` | Создать место | Admin |
| PUT | `/destinations/{id}` | Обновить место | Admin |
| DELETE | `/destinations/{id}` | Удалить место | Admin |

### 📅 Bookings
| Метод | URL | Описание | Доступ |
|---|---|---|---|
| POST | `/bookings` | Создать бронь | User |
| GET | `/bookings/my` | Мои брони | User |
| GET | `/bookings` | Все брони | Admin |
| PATCH | `/bookings/{id}/cancel` | Отменить бронь | Owner |
| PATCH | `/bookings/{id}/status` | Изменить статус: `pending` `confirmed` `cancelled` | Admin |

### ⭐ Reviews
| Метод | URL | Описание | Доступ |
|---|---|---|---|
| POST | `/reviews` | Оставить отзыв (нужна confirmed бронь) | User |
| GET | `/destinations/{id}/reviews` | Отзывы места | Public |
| PUT | `/reviews/{id}` | Редактировать отзыв | Owner |
| DELETE | `/reviews/{id}` | Удалить отзыв | Owner/Admin |

### 💳 Payments
| Метод | URL | Описание | Доступ |
|---|---|---|---|
| POST | `/payments` | Оплатить | Owner |
| GET | `/payments/my` | Мои платежи | Owner |
| GET | `/payments` | Все платежи | Admin |

### 🔧 Admin
| Метод | URL | Описание | Доступ |
|---|---|---|---|
| GET | `/admin/users` | Все пользователи | Admin |
| GET | `/admin/users/{user_id}` | Один пользователь | Admin |
| GET | `/admin/roles` | Все роли | Admin |
| GET | `/admin/permissions` | Все права | Admin |
| POST | `/admin/set-role` | Назначить роль | Admin |
| POST | `/admin/set-permissions` | Назначить права | Admin |
| POST | `/admin/make-admin` | Сделать админом | Admin |
| DELETE | `/admin/remove-role` | Удалить роль | Admin |
| DELETE | `/admin/remove-permissions` | Удалить права | Admin |
| DELETE | `/admin/users/{user_id}` | Удалить пользователя | Admin |

---

## 🔐 Авторизация

1. `POST /auth/register` — зарегистрируйтесь
2. `POST /auth/login` — получите токен
3. В Swagger нажмите **Authorize** и введите токен
4. Все защищённые эндпоинты теперь доступны

---

## 👑 Первый Admin

После запуска `seeds.py` автоматически создаётся:
- **username:** `admin`
- **password:** `admin123`

---

## 📖 Документация

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 🗄 Фильтры для Destinations
```
GET /destinations?city=Paris
GET /destinations?country=France
GET /destinations?rating=4.0
GET /destinations?city=London&rating=4.5
```

---

## ⚠️ Статусы

### Booking
| Статус | Описание |
|---|---|
| `pending` | В ожидании |
| `confirmed` | Подтверждено |
| `cancelled` | Отменено |

### Payment
| Статус | Описание |
|---|---|
| `pending` | В ожидании |
| `paid` | Оплачено |
| `failed` | Ошибка оплаты |