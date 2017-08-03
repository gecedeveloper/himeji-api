from db import db

class RoleModel(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default = True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(id = name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
