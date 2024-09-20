from flask import Flask, request
from flask_migrate import Migrate

from models import db, Item, Customer, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'

#examples of alternative to app.route with app.get and app.post
#Main Pro: separates functions into specific uses, might make sense if lots of complicated stuff hitting the same end points
#Main Con: duplicate code
#GET all - 
@app.get('/items') # should only receive get requests
def get_all_items():
    items = Item.query.all()
    # item_list = []
    # for item in items:
    #     item_list.append(item.to_dict())
    return [item.to_dict(rules=['-reviews']) for item in items], 200



# POST item
@app.post('/items')
def post_items():
    # get json data from request object and construct an Item with it
    data = request.get_json()
    new_item = Item(name=data.get('name'), price=data.get('price'))
    # add and commit to db
    db.session.add(new_item)
    db.session.commit()
    #return serialized data with status code
    return new_item.to_dict(), 201


# GET item by id
@app.get('/items/<int:id>')
def get_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()
    if item is None:
        return {"error": "item not found!"}, 404
    
    return item.to_dict(), 200

# PATCH item by id
@app.patch('/items/<int:id>')
def patch_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()
    
    if item is None:
        return {"error": "item not found!"}, 404
    
    data = request.get_json()
    #iterate through data to change relevant item[key] values to data[key] values
    for attr in data:
        setattr(item, attr, data[attr])

    db.session.add(item)
    db.session.commit()

    return item.to_dict(), 200


# DELETE item
@app.delete('/items/<int:id>')
def delete_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()

    if item is None:
        return {"error": "item not found!"}, 404
    
    db.session.delete(item)
    db.session.commit()

    return {'status': 'item deleted successfully'}, 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
