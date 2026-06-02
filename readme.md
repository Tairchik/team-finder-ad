# TeamFinder

Платформа для поиска команды на pet-проекты. Разработчики, дизайнеры и другие специалисты могут размещать идеи проектов, находить единомышленников и откликаться на опубликованные предложения.

## Функциональность

- Регистрация и аутентификация по email
- Создание и редактирование проектов
- Участие в проектах других пользователей
- Добавление проектов в избранное
- Профили пользователей с контактной информацией
- Фильтрация пользователей по связям с проектами
- Автоматическая генерация аватара при регистрации

## Стек технологий

- Python 3.12
- Django 5.2
- PostgreSQL 16
- Pillow
- Docker / Docker Compose

## Развёртывание проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Tairchik/team-finder-ad.git
cd team-finder-ad
```

### 2. Создать виртуальное окружение и установить зависимости

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Создать файл `.env`

```bash
cp .env_example .env
```

Заполнить `.env`:

| Переменная | Описание |
|------------|----------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django |
| `DJANGO_DEBUG` | Режим отладки (`True` для разработки) |
| `POSTGRES_DB` | Имя базы данных |
| `POSTGRES_USER` | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL |
| `POSTGRES_HOST` | Хост БД (обычно `localhost`) |
| `POSTGRES_PORT` | Порт БД (обычно `5432`) |

Сгенерировать `DJANGO_SECRET_KEY` можно так:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Запустить PostgreSQL через Docker

```bash
docker compose up -d
```

### 5. Применить миграции

```bash
python manage.py migrate
```

### 6. Создать суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер

```bash
python manage.py runserver
```

Проект доступен по адресу [http://localhost:8000](http://localhost:8000)

## Автор

**Таир**, студент НГТУ  
📧 gidrolaz.tr@gmail.com  
🐙 [github.com/Tairchik](https://github.com/Tairchik)
