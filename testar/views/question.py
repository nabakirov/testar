from testar import app, db
from testar.utils import http_ok, http_err, make_json
from testar.models import Question, Answers, User
from testar.security import secured
from flask import request


@app.route('/v1/questions', methods=['POST'])
@secured()
@make_json('text', 'correct_answer', 'incorrect_answers')
def questions_post(data, token, token_data):
    if not isinstance(data['incorrect_answers'], list):
        return http_err(400, 'incorrect_answers must be list')
    question = Question(text=data['text'], user_id=token_data['id'])
    db.session.add(question)
    db.session.commit()
    correct_answer = Answers(text=data['correct_answer'], correct=True, question_id=question.id)
    db.session.add(correct_answer)
    incorrects = []
    for text in data['incorrect_answers']:
        answer = Answers(text=text, question_id=question.id)
        db.session.add(answer)
        incorrects.append(answer)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return http_err(500, str(e))
    incorrect_answers = [answer.asdict() for answer in incorrects]
    return http_ok(dict(question=question.asdict(),
                        correct_answer=correct_answer.asdict(),
                        incorrect_answers=incorrect_answers))


@app.route('/v1/questions')
@secured()
def questions_get(token, token_data):
    questions = Question.query.filter_by(user_id=token_data['id']).all()
    resp = []
    for question in questions:
        answers = [a.asdict() for a in question.answers]
        resp.append(dict(question=question.asdict(), answers=answers))
    return http_ok(dict(data=resp))


@app.route('/v1/questions/<id>', methods=['GET'])
@secured()
def question_get(id, token, token_data):
    question = Question.query.filter_by(user_id=token_data['id'], id=id).first()
    if not question:
        return http_err(404, 'not found')
    answers = [a.asdict() for a in question.answers]
    return http_ok(question.asdict(), answers=answers)


@app.route('/v1/questions/<id>', methods=['DELETE'])
@secured()
def question_delete(id, token, token_data):
    question = Question.query.filter_by(user_id=token_data['id'], id=id).first()
    if not question:
        return http_err(404, 'not found')
    db.session.delete(question)
    ans = []
    for a in question.answers:
        db.session.delete(a)
        ans.append(a.asdict())
    db.session.commit()
    return http_ok(question.asdict(), answers=ans)


@app.route('/v1/questions/<id>', methods=['PATCH'])
@secured()
@make_json('text')
def question_patch(id, token_data, data):
    question = Question.query.filter_by(user_id=token_data['id'], id=id).first()
    if not question:
        return http_err(404, 'not found')
    question.text = data['text']
    db.session.add(question)
    db.session.commit()
    return http_ok(question.asdict())

