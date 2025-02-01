# Flask Microsoft OAuth2 Project

Этот проект представляет собой веб-приложение, разработанное с использованием Flask, которое позволяет пользователям аутентифицироваться с помощью учетных записей Microsoft через OAuth2. Приложение использует Microsoft Graph API для получения информации о пользователе после успешной аутентификации.

## Установка

### Предварительные требования

- Python 3.6 или выше
- Poetry (менеджер пакетов для Python)

### Клонирование репозитория

```
git clone https://github.com/yufilchakov/app
cd app
```

Установка зависимостей

Убедитесь, что у вас установлен Poetry. Если он не установлен, вы можете установить его, следуя официальной документации Poetry.

После установки Poetry выполните следующую команду для установки зависимостей:
```
poetry install
```

Настройка переменных окружения

Создайте файл .env.sample в корне проекта и добавьте следующие переменные:

OAUTH_APP_ID=ваш_client_id

OAUTH_APP_PASSWORD=ваш_client_secret

OAUTH_AUTHORITY=https://login.microsoftonline.com/{tenant_id}/

OAUTH_AUTHORIZE_ENDPOINT=/oauth2/v2.0/authorize

OAUTH_TOKEN_ENDPOINT=/oauth2/v2.0/token

OAUTH_REDIRECT_URI=http://localhost:3000/callback

OAUTH_SCOPES=openid profile email

SECRET_KEY=ваш_секретный_ключ

Замените ваш_client_id, ваш_client_secret, {tenant_id} и ваш_секретный_ключ на соответствующие значения.

Запуск приложения

Запустите приложение с помощью следующей команды:

poetry run python app.py

Приложение будет доступно по адресу http://localhost:3000