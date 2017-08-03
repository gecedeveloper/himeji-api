from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.menu import MenuModel

class Menu(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('name',
		type = str,
		required = True,
		help = "This field cannot be left blank!"
	)
	parser.add_argument('description')
	parser.add_argument('url')

	@jwt_required()
	def get(self, _id):
		menu = MenuModel.find_by_id(_id)
		if menu:
			return menu.json()
		return {'message': 'Menu not found'}, 404

	def post(self):
		data = Menu.parser.parse_args()
		if MenuModel.find_by_name(data['name']):
			return {'message': "A menu with name '{}' already exists.".format(name)}, 400

		menu = MenuModel(**data)

		try:
			menu.save_to_db()
		except:
			return {'message': "An error ocurred inserting the menu."}, 500

		return menu.json(), 201

	def delete(self, _id):
		menu = MenuModel.find_by_id(_id)
		if menu:
			menu.delete_from_db()

		return {'message': 'Menu deleted'}

	def put(self, _id):
		data = Menu.parser.parse_args()
		menu = MenuModel.find_by_id(_id)

		if menu is None:
			menu = MenuModel(**data)
		else:
			if data['name']:
				menu.name = data['name']
			if data['description']:
				menu.description = data['description']
			if data['url']:
				menu.url = data['url']

		try:
			menu.save_to_db()
		except:
			return {'message': "An error ocurred saving the menu."}, 500


		return menu.json()


class MenuList(Resource):

	def get(self):
		return {'menus': [menu.json() for menu in MenuModel.query.all()]}
