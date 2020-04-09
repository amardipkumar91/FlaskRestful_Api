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
    parser.add_argument('store_id', 
        type= int,
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
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except Exception as e:
            return ({'message': 'An error occurred inserting the data'}), 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item Deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()         
        
class ItemList(Resource):
    @jwt_required()
    def get(self):
        '''
            you can use any things either through lambda or list comprehension
        '''
        return {'item' : [item.json() for item in ItemModel.query.all()]} 
        # return {'item' : list(map(lambda x : x.json(), ItemModel.query.all()))}
        