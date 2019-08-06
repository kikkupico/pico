import datetime, json
from peewee import *


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


db_connection = SqliteDatabase('temp.db')
db = {}
(system, guest)=(None, None)

class User(Model):
    username = TextField()
    token = TextField()
    class Meta:
        database = db_connection

def make_persistent(resource):        
    class BaseModel(Model):
        properties = JSONField()
        created_at = DateTimeField(default=datetime.datetime.now)
        creator = ForeignKeyField(User, backref=resource)
        class Meta:
            database = db_connection
            db_table = resource

    db[resource] = BaseModel

    return BaseModel

def setup():
    global system, guest
    print('creating tables for', db.keys())
    db_connection.connect()
    db_connection.create_tables([User])
    for resource in db.keys():
        db[resource] = make_persistent(resource)
        db_connection.create_tables([db[resource]])
    system=User.create(username='system', token='system')
    guest=User.create(username='guest', token='guest')
    db_connection.close()

def test():
    make_persistent('todos')
    make_persistent('teams')

    setup()    

    db['todos'].create(content="test", creator=system)

    print(User.get(User.id == 1).todos[0].content)


if __name__ == '__main__':
    test()
