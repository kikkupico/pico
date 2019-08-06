from pony.orm import *
from datetime import datetime

db_connection = Database()

class User(db_connection.Entity):    
    username = Required(str, unique=True)    

def make_persistent(resource):
    class T(db_connection.Entity):
        owner = Required(User)
        created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
        data = Optional(Json)

    T.__name__ = resource
    T.__qualname__ = resource
    
    
    
    return T


def setup():
    db_connection.bind('sqlite', ':memory:', create_db=True)
    db_connection.generate_mapping(create_tables=True)

set_sql_debug(True)
todo_model = make_persistent('todos')
setup()

todo = todo_model(data={'desc':'wish pop', 'completed':False}, owner=admin)
admin = User(username='system')
guest = User(username='guest')    


@db_session
def test():    
    for user in select(u for u in User)[:]:
        print(user.todos)

if __name__ == '__main__':
    test()
