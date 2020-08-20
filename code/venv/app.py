from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from user import UserRegister
from item import Item, ItemList

from security import authenticate, identity

# Below the app is created
app = Flask(__name__)
app.secret_key = 'superlongandsecurepassword'
# Below the api is created and imported from flask_restful
api = Api(app)

#JWT creates a new endpoint /auth, which intakes a username and password.
# JWT then sends the username and password to the authenticate and identity functions
jwt = JWT(app, authenticate, identity)

# Below tells the api that the resource item/<string:name> is now accessible via the api
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# before running the app
# This condition checks if this file is being run, or simply being imported,
if __name__ == '__main__':
    app.run(port=5000, debug=True)
