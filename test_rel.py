import datetime, json
from peewee import *
from playhouse.shortcuts import model_to_dict


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


db_connection = SqliteDatabase('test.db')
db = {}
deb_defs={}
(system, guest)=(None, None)

class User(Model):
    username = TextField()
    token = TextField()
    class Meta:
        database = db_connection

class BaseModel(Model):
        properties = JSONField()
        created_at = DateTimeField(default=datetime.datetime.now)            
        class Meta:
            database = db_connection

def make_persistent(resource):
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

def finalize():
    ...

'''
relationships['tickets']{'show':one('shows')} => {'show':ForeignKeyField(db['shows'], backref='tickets')}

'''

def test():
    global system, guest    
    db['teams'] = type('teams', (BaseModel,), {'creator':ForeignKeyField(User, backref='teams')})
    db['todos'] = type('todos', (BaseModel,), {'team':ForeignKeyField(db['teams'], backref='todos'),'creator':ForeignKeyField(User, backref='todos')})
    db_connection.connect()
    db_connection.create_tables([User]+list(db.values()))
    system=User.create(username='system', token='system')
    t=db['teams'].create(creator=system, properties={'name':'popkik'})
    d= db['todos'].create(creator=system, properties={'title':'it works'}, team=t)
    print(model_to_dict(d))

if __name__ == '__main__':
    test()
