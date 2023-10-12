# Настройка проекта:
pip install -r requirements.txt

# Запуск тестов:
В консоли выполнить команду:
* `pytest -v test_file.py::TestClass::test_method` - запуск конкретного теста
* `pytest -v -m annotation_name` - запуск тестов по тэгу (список аннотаций в pytest.ini - добавляются вручную)
* `pytest` - запуск всех тестов в проекте
* `pytest tests/health_check` - запуск тестов первичной проверки работоспособности системы
* `ssh -L 5434:localhost:5434 -i ~/.ssh/id_rsa apic@209.38.228.41` - если 
  тест запускается локально и ему необходим доступ к БД, необходимо прокинуть 
  порты по необходимому ip (временная мера, потом будет VPN)

# Запуск линтера перед коммитом:
В консоли выполнить команду: `flake8`.
Настройки линтера в файле setup.cfg в корне
#toDo Исправить замечания линтера.

# Структура проекта:
* clients - отдельные сущности для работы с endpoints и всеми его методами
* custom_requests - враппер для библиотеки requests
* data - jsons для фикстур
* entities - сущности с атрибутами (1 модуль = 1 сущность)
* enums - списки однотипных значений, используются в tests и не только
* tests - тесты, используют "высокоуровневые" сущности из clients (например, заказ)
* utils - утилиты (@staticmethod)

### Код должен соответствовать [PEP8](https://peps.python.org/pep-0008/) (Style Guide for Python Code)
