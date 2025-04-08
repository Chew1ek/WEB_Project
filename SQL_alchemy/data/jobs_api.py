import flask
from . import db_session
from . jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/items/')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify(
        {
            'items':
                [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/items/<int:items_id>', methods=['GET'])
def get_one_jobs(items_id):
    db_sess = db_session.create_session()
    items = db_sess.query(Jobs).get(items_id)
    if not items:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify(
        {
            'items': items.to_dict()
        }
    )