from db import db

class PersonModel(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key = True)
    documentNumber = db.Column(db.String(9))
    firstName = db.Column(db.String(60))
    lastName = db.Column(db.String(60))
    gender = db.Column(db.String(1))
    birthdate = db.Column(db.String(20))
    phone = db.Column(db.String(30))
    cellphone = db.Column(db.String(30))
    status = db.Column(db.Boolean, default = True)

    def __init__(self, documentNumber, firstName, lastName, gender, birthdate, phone, cellphone):
        self.firstName = firstName
        self.lastName = lastName
        self.documentNumber = documentNumber
        self.gender = gender
        self.birthdate = birthdate
        self.phone = phone
        self.cellphone = cellphone

    def json(self):
        return {'documentNumber': self.documentNumber, 'firstName': self.firstName, 'lastName': self.lastName, 'gender': self.gender
        ,'birthdate': self.birthdate, 'phone': self.phone, 'cellphone': self.cellphone, 'status': self.status}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    @classmethod
    def find_by_documentNumber(cls, documentNumber):
        return cls.query.filter_by(documentNumber = documentNumber).first()
