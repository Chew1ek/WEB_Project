from datetime import *
from flask import *
from flask_restful import *
from werkzeug.utils import *

from data import db_session, user_resources, jobs_api
from flask_login import *
from data.users import User
from data.jobs import Jobs
from data.login import LoginForm
from data.job_form_model import ItemForm
from data.register_form import RegisterForm
import requests
import os
from sqlalchemy import *
import random



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MOZNO'] = {'png', 'jpg', 'jpeg'}

login_manager = LoginManager()
login_manager.init_app(app)


def create_upload_folder():
    upload_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_path):
        os.makedirs(upload_path, exist_ok=True)

create_upload_folder()

def allowed_file(filename, allowed_extensions):
    a = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return a in allowed_extensions


@app.route('/basket')
def basket():
    basket_items = session.get('basket', [])
    return render_template('basket.html', items=basket_items, bg=session.get('background', '#FFFFFF'))



@app.route('/remove_from_basket/<int:item_id>', methods=['POST'])
def remove_from_basket(item_id):
    if 'basket' in session:
        basket = session['basket']
        for index, item in enumerate(basket):
            if item['item_id'] == item_id:
                del basket[index]
                session.modified = True
    return render_template('basket.html', bg=session.get('background', '#FFFFFF'))


@app.route('/add_to_basket/<int:item_id>', methods=['POST'])
def add_to_basket(item_id):
    if not current_user.is_authenticated:
        return render_template('login.html', bg=session.get('background', '#FFFFFF'))

    response = requests.get(f'http://127.0.0.1:10000/api/items/{item_id}')
    if response.status_code != 200:
        return "Товар не найден", 404

    item_data = response.json()['items']

    if 'basket' not in session:
        session['basket'] = []

    session['basket'].append({
        'item_id': item_id,
        'item_name': item_data['item_name'],
        'price': item_data['price']
    })
    session.modified = True

    return redirect('/catalog')


@app.route('/buy', methods=['POST'])
def buy():
    if not current_user.is_authenticated:
        return render_template('base.html')
    db_sess = db_session.create_session()
    for item in session.get('basket', []):
        del_item = db_sess.get(Jobs, item['item_id'])
        if del_item:
            db_sess.delete(del_item)

    db_sess.commit()
    session.pop('basket', None)
    return redirect('/catalog')


@app.route('/buy_solo/<int:item_id>', methods=['POST'])
def buy_solo(item_id):
    if not current_user.is_authenticated:
        return render_template('base.html')
    db_sess = db_session.create_session()
    del_item = db_sess.get(Jobs, item_id)
    if del_item:
        db_sess.delete(del_item)
        db_sess.commit()
    return redirect(url_for('catalog'))


@app.route('/catalog')
def catalog():
    db_sess = db_session.create_session()
    jobs = db_sess.scalars(select(Jobs)).all()
    db_sess.commit()
    return render_template('items_list.html', jobs=jobs, bg=session.get('background', '#FFFFFF'))


@app.route('/catalog/<int:item_id>')
def item_desc(item_id):
    response = requests.get(f'http://127.0.0.1:10000/api/items/{item_id}')
    if response.status_code != 200:
        return render_template('base.html', message="Товар не найден"), 404

    data = response.json()['items']
    return render_template(
        'item_desc.html',
        item_name=data['item_name'],
        description=data['description'],
        item_id=data['id'],
        price=data['price'],
        image_path=data.get('image_path', '')
    )

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/')
@app.route('/index')
def index():
    session.pop('basket', None)
    session.modified = True
    return render_template('base.html', bg=session.get('background', '#FFFFFF'))


@app.route('/theme')
def theme():
    if 'background' not in session or session['background'] == '#FFFFFF':
        session['background'] = '#808080'
    else:
        session['background'] = '#FFFFFF'

    return render_template('base.html', bg=session['background'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.scalar(
            select(User).filter_by(email=form.email.data)
        )
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, bg=session.get('background', '#FFFFFF'))
    return render_template('login.html', title='Авторизация', form=form, bg=session.get('background', '#FFFFFF'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    random_number = random.randint(1000, 1000000)
    if form.validate_on_submit():
        user = User()
        db_sess = db_session.create_session()
        user.surname = form.surname.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        try:
            db_sess.commit()
        except Exception as e:
            return render_template('register_user.html',
                                          title='Регистрация',
                                          form=form,
                                          message="Уже есть")
        return redirect("/login")
    return render_template('register_user.html', title='Регистрация', form=form, random_number=random_number,
                           bg=session.get('background', '#FFFFFF'))


@app.route('/vasiliev')
def vasiliev():
    return render_template('vasiliev.html', bg=session.get('background', '#FFFFFF'))



@app.route('/seller', methods=['GET', 'POST'])
def seller():
    form = ItemForm()
    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        relative_path = os.path.join('uploads', filename)
        db_sess = db_session.create_session()
        item = Jobs(
            image_path=relative_path,
            item_name=form.item_name.data,
            description=form.description.data,
            name_one=current_user.surname,
            price=form.price.data,
            start_date=datetime.now(),
        )
        db_sess.add(item)
        db_sess.commit()

        return redirect('/')
    return render_template('sell_some.html', form=form, bg=session.get('background', '#FFFFFF'))


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/database.db")
    app.register_blueprint(jobs_api.blueprint)
    api.add_resource(user_resources.UsersResource, '/api/v2/user/<int:user_id>')
    api.add_resource(user_resources.UsersResourceList, '/api/v2/users/')
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()