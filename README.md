# Индивидуальный телеграм-бот для подсчета заработной платы компьютерного мастера

<p align="center"><img src="https://i.imgur.com/Mp6DYhC.png" width="400" alt="lspewz Logo"></p>
<p align="center">
<img src="https://img.shields.io/github/repo-size/SSA1MON/lspewzTgbot?label=size" alt="repo-size">
<img src="https://img.shields.io/github/issues-raw/SSA1MON/lspewzTGbot" alt="open-issues">
<img src="https://img.shields.io/github/languages/top/SSA1MON/lspewzTGbot" alt="language">
<img src="https://img.shields.io/github/last-commit/SSA1MON/lspewzTGbot" alt="commits">
</p>

## Описание
Бот создает и вносит в локальную базу данных суммы полученные на заявках у клиентов, считает чистые 
доходы в зависимости от категории заявки, высчитывает средний чек.

Для просмотра и редактирования базы данных можно использовать программу [SQLiteStudio](https://sqlitestudio.pl/).

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
