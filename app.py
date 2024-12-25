from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from flask_login import LoginManager
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lr_queue.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'

# Инициализация приложения
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Teachers_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    job_title = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=True)
    reviews = db.relationship('Review', backref='teacher', lazy=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers_list.id'), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)


class ReviewForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])


@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def teachers_list():
    teachers = Teachers_list.query.all()
    return render_template('index.html', teachers=teachers)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        email = request.form['email']

        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Неверные данные'

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('teachers_list'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form.get('teacher_name')
        job_title = request.form.get('job_title')
        photo = request.files.get('photo')

        if not name or not job_title:
            return "Error: Name and Job Title are required.", 400

        photo_data = photo.read() if photo else None

        new_teacher = Teachers_list(name=name, job_title=job_title, photo=photo_data)
        db.session.add(new_teacher)
        db.session.commit()

        return redirect(url_for('teachers_list'))

    return render_template('add_teacher.html')


@app.route('/teacher/<int:teacher_id>')
def teacher_detail(teacher_id):
    teacher = Teachers_list.query.get_or_404(teacher_id)
    average_rating = calculate_average_rating(teacher.reviews)
    return render_template('teacher_detail.html', teacher=teacher, form=ReviewForm(), average_rating=average_rating)


@app.route('/teacher/<int:teacher_id>/review', methods=['POST'])
def add_review(teacher_id):
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(
            teacher_id=teacher_id,
            author=form.author.data,
            content=form.content.data,
            rating=form.rating.data
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Review added successfully!', 'success')
        return redirect(url_for('teacher_detail', teacher_id=teacher_id))
    return redirect(url_for('teacher_detail', teacher_id=teacher_id))


def calculate_average_rating(reviews):
    if not reviews:
        return 0
    total_rating = sum(review.rating for review in reviews)
    return round(total_rating / len(reviews), 1)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)