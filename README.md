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

## Как добавить трейсинг в кастомные runnable

Для автоматического логирования кастомных runnable в Langfuse достаточно унаследовать класс от [`BaseTraceableRunnable`](app/core/base_traceable_runnable.py) и реализовать необходимую логику в методе `_run` (или `_arun` для асинхронных задач). После этого методы `invoke` и `ainvoke` обеспечивают трейсинг выполнения без дополнительной настройки.

## 🔗 Дополнительная информация

- [Документация по Headless Initialization](https://langfuse.com/self-hosting/headless-initialization)
- [Официальный репозиторий Langfuse](https://github.com/langfuse/langfuse)
- [Langfuse cookbook](https://github.com/langfuse/langfuse-docs/tree/main/cookbook)
