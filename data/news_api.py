import flask
from flask import jsonify
from . import db_session
from .tasks import Tasks
from .users import User


blueprint = flask.Blueprint('news_api', __name__, template_folder='templates')


@blueprint.route('/check_task/<int:id>', methods=["GET", "POST"])
def check(id):
    db_sess = db_session.create_session()
    items = db_sess.query(Tasks).filter(id == Tasks.id)
    print(items)
    return jsonify(
        {
            'tasks': [item.to_dict(only=('title', 'content', 'id'))
                      for item in items]
        }
    )


@blueprint.route('/check_link/<str:token>', methods=["GET", "POST"])
def check_link(token):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.bot_id == token).first()
    if user.linked.data:
        return False
    return True


@blueprint.route('/link/<str:token>')
def link(token):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.bot_id == token).first()
    if user:
        user.linked = True
        db_sess.commit()


@blueprint.route('/test/<int:id>')
def test(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id)
    return jsonify(
        {'user': user.to_dict()}
    )
