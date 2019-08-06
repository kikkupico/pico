from flask import Flask,jsonify,request
from persistence import *
from playhouse.shortcuts import model_to_dict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


(create, read, update, delete, delete_all) = ('create', 'read', 'update', 'delete', 'delete_all')
default_props = {}

def unroll(row):
        to_dict = model_to_dict(row, recurse=False)
        props = to_dict.pop('properties')
        return {**props, **to_dict}

class Anyone:
    def handle_read_all(r, check_request, error):
        db_connection.connect()
        if check_request():            
            return jsonify([{**(unroll(e)), **{'url':request.url+'/'+str(e.id)}} for e in db[r].select()])
        else:
            return error()

    def handle_create(r, check_request, error):
        if check_request():
            creator = User.get(token=request.headers['token']) if 'token' in request.headers else User.get(username='guest')
            props = {**request.json,**default_props[r]} if default_props[r] else request.json
            e = db[r].create(properties=props,creator=creator)
            return jsonify(**(unroll(e)), **{'url':request.url+'/'+str(e.id)}), 201
        else:
            return error()           

    def handle_read_one(r, i, check_request, check_item, error):
        if check_request():
            item = db[r].get_or_none(id=i)
            if(item is None): return 'Not found', 404
            if(check_item(item)):
                return jsonify(**(unroll(item)), **{'url':request.url})
            else:
                return error()
        else:
            return error()

    def handle_update(r, i, check_request, check_item, error):
        if check_request():
            item = db[r].get_or_none(id=i)
            if(item is None): return 'Not found', 404
            if(check_item(item)):
                item.properties = {**item.properties, **request.json}
                item.save()
                return jsonify(**(unroll(item)), **{'url':request.url})
            else:
                return error()            
        else:
            return error()
            
    def handle_delete(r, i, check_request, check_item, error):
        if check_request():
            item = db[r].get_or_none(id=i)
            if(item is None): return 'Not found', 404
            if(check_item(item)):
                item.delete_instance()
                return '', 204
            else:
                return error()
        else:
            return error()

    def handle_delete_all(r, check_request, error):
        if check_request():            
            db[r].delete().execute()
            return '',204
        else:
            return error()
    
    def check_request():
        return True

    def check_item(i):
        return True

    def error():
        return 'Not found', 404

    @classmethod
    def can(cls, actions, resource):
        if resource not in db:
            db[resource]=None 
        for action in actions:
            if action == read:
                app.add_url_rule('/'+resource, 'read_'+resource, lambda:cls.handle_read_all(resource, cls.check_request, cls.error))
                app.add_url_rule('/'+resource+'/<int:r_id>', 'read_one_'+resource, lambda **d: cls.handle_read_one(resource, d['r_id'], cls.check_request, cls.check_item, cls.error))
            if action == create:
                app.add_url_rule('/'+resource, 'create_'+resource, lambda:cls.handle_create(resource, cls.check_request, cls.error), methods=['POST'])
            if action == update:
                app.add_url_rule('/'+resource+'/<int:r_id>', 'update_'+resource, lambda **d: cls.handle_update(resource, d['r_id'], cls.check_request, cls.check_item, cls.error), methods=['PUT', 'PATCH'])
            if action == delete:
                app.add_url_rule('/'+resource+'/<int:r_id>', 'delete_'+resource, lambda **d: cls.handle_delete(resource, d['r_id'], cls.check_request, cls.check_item, cls.error), methods=['DELETE'])
            if action == delete_all:
                app.add_url_rule('/'+resource, 'delete_all_'+resource, lambda:cls.handle_delete_all(resource, cls.check_request, cls.error), methods=['DELETE'])



class AuthenticatedUser(Anyone):    
    def check_request():
        return 'token' in request.headers


class Creator(AuthenticatedUser):    
    def check_item(item):
        print(getattr(item,'creator').id)
        return request.headers['token'] == getattr(item,'creator').username

def end():
    setup()


@app.route('/')
def index():    
    return 'it works'
