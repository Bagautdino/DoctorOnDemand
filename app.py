from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from math import cos, asin, sqrt

app = Flask(__name__)

# Конфигурация приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'your-secret-key'

# Инициализация расширений
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    full_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    call_type = db.Column(db.String(50))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

# Модель доктора
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    location = db.Column(db.String(100))
    about = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    available = db.Column(db.Boolean, default=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.DateTime)
    status = db.Column(db.String(50))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    rating = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Неверное имя пользователя или пароль'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=request.form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    current_user.lat = 59.751244  # Пример широты
    current_user.lng = 37.618423
    user_location = (current_user.lat, current_user.lng)  # Предполагаем, что у пользователя есть координаты

    doctors = Doctor.query.filter(Doctor.name.contains(query) | Doctor.specialization.contains(query)).all()
    doctors_with_distance = [{
        'doctor': doctor,
        'distance': distance(user_location[0], user_location[1], doctor.lat, doctor.lng)
    } for doctor in doctors]

    sorted_doctors = sorted(doctors_with_distance, key=lambda x: x['distance'])

    return render_template('search.html', doctors=sorted_doctors)


@app.route('/doctor/<int:doctor_id>', methods=['GET', 'POST'])
def doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    reviews = Review.query.filter_by(doctor_id=doctor_id).all()
    all_doctors = Doctor.query.all()  # Получаем список всех врачей

    if request.method == 'POST':
        content = request.form.get('content')
        rating = request.form.get('rating')
        new_review = Review(doctor_id=doctor_id, user_id=current_user.id, content=content, rating=rating)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('doctor_profile', doctor_id=doctor_id))

    return render_template('doctor_profile.html', doctor=doctor, reviews=reviews, all_doctors=all_doctors)

def distance(lat1, lon1, lat2, lon2):
    if None in [lat1, lon1, lat2, lon2]:
        return float('inf')  # Возвращает бесконечность, если координаты отсутствуют
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))



@app.route('/find_nearest_doctors')
@login_required
def find_nearest_doctors():
    user_location = (current_user.lat, current_user.lng)
    doctors = Doctor.query.all()
    doctors_with_distance = [{
        'doctor': doctor,
        'distance': distance(user_location[0], user_location[1], doctor.lat, doctor.lng)
    } for doctor in doctors]
    nearest_doctors = sorted(doctors_with_distance, key=lambda x: x['distance'])
    return render_template('nearest_doctors.html', doctors=nearest_doctors)


@app.route('/call_doctor/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def call_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == 'POST':
        visit_date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
        new_call = Appointment(patient_id=current_user.id, doctor_id=doctor.id, date=visit_date, status='Запланировано')
        db.session.add(new_call)
        db.session.commit()
        return redirect(url_for('doctor_profile', doctor_id=doctor_id))

    return render_template('call_doctor.html', doctor=doctor)



def add_doctors_to_db():
    doctors_list = [
        {
            "name": "Олег Олегович", 
            "specialization": "Кризисный врач", 
            "location": "Город 1", 
            "about": "Описание 1",
            "lat": 55.751244,
            "lng": 37.618423
        },
        {
            "name": "Анна Ивановна", 
            "specialization": "Терапевт", 
            "location": "Город 2", 
            "about": "Описание 2",
            "lat": 59.9342802,
            "lng": 30.3350986
        }
    ]

    for doc_info in doctors_list:
        if not Doctor.query.filter_by(name=doc_info["name"]).first():
            doctor = Doctor(
                name=doc_info["name"], 
                specialization=doc_info["specialization"], 
                location=doc_info["location"],
                about=doc_info["about"],
                lat=doc_info["lat"],
                lng=doc_info["lng"]
            )
            db.session.add(doctor)
    db.session.commit()

with app.app_context():
    db.create_all()
    add_doctors_to_db()

if __name__ == '__main__':
    app.run(debug=True)
