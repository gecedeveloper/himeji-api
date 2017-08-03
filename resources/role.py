from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.role import RoleModel

class Role(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('name',
		type = str,
		required = True,
		help = "This field cannot be left blank!"
	)
	parser.add_argument('description')

	@jwt_required()
	def get(self, _id):
		role = RoleModel.find_by_id(_id)
		if role:
			return role.json()
		return {'message': 'Role not found'}, 404

	def post(self):
		data = Role.parser.parse_args()
		if RoleModel.find_by_name(data['name']):
			return {'message': "A role with name '{}' already exists.".format(name)}, 400

		role = RoleModel(**data)

		try:
			role.save_to_db()
		except:
			return {'message': "An error ocurred inserting the role."}, 500

		return role.json(), 201

	def delete(self, _id):
		role = RoleModel.find_by_id(_id)
		if role:
			role.delete_from_db()

		return {'message': 'Role deleted'}

	def put(self, _id):
		data = Role.parser.parse_args()
		role = RoleModel.find_by_id(_id)

		if role is None:
			role = RoleModel(**data)
		else:
			role.name = data['name']
			role.description = data['description']

		try:
			role.save_to_db()
		except:
			return {'message': "An error ocurred saving the role."}, 500


		return role.json()


class RoleList(Resource):

	def get(self):
		return {'roles': [role.json() for role in RoleModel.query.all()]}
