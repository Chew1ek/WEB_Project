from flask import *
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_login import *
from data.login import LoginForm
from data.job_form_module import JobForm
from datetime import *

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/cookie_test")
def cookie_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def work():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.work_done.data
        job.start_date = datetime.now()
        job.end_date = datetime.now() + timedelta(days=3)
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title="Работа", form=form)


if __name__ == '__main__':
    main()
