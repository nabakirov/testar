from testar import db
from time import time as now
from testar.utils import mix


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False, index=True)
    created = db.Column(db.Float, default=int(now()))
    answers = db.relationship('Answers', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # group_id = db.Column(db.Integer, nullable=True)

    def asdict(self, with_created=True):
        a = dict(id=self.id, text=self.text)
        if with_created:
            a['created'] = self.created
        return a

    def mixed_answers(self):
        answers = [a.asdict(with_correct=False) for a in self.answers]
        return mix(answers)

    def only_corrects(self):
        corrects = []
        for answer in self.answers:
            if answer.correct:
                corrects.append(answer.id)
        return corrects






class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def asdict(self, with_correct=True):
        a = dict(
            id=self.id,
            text=self.text
        )
        if with_correct:
            a['correct'] = self.correct
        return a

