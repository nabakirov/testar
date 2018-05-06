from testar import db
competition_participants = db.Table('competition_participants',
                                    db.Column('competition', db.Integer, db.ForeignKey('competition.id'), primary_key=True),
                                    db.Column('user', db.Integer, db.ForeignKey('user.id'), primary_key=True))

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    start_date = db.Column(db.Float, index=True)
    end_date = db.Column(db.Float, index=True)
    description = db.Column(db.Text, nullable=True)
    participants = db.relationship('User', secondary=competition_participants, backref='competition', lazy='joined')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def asdict(self):
        return dict(id=self.id,
                    title=self.title,
                    test_id=self.test_id,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    description=self.description)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, nullable=True)

    def asdict(self):
        return dict(question=self.question_id,
                    answer=self.answer_id)
