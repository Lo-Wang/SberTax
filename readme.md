# SberTax

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
![Static Badge](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue&labelColor=FFD43B)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

## Архитектура репозитория

### Основная модель веток:
1. **`main`**:
   - Главная стабильная ветка.
   - Только релизные версии проекта попадают сюда.
   - Ветка защищена, слияние происходит только через Pull Request (PR) с успешными тестами.

2. **`develop`**:
   - Основная ветка для активной разработки.
   - Сюда вливаются изменения с feature-веток после их завершения и успешного тестирования.
   - Периодически изменения из `develop` сливаются в `main`, когда готов новый релиз.
   - Должна содержать Docker-compose файл для поднятия всех сервисов в единой среде.

3. **`feature/*`**:
   - Ветки для каждой новой фичи или задачи.
   - Создаются от `develop` и после завершения работы сливаются обратно в `develop`.
   - Пример названия: `feature/api-endpoints`, `feature/data-processing`.

4. **`bugfix/*`**:
   - Ветки для исправления багов, изначально их нет.
   - Создаются от `develop` или, в случае критических ошибок на продакшне, от `main`.
   - После фикса баги вливаются обратно в соответствующую ветку (например, `develop` или `main`).

5. **`hotfix/*`**:
   - Ветки для срочных исправлений в продакшене, изначально их нет.
   - Создаются от `main`, исправления тестируются и затем вливаются обратно в `main` и `develop`.
   - Пример названия: `hotfix/critical-bug`.

6. **`release/*`**:
   - Ветки для подготовки релиза.
   - Когда фичи стабилизированы в `develop`, создается ветка `release/x.x.x` для подготовки новой версии.
   - После тестирования и исправлений изменения сливаются в `main`.


### Визуализация:
```bash
main <--- release <--- develop <--- feature/*
 ^          ^            ^             ^
 |          |            |             |
 hotfix     bugfix      feature       feature
```
