from testar import app, db
from testar.utils import http_ok, http_err, make_json
from testar.models import Question, Answers
from testar.security import secured


@app.route('/v1/questions/<q_id>/answers', methods=['POST'])
@secured()
@make_json('text')
def answer_post(data, token_data, q_id):
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answer = Answers(text=data['text'], correct=data['correct'], question_id=question.id)
    db.session.add(answer)
    db.session.commit()
    return http_ok(answer.asdict())


@app.route('/v1/questions/<q_id>/answers/<a_id>')
@secured()
def answer_get(token_data, q_id, a_id):
    answer = Question.query.filter_by(id=q_id, user_id=token_data['id']).first().answers.query.filter_by(id=a_id).first()
    if not answer:
        return http_err(404, 'answer not found')
    return http_ok(answer.asdict())


@app.route('/v1/questions/<q_id>/answers', methods=['GET'])
@secured()
def answers_get(q_id, token_data):
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answers = [a.asdict() for a in question.answers]
    return http_ok(dict(answers=answers))


@app.route('/v1/questions/<q_id>/answers/<a_id>', methods=['DELETE'])
@secured()
def answer_delete(q_id, a_id, token_data):
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answer = question.query.filter_by(id=a_id)
    if not answer:
        return http_err(404, 'answer not found')
    db.session.delete(answer)
    db.session.commit()
    return http_ok(answer.asdict())


@app.route('/v1/questions/<q_id>/answers/<a_id>', methods=['PATCH'])
@secured()
@make_json('text', 'correct')
def answer_patch(q_id, a_id, token_data, data):
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answer = question.query.filter_by(id=a_id).first()
    if not answer:
        return http_err(404, 'answer not found')
    answer.text = data['text']
    answer.correct = data['correct']
    db.session.add(answer)
    db.session.commit()
    return http_ok(answer.asdict())
