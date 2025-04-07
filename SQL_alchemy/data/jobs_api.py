import flask
from . import db_session
from . jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify(
        {
            'jobs':
                [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify(
        {
            'news': jobs.to_dict()
        }
    )