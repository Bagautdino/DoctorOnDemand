[![Docker Build](https://github.com/Bagautdino/DoctorOnDemand/actions/workflows/docker-build.yml/badge.svg)](https://github.com/Bagautdino/DoctorOnDemand/actions/workflows/docker-build.yml)
[![Python Security Check](https://github.com/Bagautdino/DoctorOnDemand/actions/workflows/python-security.yml/badge.svg)](https://github.com/Bagautdino/DoctorOnDemand/actions/workflows/python-security.yml)


# DoctorOnDemand

DoctorOnDemand — это веб-приложение, созданное для связи пациентов с врачами онлайн. Разработанное на основе Flask и SQLite, оно позволяет пациентам искать врачей, записываться на прием и оставлять отзывы. Врачи могут регистрироваться, управлять своими профилями и принимать записи на прием.

## Особенности

- Аутентификация и регистрация пользователей и врачей.
- Функционал поиска врачей по специализации, местоположению и наличию свободного времени.
- Система записи на прием.
- Профили врачей с отзывами и рейтингами.
- Расчет расстояния для поиска ближайшего врача.

## Установка

Перед началом убедитесь, что на вашем компьютере установлен Python. Этот проект был разработан с использованием Python 3.8, но должен работать на большинстве версий Python 3.x.

### Клонирование репозитория

```bash
git clone https://github.com/yourusername/DoctorOnDemand.git
cd DoctorOnDemand
```

### Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

## Конфигурация

Приложение использует SQLite для базы данных и автоматически создаст файл `mydatabase.db` в директории проекта.

## Запуск приложения

```bash
flask run
```

Приложение будет доступно по адресу `http://localhost:5000`.

## Интеграция с Docker

### Сборка Docker образа

```bash
docker build -t doctorondemand .
```

### Запуск контейнера

```bash
docker run -d -p 5000:5000 doctorondemand
```

### Использование образа с Docker Hub

```bash
docker pull ayvazbudapeshtov/doctorondemand
docker run -d -p 5000:5000 ayvazbudapeshtov/doctorondemand
```

## Безопасность

Проект включает автоматическую проверку зависимостей на наличие уязвимостей. Рекомендуется регулярно обновлять зависимости и следить за уведомлениями о безопасности.

## Непрерывная интеграция и развертывание

В репозитории настроены рабочие процессы GitHub Actions для Docker и проверки безопасности, обеспечивающие автоматическую сборку и тестирование приложения.
