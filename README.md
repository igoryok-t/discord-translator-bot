# Discord Translator Bot

Автоматически переводит сообщения с английского на русский в указанном канале.

## Файлы
- `main.py` — основной код бота
- `requirements.txt` — зависимости Python
- `Dockerfile` — для деплоя на Railway/Render
- `.env.example` — пример переменных окружения

## Локальный запуск
```bash
cd /home/hermes/discord/discord-translator-bot
cp .env.example .env
# отредактируй .env, вставь свой токен
pip install -r requirements.txt
python main.py
```

## Деплой на Railway
1. Создай репозиторий на GitHub с этими файлами
2. На Railway: New Project → Deploy from GitHub repo
3. Добавь переменные окружения (Variables):
   - `DISCORD_TOKEN` — токен бота из Discord Developer Portal
   - `SOURCE_CHANNEL_ID` — ID канала-источника (1566385711588966442)
   - `TARGET_CHANNEL_ID` — ID канала для перевода (может быть тем же)
   - `SOURCE_LANG=en`
   - `TARGET_LANG=ru`
4. Deploy

## Создание бота в Discord
1. https://discord.com/developers/applications → New Application
2. Bot → Reset Token → скопируй токен
3. Privileged Gateway Intents → включи Message Content Intent
4. OAuth2 → URL Generator → scopes: bot, applications.commands
   Permissions: Read Messages, Send Messages, Embed Links, Read Message History
5. Открой сгенерированный URL → добавь бота на сервер