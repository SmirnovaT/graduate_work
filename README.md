# Дипломная работа: "Голосовой ассистент"

## [Ссылка на репозиторий](https://github.com/Cobolock/graduate_work)

## Запуск проекта

Необходимо создать .env по шаблону .env_example в сервисах:

[Голосовой ассистент](./assistant)

[API для онлайн-кинотеатра](./movies/fastapi-solutions)

### Запуск приложения в контейнере из корня проекта

```
docker-compose --profile all up --build
```

### Работа с профилями Docker

Для запуска только контейнеров API кинотеатра:

```
docker compose --profile movies up -d
```

Для запуска конкретного контейнера нужно указать и профиль, в котором этот контейнер присутствует, и имя контейнера.
Например, для запуска Redis голосового ассистента:

```
docker compose --profile assistant up -d assistant_cache
```

Если нужно открыть порты контейнеров в целях разработки, выполните:

```
docker-compose -f docker-compose.yml --profile all -f docker-compose.prod.yml up -d
```

### Вопросы к голосовому ассистенту:

1. Какой рейтинг у фильма X?
2. Расскажи о фильме Х (О чем фильм Х? Про что фильм Х?)
3. Какой жанр у фильма Х?
4. Кто актер фильма X? (Кто снимался в фильме Х?)
5. Кто автор фильма Х?
6. Кто режиссер фильма Х?

#### Создание и тестирование навыка Маруси:

1. Необходимо создать [приложение](https://vk.com/editapp?act=create)
   по [инструкции](https://dev.vk.com/ru/marusia/getting-started?ref=old_portal)

2. Тестирование навыка по [ссылке](https://skill-debugger.marusia.mail.ru/)

3. Указать Webhook URL навыка: http://localhost:8001/api/v1/assistant/vk

### Создание и тестирование навыка Алисы

1. Необходимо зарегистрировать приложение в [Yandex OAuth](https://oauth.yandex.ru/)
2. Также создать Навык в консоли [Яндекс.Диалогов](https://dialogs.yandex.ru/developer)
3. В Навыке указать все требуемые данные, в том числе - адрес webhook с обязательно актуальными SSL-сертификатами, в нашем случае - https://(адрес_сервера)/api/v1/assistant/yandex
4. В Навыке->Связка аккаунтов указать полученную в Yandex OAuth пару ClientID / Client Secret в качестве "Идентификатор приложения" / "Секрет приложения" соответственно
5. В Навыке->Связка аккаунтов указать URL: авторизации - https://oauth.yandex.com/authorize , получения и обновления токена - https://oauth.yandex.com/token
6. Указать тип навыка "Приватный"
7. В Навыке->Тестирование начать писать запросы к вебхуку и наблюдать ответы от сервиса.

### Настройка ГигаЧата от Сбер

1. Зарегистрироваться в Студии и [создать свой проект](ttps://developers.sber.ru/studio/)
2. Сгенерировать Client Secret
3. Указать в [.env модуля ассистента](/assistant/.env) Auth Data и Client Secret, а также выбранную модель (GigaChat для бесплатных аккаунтов) и Scope (GIGACHAT_API_PERS для частных лиц)

###  Локальный запуск тестов:
```
1. Из корня проекта: docker-compose up --build
2. cd assistant/src/
3. poetry run pytest
```




