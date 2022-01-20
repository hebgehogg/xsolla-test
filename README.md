# Тестовое задание в Xsolla
> Цель: реализовать приложение для управления встречами в компании.

- Овчинникова Алина Владимировна
- hebgehogg@gmail.com
- тел: +7(950) 446-12-02
- Telegram: @hebgehog

### Content  
[libraries](#libraries)  
[environment](#environment)  
[database](#database)  
[commands](#commands) 
[task](#task) 


<a name="libraries"><h2>libraries</task></a>
Для установки библиотек используйте команду:
```python
pip install -r requirements.txt
```

<a name="environment"><h2>environment</task></a>
Перед запуском создайте файл `.env`
В него вставить настройку бд (добавила для примера)
```python
SQLITE_CONFIG=sqlite+aiosqlite:///xsolla_test_db.db
```


<a name="database"><h2>database</h2></a>
meetings
| column | type |
| --- | --- |
| id | integer primary key |
| name | text |
| start_time | datatime |
| end_time | datatime |
| emails | text |


<a name="commands"><h2>commands</h2></a>

python client.py —api-root=localhost:8080/api/ create data.json

python client.py update 2


<a name="task"><h2>database</task></a>
