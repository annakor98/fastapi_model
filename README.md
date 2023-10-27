## I. Cеминар 13.10
1. [Обзор проекта и введение в FastAPI][intro]

## II. Семинар 20.10
1. [Работа с БД][db]
2. [Введение в CI/CD][ci_intro]

---

[intro]: assets/materials/fastapi_introduction.md "intro"
[db]: assets/materials/add_database.md "db"
[ci_intro]: assets/materials/ci_intro.md "ci_intro"

| Подсказка                                                                                       |
|-------------------------------------------------------------------------------------------------|
| Используйте код вида ``db.query(column_1, column_2).group_by(column_1)`` и функцию ``sqlalchemy.func.count`` 
| Используйте код вида ``db.query(model).filter(expression).order_by(column.desc())``             |