# xsolla_test

.env 
SQLITE_CONFIG=sqlite+aiosqlite:///xsolla_test_db.db

pip install -r requirements.txt


python client.py —api-root=localhost:8080/api/ create data.json

python client.py update 2


meetings

id integer primary key          
name text          
start_time datatime           
end_time datatime          


members

id integer primary key         
user_id integer        
meeting_id integer         

users

id integer primary key           
email text


python client.py —api-root=localhost:8080/api/ create data.json
