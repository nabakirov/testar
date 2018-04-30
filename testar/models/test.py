from testar import db
from time import time as now

test_questions = db.Table('test_questions',
                          db.Column('test_id', db.Integer, db.ForeignKey('test.id'), primary_key=True),
                          db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True))


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Float, nullable=False)
    end_date = db.Column(db.Float, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    questions = db.relationship('Question', secondary=test_questions, backref=db.backref('tests', lazy=True), lazy=True)
    # participants = db.relationship('TestParticipants', backref='test', lazy=True)

    def asdict(self):
        return dict(id=self.id,
                    title=self.title,
                    subtitle=self.subtitle,
                    description=self.description,
                    start_date=self.start_date,
                    end_date=self.end_date)

#
# class TestParticipants(db.Model):
#     test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
#     answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
#
#
#     # TODO: test admins that can view