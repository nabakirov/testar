from flask_script import Manager
from testar import app, db
from testar.models import User
from flask_migrate import MigrateCommand, Migrate


migrate = Migrate(app, db)
manager = Manager(app, db)




@manager.command
def runserver():
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'],
            threaded=app.config['THREADED'])


@manager.command
def create_all():
    db.create_all()


@manager.command
def drop_all():
    db.drop_all()


@manager.command
def recreate():
    db.drop_all()
    db.create_all()

@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake(number_users):
    from sqlalchemy.exc import IntegrityError
    from random import seed, choice
    from faker import Faker

    fake = Faker()
    seed()
    for i in range(number_users):
        u = User(

            username=fake.first_name(),
            email=fake.email(),
            password='password',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()