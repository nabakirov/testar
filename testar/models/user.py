from testar import db
from passlib.hash import pbkdf2_sha256
from time import time as now
from .competition import competition_participants


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False, index=True)
    email = db.Column(db.String(), unique=True, nullable=False, index=True)
    pwd_hash = db.Column(db.String(), nullable=False)
    registered = db.Column(db.Float, default=now())
    questions = db.relationship('Question', backref='user', lazy=True)
    tests = db.relationship('Test', lazy=True)
    competitions = db.relationship('Competition', secondary=competition_participants, lazy=True)
    admin = db.Column(db.Boolean, default=False)
    manager = db.Column(db.Boolean, default=False)
    groups = db.relationship('Group', lazy=True)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)

    # group_id = db.Column(db.Integer, nullable=True)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pwd_hash = pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.pwd_hash)

    def asdict(self):
        scopes = []
        if self.admin:
            scopes.append('admin')
        if self.manager:
            scopes.append('manager')
        return dict(id=self.id,
                    username=self.username,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email,
                    scopes=scopes)

