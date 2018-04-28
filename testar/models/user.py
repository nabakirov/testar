from testar import db
from passlib.hash import pbkdf2_sha256


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(), nullable=False)

    questions = db.relationship('Question', backref='user', lazy=True)

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

    def email_exists(self):
        if self.query.filter_by(email=self.email).first():
            return True
        return False

    def username_exists(self):
        if self.query.filter_by(username=self.username).first():
            return True
        return False