from testar import db

questions_groups = db.Table('questions_groups',
                            db.Column('question', db.Integer, db.ForeignKey('question.id'), primary_key=True),
                            db.Column('group', db.Integer, db.ForeignKey('group.id'), primary_key=True))

users_groups = db.Table('users_groups',
                        db.Column('user', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('group', db.Integer, db.ForeignKey('group.id'), primary_key=True))


class GroupsGroups(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    group = db.Column(db.Integer, index=True)
    entry = db.Column(db.Integer, index=True)



class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    # TODO: many-to-many field, group_id -> array
    # group_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    questions = db.relationship('Question', secondary=questions_groups)
    users = db.relationship('User', secondary=users_groups)

    def asdict(self):
        return dict(id=self.id,
                    title=self.title,
                    description=self.description)


