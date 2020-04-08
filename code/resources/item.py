import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return ({'message' : 'Item Not Found'}), 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return ({'message' : 'Item name with "{}" already exists'.format(name)}), 400 # bad request
            
        data = Item.parser.parse_args()
        item = ItemModel(name,data['price'])
        try:
            item.insert()
        except Exception as e:
            return ({'message': 'An error occurred inserting the data'}), 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('store.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name, ))
        connection.commit()
        connection.close()
        return ({'message' : "Item Deleted"})

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        updated_item = ItemModel(name,data['price'])
        item = ItemModel.find_by_name(name)
        if item is None:
            try:
                updated_item.insert()
            except:
                return ({'message': 'An error occurred inserting the data'}), 500
        else:
            try:
                updated_item.update()
            except:
                return ({'message': 'An error occurred Updating the data'}), 500
        return updated_item.json()         
        
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
        