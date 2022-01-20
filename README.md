# xsolla_test

.env 
SQLITE_CONFIG=sqlite+aiosqlite:///xsolla_test_db.db

pip install -r requirements.txt


python client.py —api-root=localhost:8080/api/ create data.json

python client.py update 2




python client.py —api-root=localhost:8080/api/ create data.json

- Овчинникова Алина Владимировна
- hebgehogg@gmail.com
- тел: +7(950) 446-12-02
- Telegram: @hebgehog

##### Content 
[task](#task)  
[libraries](#libraries)  
[environment](#environment)  
[database](#database)  
[commands](#commands) 


<a name="database"><h2>database</h2></a>
* meetings

id integer primary key          
name text          
start_time datatime           
end_time datatime             
emails text
