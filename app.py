import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserList
from resources.person import Person, PersonList
from resources.menu import Menu, MenuList
from resources.role import Role, RoleList
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:5000/item/Gian
api.add_resource(ItemList, '/items') #http://127.0.0.1:5000/item/Gian
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')
api.add_resource(Person, '/person/<string:documentNumber>')
api.add_resource(PersonList, '/persons')
api.add_resource(Menu, '/menu', '/menu/<string:_id>')
api.add_resource(MenuList, '/menus')
api.add_resource(Role, '/role', '/role/<string:_id>')
api.add_resource(RoleList, '/roles')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port = 5000)
