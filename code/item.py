import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type= float,
        required=True,
        help="This field can not be blank"
    )

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = self.find_by_name(name)
        if item:
            return item
        return ({'message' : 'Item Not Found'}), 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "SELECT * from items WHERE name = ?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        if row:
            return ({'item': {'name' : row[0], 'price' : row[1] }})

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return ({'message' : 'Item name with "{}" already exists'.format(name)}), 400 # bad request
            
        data = Item.parser.parse_args()
        item = { 'name' : name, 'price' : data['price']}
        try:
            self.insert(item)
        except Exception as e:
            return ({'message': 'An error occurred inserting the data'}), 500
        return item, 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name, ))
        connection.commit()
        connection.close()

        return ({'message' : "Item Deleted"})


    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        updated_item = { 'name' : name, 'price' : data['price']}

        if self.find_by_name(name):
            try:
                self.update(updated_item)
            except:
                return ({'message': 'An error occurred updating the data'}), 500
        else:
            try:
                self.insert(updated_item)
            except:
                return ({'message': 'An error occurred inserting the data'}), 500
        return updated_item            
        
class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "SELECT * from items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price' : row[1]})
        connection.commit()
        connection.close()
        return {'items': items}
        