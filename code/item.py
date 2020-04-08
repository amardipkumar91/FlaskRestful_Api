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
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "SELECT * from items WHERE name = ?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        if row:
            return ({'item': {'name' : row[0], 'price' : row[1] }})
        return ({'message' : 'Item Not Found'}), 404

    @jwt_required()
    def post(self, name):

        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return ({'message' : 'Item name with "{}" already exists'.format(name)}), 400 # bad request
            
        data = Item.parser.parse_args()
        item = { 'name' : name, 'price' : data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return ({'message' : "Item Deleted"})

    @jwt_required()
    def put(self, name):
        #request parser

        item = next(filter(lambda x: x['name'] == name, items), None)
        data = Item.parser.parse_args()
        if item is None:
            item = {'name' : name, 'price' : data['price']}
            items.append(item)
        else:
            item.update(data)

        return item            
        
class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items' : items}