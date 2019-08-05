import datetime
from peewee import *


db_connection = SqliteDatabase(':memory:')
db = {}
(system, guest)=(None, None)

class User(Model):
    username = TextField()
    class Meta:
        database = db_connection

def make_persistent(resource):        
    class BaseModel(Model):
        content = TextField()
        timestamp = DateTimeField(default=datetime.datetime.now)
        creator = ForeignKeyField(User, backref=resource)
        class Meta:
            database = db_connection

    BaseModel.__name__=resource
    BaseModel.__qualname__=resource

    db[resource] = BaseModel

    return BaseModel

def setup():
    global system, guest
    db_connection.create_tables([User]+list(db.values()))
    system=User.create(username='system')
    guest=User.create(username='guest')

def test():
    make_persistent('todos')
    make_persistent('teams')

    setup()    

    db['todos'].create(content="test", creator=system)

    print(User.get(User.id == 1).todos[0].content)


if __name__ == '__main__':
    test()


# from pony.orm import *
# from datetime import datetime

# db_connection = Database()

# class User(db_connection.Entity):    
#     username = Required(str, unique=True)    

# def make_persistent(resource):
#     class T(db_connection.Entity):
#         owner = Required(User)
#         created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
#         data = Optional(Json)

#     T.__name__ = resource
#     T.__qualname__ = resource
    
    
    
#     return T


# def setup():
#     db_connection.bind('sqlite', ':memory:', create_db=True)
#     db_connection.generate_mapping(create_tables=True)

# set_sql_debug(True)
# todo_model = make_persistent('todos')
# setup()

# todo = todo_model(data={'desc':'wish pop', 'completed':False}, owner=admin)
# admin = User(username='system')
# guest = User(username='guest')    


# @db_session
# def test():    
#     for user in select(u for u in User)[:]:
#         print(user.todos)

# if __name__ == '__main__':
#     test()
