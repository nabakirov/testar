from testar import app, db
from testar.utils import http_ok, http_err, make_json
from testar.models import Question, Answers, User
from testar.security import secured
from flask import request


@app.route('/v1/questions', methods=['POST'])
@secured('admin manager')
@make_json('text', 'correct_answers', 'incorrect_answers')
def questions_post(data, token_data):
    if not isinstance(data['incorrect_answers'], list):
        return http_err(400, 'incorrect_answers must be array')
    if not isinstance(data['correct_answers'], list):
        return http_err(400, 'correct_answers must be array')
    if not isinstance(data['text'], str):
        return http_err(400, 'text must be string')
    corrects = set()
    incorrects = set()
    for answer in data['correct_answers']:
        if not isinstance(answer, str):
            return http_err(400, 'correct_answers must consist only strings, but {} ({}) found'.
                            format(type(answer), answer))
        corrects.add(answer.lower())
    for answer in data['incorrect_answers']:
        if not isinstance(answer, str):
            return http_err(400, 'incorrect_answers must consist only strings, but {} ({}) found'.
                            format(type(answer), answer))
        incorrects.add(answer.lower())

    matched = corrects.intersection(incorrects)
    if matched:
        return http_err(400, 'there is matches between correct_answers and incorrect_answers',
                        matched=list(matched))

    question = Question(text=data['text'], user_id=token_data['id'])

    for answer in data['correct_answers']:
        ans = Answers(text=answer, correct=True)
        question.answers.append(ans)
    for answer in data['incorrect_answers']:
        ans = Answers(text=answer, correct=False)
        question.answers.append(ans)

    db.session.add(question)
    db.session.commit()

    answers = [q.asdict() for q in question.answers]
    return http_ok(question=question.asdict(),
                   answers=answers)


@app.route('/v1/questions')
@secured('admin manager')
def questions_get(token_data):
    questions = Question.query.filter_by(user_id=token_data['id']).all()
    resp = [q.asdict() for q in questions]
    # for question in questions:
    #     answers = [a.asdict() for a in question.answers]
    #     resp.append(dict(question=question.asdict(), answers=answers))
    return http_ok(questions=resp)


@app.route('/v1/questions/<id>', methods=['GET'])
@secured('admin manager')
def question_get(id, token_data):
    question = Question.query.filter_by(user_id=token_data['id'], id=id).first()
    if not question:
        return http_err(404, 'not found')
    answers = [a.asdict() for a in question.answers]
    return http_ok(**question.asdict(), answers=answers)


@app.route('/v1/questions/<id>', methods=['DELETE'])
@secured('admin manager')
def question_delete(id, token, token_data):
    question = Question.query.filter_by(user_id=token_data['id'], id=id).first()
    if not question:
        return http_err(404, 'not found')
    ans = []
    for a in question.answers:
        db.session.delete(a)
        ans.append(a.asdict())
    db.session.delete(question)
    db.session.commit()
    return http_ok(**question.asdict(), answers=ans)


@app.route('/v1/questions/<id>', methods=['PATCH'])
@secured('admin manager')
@make_json('text')
def question_patch(id, token_data, data):
    question = Question.query.filter_by(user_id=token_data['id'], id=id).first()
    if not question:
        return http_err(404, 'not found')
    question.text = data['text']
    db.session.add(question)
    db.session.commit()
    return http_ok(**question.asdict())

