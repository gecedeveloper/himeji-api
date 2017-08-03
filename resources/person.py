from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.person import PersonModel


class Person(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('firstName',
		type=str,
		required=True,
		help="This field cannot be blank."
	)

	parser.add_argument('lastName')
	parser.add_argument('gender')
	parser.add_argument('birthdate')
	parser.add_argument('phone')
	parser.add_argument('cellphone')

	parser_for_update = parser.copy()
	parser_for_update.replace_argument('firstName', required=False)

	def post(self, documentNumber):
		if PersonModel.find_by_documentNumber(documentNumber):
			return {'message': "A person with document number '{}' already exists.".format(documentNumber)}, 404

		data = Person.parser.parse_args()
		person = PersonModel(documentNumber, **data)

		try:
			person.save_to_db()
		except:
			return {'message': 'An error ocurred while creating the person.'}, 500

		return person.json(), 201

	@jwt_required()
	def get(self, documentNumber):
		person = PersonModel.find_by_documentNumber(documentNumber)
		if person:
			return person.json()
		return {'message': 'Person not found'}, 404

	@jwt_required()
	def delete(self, documentNumber):
		person = PersonModel.find_by_documentNumber(documentNumber)
		if person:
			person.delete_from_db()

		return {'message': 'Person deleted'}

	@jwt_required()
	def put(self, documentNumber):
		data = Person.parser_for_update.parse_args()
		person = PersonModel.find_by_documentNumber(documentNumber)

		if person is None:
			person = PersonModel(documentNumber, **data)
		else:
			if data['firstName']:
				person.firstName = data['firstName']
			if data['lastName']:
				person.firstName = data['lastName']
			if data['gender']:
				person.gender = data['gender']
			if data['birthdate']:
				person.birthdate = data['birthdate']
			if data['phone']:
				person.phone = data['phone']
			if data['cellphone']:
				person.cellphone = data['cellphone']

		try:
			person.save_to_db()
		except:
			return {'message': "An error ocurred saving the person."}, 500

		return person.json()


class PersonList(Resource):

	@jwt_required()
	def get(self):
		return {'persons': [person.json() for person in PersonModel.query.all()]}
