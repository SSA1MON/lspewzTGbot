# Телеграм бот для подсчета заработной платы ПК мастера

<p align="center"><img src="https://i.imgur.com/Mp6DYhC.png" width="400" alt="lspewz Logo"></p>
<p align="center">
<img src="https://img.shields.io/github/repo-size/SSA1MON/lspewzTgbot?label=size" alt="repo-size">
<img src="https://img.shields.io/github/issues-raw/SSA1MON/lspewzTGbot" alt="open-issues">
<img src="https://img.shields.io/github/languages/top/SSA1MON/lspewzTGbot" alt="language">
<img src="https://img.shields.io/github/last-commit/SSA1MON/lspewzTGbot" alt="commits">
</p>

## Описание
Этот бот позволяет вносить в локальную базу данных суммы полученные на заявках у клиентов и считает чистый процент 
своих доходов в зависимости от категории заявки.

Для просмотра либо редактирования базы данных можно использовать программу [SQLiteStudio](https://sqlitestudio.pl/).

По всем вопросам можно обращаться к создателю идеи и разработчику бота в [telegram](https://t.me/lspewz).

## Как запустить
Нужно [создать бота](https://habr.com/ru/post/262247/) и получить **токен** у отца всех ботов — 
[BotFather](https://t.me/BotFather).

Прописываем свой токен в файл config.py:
```
TOKEN = "Telegram API Token"
```

Осталось установить дополнительную библиотеку и можно запускать!
```
pip3 install pytelegrambotapi
python3 bot.py
```
