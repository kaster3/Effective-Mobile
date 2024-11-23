Выполненое тестовое задание компании Effective-Mobile по созданию WEB приложения с основным CRUD функционалом.

Стек: FastAPI, PostgreSQL, SQLAlchemy, Alembic, Redis, Docker, Pytest, Asyncio

Что сделал:
1) Реализауия по заданию основных CRUD ручек модели Book
3) Кэширование получения всех книг
4) Unit тестирование и Интеграционное через pytest, а также с помощью библиотеки syrupy
5) Контейнеризация
6) Обработка ошибок
7) Внедрение зависимосте

Слои приложения:
1) Handler - Принимаем запрос от пользователя и возвращаем его, дергая Service слой
2) Service layer - Содержит основную бизнес логику и взаимодействует с классами Repository/CacheRepository
3) Repository - Выполняет СRUD операции, промежуточный слой между БД и Бизнес логикой
4) ORM model
