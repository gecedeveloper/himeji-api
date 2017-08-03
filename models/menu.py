from db import db

class MenuModel(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    description = db.Column(db.Text)
    url = db.Column(db.String(200))
    status = db.Column(db.Boolean, default = True)

    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'url': self.url}

    @classmethod
    def find_by_id(cls, _id):
	       return cls.query.filter_by(id = _id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
