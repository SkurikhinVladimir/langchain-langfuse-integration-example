# Langfuse Demo

Демонстрационный проект локальной (self-hosted) интеграции LangChain с Langfuse с использованием LangServe.

---

## Быстрый старт

```bash
# Запуск Langfuse и всех зависимостей
docker-compose -f docker-compose.langfuse.yml up -d

# Запуск приложения
docker-compose -f docker-compose.app.yml up --build -d
```

---

Все запросы можно посмотреть в Langfuse UI:

🌐 Web интерфейс: http://localhost:3000

## Как добавить трейсинг в свои runnable

Чтобы ваши кастомные runnable автоматически логировались в Langfuse, просто наследуйтесь от `BaseTraceableRunnable` и реализуйте нужную логику в методе `_run` (или `_arun` для асинхронных задач). Всё — дальше используйте `invoke` или `ainvoke`, и трейсинг будет работать сам по себе.

## 🔗 Дополнительная информация

- [Документация по Headless Initialization](https://langfuse.com/self-hosting/headless-initialization)
- [Официальный репозиторий Langfuse](https://github.com/langfuse/langfuse)
- [Langfuse cookbook](https://github.com/langfuse/langfuse-docs/tree/main/cookbook)
