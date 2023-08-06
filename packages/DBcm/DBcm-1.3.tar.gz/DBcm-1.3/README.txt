The UseDatabase context manager for working with MySQL/MariaDB.

For more information, see Chapters 7, 8, and 9 of Head First Python, 2nd edition.

Simple usage: 

```
from DBcm import UseDatabase

config = { ’host’: ’127.0.0.1’,
           ’user’: ’myUserid',
           ’password’: ’myPassword’,
           ’database’: ’myDB’ }

with UseDatabase(config) as cursor:
    _SQL = "select * from log"
    cursor.execute(_SQL)
    data = cursor.fetchall()
```
