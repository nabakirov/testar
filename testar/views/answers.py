from testar import app, db
from testar.utils import http_ok, http_err, make_json
from testar.models import Question, Answers
from testar.security import secured


@app.route('/v1/questions/<q_id>/answers', methods=['POST'])
@secured('admin manager')
@make_json('text', 'correct')
def answer_post(data, token_data, q_id):
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answer = Answers(text=data['text'], correct=data['correct'], question_id=question.id)
    db.session.add(answer)
    db.session.commit()
    return http_ok(**answer.asdict())


@app.route('/v1/questions/<q_id>/answers/<a_id>')
@secured('admin manager')
def answer_get(token_data, q_id, a_id):
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answer = Answers.query.filter_by(question_id=question.id, id=a_id).first()
    if not answer:
        return http_err(404, 'answer not found')
    return http_ok(**answer.asdict())


@app.route('/v1/questions/<q_id>/answers', methods=['GET'])
@secured('admin manager')
def answers_get(q_id, token_data):
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answers = [a.asdict() for a in question.answers]
    return http_ok(answers=answers)


@app.route('/v1/questions/<q_id>/answers/<a_id>', methods=['DELETE'])
@secured('admin manager')
def answer_delete(q_id, a_id, token_data):
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answer = Answers.query.filter_by(question_id=question.id, id=a_id).first()
    if not answer:
        return http_err(404, 'answer not found')
    db.session.delete(answer)
    db.session.commit()
    return http_ok(**answer.asdict())


@app.route('/v1/questions/<q_id>/answers/<a_id>', methods=['PATCH'])
@secured('admin manager')
@make_json()
def answer_patch(q_id, a_id, token_data, data):
    for k, v in data.items():
        if k not in ['text', 'correct']:
            return http_err(400, 'unknown parameter {}'.format(k))
    question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
    if not question:
        return http_err(404, 'question not found')
    answer = Answers.query.filter_by(question_id=question.id, id=a_id).first()
    if not answer:
        return http_err(404, 'answer not found')
    if data.get('text'):
        answer.text = data['text']
    if data.get('correct'):
        answer.correct = data['correct']
    db.session.add(answer)
    db.session.commit()
    return http_ok(**answer.asdict())
