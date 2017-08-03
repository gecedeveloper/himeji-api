from db import db

class ProfileModel(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default = True)

    def __init__(self, name, description):
		self.name = name
		self.description = description

	def json(self):
		return {'name': self.name, 'description': self.description}

    @classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
