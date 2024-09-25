# Appartment rent telegram bot

## Introduction

Telegram bot to rent an appartment


## Get started

### Generate `.env` file

```bash
cp .template-env .env
```

### Configure bot token
1. Create telegram bot with BotFather
2. Change TELEGRAM_BOT_TOKEN variable in .env with new bot token

### Run application

Run docker-compose:
```bash
docker-compose -f docker-compose.local.yaml up --build -d
```
