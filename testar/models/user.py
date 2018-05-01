from testar import db
from passlib.hash import pbkdf2_sha256
from time import time as now


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False, index=True)
    email = db.Column(db.String(), unique=True, nullable=False, index=True)
    pwd_hash = db.Column(db.String(), nullable=False)
    registered = db.Column(db.Float, default=now())

    competitions = db.relationship('Participant', backref='user', lazy=True)
    questions = db.relationship('Question', backref='user', lazy=True)
    tests = db.relationship('Test', lazy=True)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pwd_hash = pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.pwd_hash)

    def asdict(self):
        return dict(id=self.id, username=self.username, email=self.email)

