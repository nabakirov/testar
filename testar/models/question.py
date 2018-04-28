from testar import db
from datetime import datetime


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())
    answers = db.relationship('Answers', backref='question', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def asdict(self):
        return dict(id=self.id,
                    text=self.text,
                    time=self.time)


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def asdict(self):
        return dict(id=self.id,
                    text=self.text,
                    correct=self.correct)