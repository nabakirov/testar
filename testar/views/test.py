from testar import app, db
from testar.security import secured
from testar.utils import http_ok, http_err, make_json
from testar.models import Test, Question


@app.route('/v1/tests')
@secured()
def tests_get(token_data):
    tests = Test.query.filter_by(owner=token_data['id']).all()
    data = [t.asdict() for t in tests]
    return http_ok(tests=data)


@app.route('/v1/tests', methods=['POST'])
@secured()
@make_json('questions', 'title', 'start_date', 'end_date')
def tests_post(data, token_data):
    if not isinstance(data['start_date'], (int, float)):
        return http_err(400, 'start_date must be timestamp unix format')
    if not isinstance(data['end_date'], (int, float)):
        return http_err(400, 'end_date must be timestamp unix format')
    if not isinstance(data['questions'], list):
        return http_err(400, 'questions must be array of question ids')
    if data['end_date'] < data['start_date']:
        return http_err(400, 'specify correct end_date *hint greater than start_date')
    for q_id in data['questions']:
        if not isinstance(q_id, int):
            return http_err(400, 'questions must be array of question ids')
    params = {
        k: v
        for k, v in data.items() if k in ['start_date', 'end_date', 'title', 'subtitle', 'description']
    }
    test = Test(**params, owner=token_data['id'], )

    for q_id in data['questions']:
        question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
        if not question:
            return http_err(400, 'question not found, save question first')
        test.questions.append(question)
    db.session.add(test)
    db.session.commit()
    return http_ok(**test.asdict())


@app.route('/v1/tests/<id>')
@secured()
def test_get(id, token_data):
    test = Test.query.filter_by(id=id, owner=token_data['id']).first()
    if not test:
        return http_err(404, 'test not found')
    questions = test.questions
    q_dict = []
    for question in questions:
        answers = [a.asdict() for a in question.answers]
        question = question.asdict()
        question['answers'] = answers
        q_dict.append(question)

    return http_ok(**test.asdict(), questions=q_dict)


@app.route('/v1/tests/<id>', methods=['DELETE'])
@secured()
def test_delete(id, token_data):
    test = Test.query.filter_by(id=id, owner=token_data['id']).first()
    if not test:
        return http_err(404, 'test not found')
    db.session.delete(test)
    db.session.commit()
    return http_ok(**test.asdict())