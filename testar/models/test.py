from testar import db

test_questions = db.Table('test_questions',
                          db.Column('test_id', db.Integer, db.ForeignKey('test.id'), primary_key=True),
                          db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True))


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    questions = db.relationship('Question', secondary=test_questions, backref=db.backref('tests', lazy=True), lazy=True)
    competitions = db.relationship('Competition', lazy=True)

    def asdict(self):
        return dict(id=self.id,
                    title=self.title,
                    description=self.description)
