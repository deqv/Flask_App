from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Price not properly entered."
    )

    @jwt_required()
    def get(self,name):
        # The following iterates through items and checks
        # if the name provided by the get method is found in an item,
        # in which case the item to be returned is set to the found item.
        # If not found, None is assigned
#        item = next(filter(lambda x: x['name']==name, items), None)
        # {'item': item} returns a JSON with the value item
#        return {'item': item}, 200 if item else 404

        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found.'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        # The following is an if condition that checks
        # if the name given by post method is equal to the name of an existing item.
        # If it is, an error message is returned before a duplicate item is created.
        if Item.find_by_name(name)!=({'message': 'Item not found.'}, 404):
            return {'message': "Item with name {} already exists.".format(name)}, 400

        # Item.parser.parse_args() parses the JSON data from the method
        # and extracts the 'price' information that is desired.
        data = Item.parser.parse_args()

        # A new item with the name provided by the method
        # and price parsed from the data is created
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'message': "An error occurred inserting the item."}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # CAUTION: without "WHERE" clause, everything is deleted
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted.'}

    def put(self,name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item == ({'message': 'Item not found.'}, 404):
            try:
                self.insert(updated_item)
                return {'price': updated_item['price']}
            except:
                return {'message': 'An error occurred while inserting.'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occurred while updating.'}, 500
            return {'price': updated_item['price']}

    @classmethod
    def update(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return items
