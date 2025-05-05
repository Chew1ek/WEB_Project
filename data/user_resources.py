from .users import User
from flask import jsonify
from . import db_session
from flask_restful import reqparse, abort, Api, Resource


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict()})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)

# http://127.0.0.1:8080/api/v2/users/surname=lol&name=kek&age=13&position=kek&speciality=kek&address=kek&email=kek@kek.ru&password=123

class UsersResourceList(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({
            'users':
                [item.to_dict() for item in user]
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        User.surname = args["surname"]
        User.name = args["name"]
        User.age = args["age"]
        User.position = args["position"]
        User.speciality = args["speciality"]
        User.address = args["address"]
        User.email = args["email"]
        User.hashed_password = args["password"]
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})




