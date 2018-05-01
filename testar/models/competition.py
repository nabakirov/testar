from testar import db


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    start_date = db.Column(db.Float, index=True)
    end_date = db.Column(db.Float, index=True)
    description = db.Column(db.Text, nullable=True)
    participants = db.relationship('Participant', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def asdict(self):
        return dict(id=self.id,
                    title=self.title,
                    test_id=self.test_id,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    description=self.description)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))
