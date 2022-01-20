# Тестовое задание в Xsolla
> Цель: реализовать приложение для управления встречами в компании.  
Задание: ![ТЗ](https://github.com/hebgehogg/xsolla_test/blob/master/tz.pdf)

### Content  
[contacts](#contacts)  
[libraries](#libraries)  
[environment](#environment)  
[database](#database)  
[commands](#commands)  

***

<a name="contacts"><h2>contacts</h2></a>  

- Овчинникова Алина Владимировна
- hebgehogg@gmail.com
- тел: +7(950) 446-12-02
- Telegram: @hebgehog


<a name="libraries"><h2>libraries</h2></a>  

Для установки библиотек используйте команду:
```python
pip install -r requirements.txt
```

<a name="environment"><h2>environment</h2></a>

Перед запуском создайте файл `.env`. 

В него вставьте настройку бд (добавила для примера)
```python
SQLITE_CONFIG=sqlite+aiosqlite:///xsolla_test_db.db
```

<a name="database"><h2>database</h2></a>

Посредством Sqlite были созданы таблицы `meetings`, `users`, `eeting_user`.
Был выбран именно такой вариант реализации тк это более нормализованная форма чем создание 1 таблицы meetings с текстовым полем emails.
Это нужно для того, чтобы при аналитике (такая изначально стояла задача) можно было более быстро проверить какие пользователи были на встрече.
Ниже описаны поля и их типы.

> meetings. 

| column | type |
| --- | --- |
| id | integer PRIMARY KEY |
| name | text NOT NULL |
| start_time | datatime NOT NULL |
| end_time | datatime NOT NULL |
| emails | text NOT NULL|


> users. 

| column | type |
| --- | --- |
| id | integer PRIMARY KEY |
| `email` | text NOT NULL|


> meeting_users  

| column | type |
| --- | --- |
| user_id | integer NOT NULL |
| meeting_id | integer NOT NULL |


<a name="commands"><h2>commands</h2></a>  

> Порядок запуска:
> 1. Запуск server.py (uvicorn запустится автоматически)
> 2. Через терминал введите одну из коммед 

Команда может состоять из указания `корневого адреса API` (не обязательно), `функции` и `параметра` (не обязательно)

### create:
Указание метода и файла.
```python
python client.py create data.json
```
Можно также добавить путь (в любой метод)
```python
python client.py --api-root=localhost:8080/api create data.json
```

---

### select:
Общий select который выводит по 10 объектов все что есть в таблице.
```python
python client.py select
```
Select по id
```python
python client.py select 4
```
Возвращает объект/объекты

---

### create:
Указание метода и файла.
```python
python client.py update update_data.json
```
Возвращает id

---


### update:
Указание метода и файла.
```python
python client.py create data.json
```
Возвращает id

---


### delete:
Указание метода и объекта который требуется удалить.
```python
python client.py delete 4
```
Возвращает id

---

### create_table:
Для теста было создано. Если потребуется обновить бд можно ее удалить и пересоздать так таблицу.
```python
python client.py create_table
```

# Все файлы из примеров добавлены в проект

