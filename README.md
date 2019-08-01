# Support Bot

Вопросно-ответный бот для ВКонтакте и Telegram на базе DialogFlow.

DialogFlow – сервис от Google, который позволяет построить вопросно-отвветные системы при помощи обработки естественного языка.

![Пример в Telegram](example_tg.gif)

[Демо ВКонтакте](https://vk.com/im?sel=-184621261) | [Демо в Telegram](https://t.me/verbplay_bot)

## Запуск

Установить зависимости:
```bash
pip install -r requirements.txt
```
или при помощи Pipenv:
```bash
pipenv install
```

Заполнить `.env` файл своими данными по примеру из `.env.example`.

Для корректной работы бота необходимо заполнить вопросы-ответы в DialogFlow. Это можно сделать вручную в интерфейсе DialogFlow.
Или из `JSON` файла, например из `questions_example.json`:

```bash
python import_intents.py questions_example.json
```

Запустить бота в Telegram
```bash
python telegram_bot.py
```


Запустить бота в ВКонтакте
```bash
python vk_bot.py
```