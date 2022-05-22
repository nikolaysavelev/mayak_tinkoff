# django-telegram-bot
Sexy Django + python-telegram-bot + Celery + Redis + Postgres + Dokku + GitHub Actions template. Production-ready Telegram bot with database, admin panel and a bunch of useful built-in methods.

[![Sparkline](https://stars.medv.io/ohld/django-telegram-bot.svg)](https://stars.medv.io/ohld/django-telegram-bot)


### Check the example bot that uses the code from Main branch: [t.me/djangotelegrambot](https://t.me/djangotelegrambot)

## Features

* Database: Postgres, Sqlite3, MySQL - you decide!
* Admin panel (thanks to [Django](https://docs.djangoproject.com/en/3.1/intro/tutorial01/))
* Background jobs using [Celery](https://docs.celeryproject.org/en/stable/)
* [Production-ready](https://github.com/ohld/django-telegram-bot/wiki/Production-Deployment-using-Dokku) deployment using [Dokku](https://dokku.com)
* Telegram API usage in pooling or [webhook mode](https://core.telegram.org/bots/api#setwebhook)
* Reverse geocode of user via [ArcGis](https://www.arcgis.com/)
* Export all users in `.csv`
* Native telegram [commands in menu](https://github.com/ohld/django-telegram-bot/blob/main/.github/imgs/bot_commands_example.jpg)

Built-in Telegram bot methods:
* `/broadcast` — send message to all users (admin command)
* `/export_users` — bot sends you info about your users in .csv file (admin command)
* `/stats` — show basic bot stats 
* `/ask_for_location` — log user location when received and reverse geocode it to get country, city, etc.

Check out our [Wiki](https://github.com/ohld/django-telegram-bot/wiki) for more info.

# How to run

## Run locally using docker-compose

If you like docker-compose you can check [full instructions in our Wiki](https://github.com/ohld/django-telegram-bot/wiki/Run-locally-using-Docker-compose).

## Deploy to Production 

Read Wiki page on how to [deploy production-ready](https://github.com/ohld/django-telegram-bot/wiki/Production-Deployment-using-Dokku) scalable Telegram bot using Dokku.

----
