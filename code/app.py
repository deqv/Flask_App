from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import User, UserRegister

# Below the app is created
app = Flask(__name__)
app.secret_key = 'superlongandsecurepassword'
# Below the api is created and imported from flask_restful
api = Api(app)

#JWT creates a new endpoint /auth, which intakes a username and password.
# JWT then sends the username and password to the authenticate and identity functions
jwt = JWT(app, authenticate, identity)

items = []

# The api works with resources and every resource is a class
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required=True,
        help="Price not properly entered."
    )
    # jwt_required is inserted to require a jwt token before the HTTP verb
    @jwt_required()
    def get(self,name):
        # next provides the first match instead of providing a list of matches
        # None is the value returned if no matches are found
        # the filter function is equivalent to the for loop below
        item = next(filter(lambda x: x['name']==name, items), None)
#        for item in items:
#            if item['name'] == name:
#                return item
                            # ie: if item is not None
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name']==name, items), None) is not None:
            return {'message': "Item with name '{}' already exists.".format(name)}, 400
                                    # 400 is the HTTP return code for bad request ^^^
        data = Item.parser.parse_args()
        # force=True means you do not need the Content-Type header in Postman
        # silent=True does not return an error but simply returns "None"
#        data = request.get_json(silent=True)
        # ^^^ data is a dictionary
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self,name):
        global items
        # items is remade to include only the values of items
        # that do not equal the name given to the delete function
        items = list(filter(lambda x: x['name']!=name, items))
        return {'message': 'Item deleted.'}

    def put(self,name):
# This parses the JSON payload for valid values to enter into data
        data = Item.parser.parse_args() # replaces the line below
#        data = request.get_json()
        # First must check if item exists
        item = next(filter(lambda x: x['name']==name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

# Below tells the api that the resource item/<string:name> is now accessible via the api
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
# A post request made to '/register' will call the post method in UserRegister class

app.run(port=5000, debug=True)
