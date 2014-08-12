PythonHelpers
=============

A set of python helpers that help you developing python applications:

#How to use
```
git submodule add https://github.com/GeographicaGS/pythonhelpers.git pythonhelpers

#using postgresSQLModel
from pythonhelpers.database.postgresql.postgresqlmodel import PostgreSQLModel
conn = psycopg2.connect(host="localhost",dbname="XXX"...)
pm = PosgresSQLModel(conn)

user = {"username": "Geographica", "email": "info@geographica.gs","pass":"XXXXX"}
pm.insert("user",user)

user = pm.query("SELECT * FROM user WHERE username=%",["Geographica"]).row()

```

##Datacache.py
Cache your data functions using Redis or memcached (datacache.py)

Add to your code using:
```
# Redis
from pythonhelpers.database.datacache import RedisDataCache
# Memcached
from pythonhelpers.database.datacache import MemcachedDataCache
```

How to use:

```
def testFn():
    return {
            "name": "Alberto",
            "surname" : "Asuero",
            "childs" : [{
                "name": "Isabel",
                "surname" : "Asuero"
            }]
        }

connclient = redis.StrictRedis(host='localhost', port=6379, db=0)
cache = RedisDataCache(connclient,"testapp")

response = cache.reqFunc(testFn,1)

```

##PostgreSQLModel

Easy wrapper for psycopg2 based on CodeIgniter models. A parser from python data structure to SQL, it allows to insert data in a postgresql without writting SQL in a secure way, just give a dictionary (or an array of dictionaries) and the table where the data will be added to.

Add to your code using:
```
from pythonhelpers.database.postgresql.postgresqlmodel import PostgreSQLModel
```

##Samples
For more information take a look at samples folder.


