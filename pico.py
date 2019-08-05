from flask import Flask,jsonify,request

app = Flask(__name__)

db = {}
(create, list, retrieve, update, delete) = ('create', 'list', 'retrieve', 'update', 'delete')


class Anyone:
    def handle_list(r, check_request, error):
        if check_request():
            return jsonify(db[r])
        else:
            return error()

    def handle_create(r, check_request, error):
        if check_request():
            creator = {'creator':request.headers['token']} if 'token' in request.headers else {'creator':'guest'}
            db[r].append({**request.json,**creator})
            return 'created', 201
        else:
            return error()           

    def handle_retrieve(r, i, check_request, check_item, error):
        if check_request():
            item = db[r][i]
            if(check_item(item)):
                return jsonify(db[r][i])
            else:
                return error()
        else:
            return error()

    def handle_update(r, i, check_request, check_item, error):
        if check_request():
            item = db[r][i]
            if(check_item(item)):
                db[r][i] = {**db[r][i], **request.json}
                return jsonify(db[r][i])            
            else:
                return error()            
        else:
            return error()
            
    def handle_delete(r, i, check_request, check_item, error):
        if check_request():
            item = db[r][i]
            if(check_item(item)):
                return jsonify(db[r].pop(i))
            else:
                return error()
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
            db[resource]=[]
        for action in actions:
            if action == list:
                app.add_url_rule('/'+resource, 'list_'+resource, lambda:cls.handle_list(resource, cls.check_request, cls.error))
            if action == create:
                app.add_url_rule('/'+resource, 'create_'+resource, lambda:cls.handle_create(resource, cls.check_request, cls.error), methods=['POST'])
            if action == retrieve:
                app.add_url_rule('/'+resource+'/<int:r_id>', 'retrieve_'+resource, lambda **d: cls.handle_retrieve(resource, d['r_id'], cls.check_request, cls.check_item, cls.error))
            if action == update:
                app.add_url_rule('/'+resource+'/<int:r_id>', 'update_'+resource, lambda **d: cls.handle_update(resource, d['r_id'], cls.check_request, cls.check_item, cls.error), methods=['PUT'])
            if action == delete:
                app.add_url_rule('/'+resource+'/<int:r_id>', 'delete_'+resource, lambda **d: cls.handle_delete(resource, d['r_id'], cls.check_request, cls.check_item, cls.error), methods=['DELETE'])



class AuthenticatedUser(Anyone):    
    def check_request():
        return 'token' in request.headers


class Creator(AuthenticatedUser):    
    def check_item(item):
        return request.headers['token'] == item['creator']


@app.route('/')
def index():    
    return 'it works'
