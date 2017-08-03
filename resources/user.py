from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel


class User(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('password',
		type=str,
		required=True,
		help="This field cannot be blank."
	)
	parser.add_argument('email',
		type=str,
		required=True,
		help="This field cannot be blank."
	)
	parser.add_argument('enabled', type=bool)

	parser_for_update = parser.copy()
	parser_for_update.replace_argument('email', required=False)
	parser_for_update.replace_argument('password', required=False)

	def post(self, username):
		if UserModel.find_by_username(username):
			return {'message': "A user with username '{}' already exists.".format(username)}, 404

		data = User.parser.parse_args()
		user = UserModel(username, **data)

		try:
			user.save_to_db()
		except:
			return {'message': 'An error ocurred while creating the user.'}, 500

		return user.json(), 201

	@jwt_required()
	def get(self, username):
		user = UserModel.find_by_username(username)
		if user:
			return user.json()
		return {'message': 'User not found'}, 404

	@jwt_required()
	def delete(self, username):
		user = UserModel.find_by_username(username)
		if user:
			user.delete_from_db()

		return {'message': 'User deleted'}

	@jwt_required()
	def put(self, username):
		data = User.parser_for_update.parse_args()
		user = UserModel.find_by_username(username)

		if user is None:
			user = UserModel(username, **data)
		else:
			if data['email']:
				user.email = data['email']
			if data['password']:
				user.password = data['password']
			if data['enabled'] != None:
				user.enabled = data['status']

		try:
			user.save_to_db()
		except:
			return {'message': "An error ocurred saving the user."}, 500

		return user.json()


class UserList(Resource):

	@jwt_required()
	def get(self):
		return {'users': [user.json() for user in UserModel.query.all()]}
