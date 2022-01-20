# Тестовое задание в Xsolla
> Цель: реализовать приложение для управления встречами в компании.  
Задание: ![ТЗ](https://github.com/hebgehogg/xsolla_test/blob/master/tz.pdf)

### Content  
[contacts](#contacts)  
[libraries](#libraries)  
[environment](#environment)  
[database](#database)  
[commands](#commands)  

<a name="contacts"><h2>contacts</task></a>  
- Овчинникова Алина Владимировна
- hebgehogg@gmail.com
- тел: +7(950) 446-12-02
- Telegram: @hebgehog


<a name="libraries"><h2>libraries</task></a>  

Для установки библиотек используйте команду:
```python
pip install -r requirements.txt
```

<a name="environment"><h2>environment</task></a>  

Перед запуском создайте файл `.env`. 

В него вставьте настройку бд (добавила для примера)
```python
SQLITE_CONFIG=sqlite+aiosqlite:///xsolla_test_db.db
```


<a name="database"><h2>database</h2></a> 

Посредством Sqlite была добавлена одна таблица `meetings`. 
Ниже описаны поля и их типы.

> Подразумевается что emails массив. 

| column | type |
| --- | --- |
| id | integer primary key |
| name | text |
| start_time | datatime |
| end_time | datatime |
| emails | text |


<a name="commands"><h2>commands</h2></a>  

### Порядок запуска:
* Запуск server.py (uvicorn запустится автоматически)
* Через терминал введите одну из коммед 

> Команда может состоять из указания `корневого адреса API` (не обязательно), `функции` и `параметра` (не обязательно)

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

