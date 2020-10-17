# Flask Fyyur

## QuickStart

### Requirements
* PostgreSQL

### Installation

1. Clone or download the repository.
2. Run `pip install -r requirements.txt`, to install the required dependencies under your favorite virtual environment.
3. Run `pg_ctl -D <your DB Server Name> start`, to start your DB server.
4. Run `createdb fyyur`, to create a DB with a name, fyyur here.
5. Go `config.py` and set the following variables:
```
db_url = 'postgresql://localhost:5432/fyyur'
#db_url follows '[dialec]+[DBAPI(optional)]://[username]:[password(optional)]@[host]:[port]/[database_name]'
SQLALCHEMY_DATABASE_URI = db_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
6. Run `FLASK_APP=app.py flask db upgrade`, to create relations.
7. Run `python3 seeder.py`, to populate tables with some data.
8. Run `FLASK_APP=app.py FLASK_DEBUG=true FLASK_ENV=development flask run`
9. Open your browser and type `http://localhost:5000`
10. You made it! You should be able to use the application now.
