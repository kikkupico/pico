from flask import Flask,jsonify,request

app = Flask(__name__)

db = {}
(create, list, retrieve, update, delete) = ('create', 'list', 'retrieve', 'update', 'delete')

class Anyone:
    def handle_list(r):
        return jsonify(db[r])        

    def handle_create(r):
        db[r].append(request.json)
        return 'created', 201

    def handle_retrieve(r, i):
        return jsonify(db[r][i])

    def handle_update(r, i):
        db[r][i] = {**db[r][i], **request.json}
        return jsonify(db[r][i])

    def handle_delete(r, i):        
        return jsonify(db[r].pop(i))

    def can(actions, resource):
        return Anyone.override_can(Anyone, actions, resource)

    def override_can(i, actions, resource):
        if resource not in db:
            db[resource]=[]
        for action in actions:
            if action == list:
                app.add_url_rule('/'+resource, 'list_'+resource, lambda:i.handle_list(resource))
            if action == create:
                app.add_url_rule('/'+resource, 'create_'+resource, lambda:i.handle_create(resource), methods=['POST'])
            if action == retrieve:
                app.add_url_rule('/'+resource+'/<int:r_id>', 'retrieve_'+resource, lambda **d: i.handle_retrieve(resource, d['r_id']))
            if action == update:
                app.add_url_rule('/'+resource+'/<int:r_id>', 'update_'+resource, lambda **d: i.handle_update(resource, d['r_id']), methods=['PUT'])
            if action == delete:
                app.add_url_rule('/'+resource+'/<int:r_id>', 'delete_'+resource, lambda **d: i.handle_delete(resource, d['r_id']), methods=['DELETE'])



class AuthenticatedUser(Anyone):
    def can(actions, resource):
        return Anyone.override_can(AuthenticatedUser, actions, resource)
    
    def handle_list(r):
        if 'token' in request.headers:
            return Anyone.handle_list(r)
        else:
            return 'forbidden', 403

    def handle_create(r):
        if 'token' in request.headers:
            return Anyone.handle_create(r)
        else:
            return 'forbidden', 403

    def handle_retrieve(r, i):
        if 'token' in request.headers:
            return Anyone.handle_retrieve(r, i)
        else:
            return 'forbidden', 403

    def handle_update(r, i):
        if 'token' in request.headers:
            return Anyone.handle_update(r, i)
        else:
            return 'forbidden', 403

    def handle_delete(r, i):        
        if 'token' in request.headers:
            return Anyone.handle_delete(r, i)
        else:
            return 'forbidden', 403


@app.route('/')
def index():    
    return 'it works'
