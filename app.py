from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import flash
from math import cos, asin, sqrt
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

app = Flask(__name__)

# Конфигурация приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'your-secret-key'

# Инициализация расширений
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" 

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
    phone_number = db.Column(db.String(15))

# Модель доктора
class Doctor(UserMixin, db.Model):
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
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
<<<<<<< HEAD
    user = User.query.get(int(user_id))
    if user:
        return user
    return Doctor.query.get(int(user_id))
=======
    # Используем контекст сессии для запроса пользователя
    with db.session.no_autoflush:
        user = db.session.get(User, int(user_id))
        if user:
            return user
        return db.session.get(Doctor, int(user_id))
>>>>>>> origin/develop


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('search'))
        else:
            error = 'Неверное имя пользователя или пароль'

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')
        full_name = request.form.get('full_name')

        if not all([username, password, phone_number, full_name]):
            error = 'Все поля должны быть заполнены'
        elif len(password) < 6:
            error = 'Пароль должен содержать не менее 6 символов'
        elif User.query.filter_by(username=username).first():
            error = 'Пользователь с таким именем уже существует'
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password, full_name=full_name, phone_number=phone_number)
            db.session.add(new_user)
            try:
                db.session.commit()
                return redirect(url_for('login'))
            except Exception as e:
                logger.error(f"Ошибка при регистрации: {e}")
                error = 'Ошибка при регистрации. Пожалуйста, попробуйте снова.'

    return render_template('register.html', error=error)




@app.route('/doctor_register', methods=['GET', 'POST'])
def doctor_register():
    if request.method == 'POST':
        username = request.form['username']
        hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_doctor = Doctor(username=username, password=hashed_password)
        
        # Проверка, существует ли уже такой пользователь
        if Doctor.query.filter_by(username=username).first():
            return 'Пользователь с таким именем уже существует'

        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('doctor_login'))

    return render_template('doctor_register.html')

@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        doctor = Doctor.query.filter_by(username=username).first()
        if doctor and check_password_hash(doctor.password, password):
            login_user(doctor)
            return redirect(url_for('doctor_dashboard'))
        else:
            return 'Неверное имя пользователя или пароль'

    return render_template('doctor_login.html')


@app.route('/doctor_register', methods=['GET', 'POST'])
def doctor_register():
    if request.method == 'POST':
        username = request.form['username']
        hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_doctor = Doctor(username=username, password=hashed_password)
        
        # Проверка, существует ли уже такой пользователь
        if Doctor.query.filter_by(username=username).first():
            return 'Пользователь с таким именем уже существует'

        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('doctor_login'))

    return render_template('doctor_register.html')

@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        doctor = Doctor.query.filter_by(username=username).first()
        if doctor and check_password_hash(doctor.password, password):
            login_user(doctor)
            return redirect(url_for('doctor_dashboard'))
        else:
            return 'Неверное имя пользователя или пароль'

    return render_template('doctor_login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

STATIC_LAT = 55.7558  # Местоположение Пациента
STATIC_LNG = 37.6173  # Местоположение пациента


@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    specialization = request.args.get('specialization', None)
    max_distance_str = request.args.get('max_distance', None)
    sort_by = request.args.get('sort_by', '')

<<<<<<< HEAD
    doctors_query = Doctor.query
=======
    doctors_query = Doctor.query.filter(Doctor.available == True)
>>>>>>> origin/develop

    if query:
        doctors_query = doctors_query.filter(
            Doctor.name.contains(query) | Doctor.specialization.contains(query)
        )

    if specialization:
        doctors_query = doctors_query.filter(Doctor.specialization == specialization)
<<<<<<< HEAD

=======
>>>>>>> origin/develop
    # Преобразование строки расстояния в число и фильтрация
    max_distance = None
    if max_distance_str:
        try:
            max_distance = float(max_distance_str)
        except ValueError:
            pass  # Неверный формат строки расстояния

    # Инициализация переменной doctors
    doctors = doctors_query.all()

    for doctor in doctors:
        doctor.distance = distance(STATIC_LAT, STATIC_LNG, doctor.lat, doctor.lng)

    if max_distance is not None:
        doctors = [doctor for doctor in doctors 
                   if distance(STATIC_LAT, STATIC_LNG, doctor.lat, doctor.lng) <= max_distance]

    # Сортировка результатов
    if sort_by:
        if sort_by == "distance_asc":
            # Сортировка по расстоянию (по возрастанию)
            pass
        elif sort_by == "distance_desc":
            # Сортировка по расстоянию (по убыванию)
            pass
        elif sort_by == "name_asc":
            doctors = sorted(doctors, key=lambda d: d.name)
        elif sort_by == "name_desc":
            doctors = sorted(doctors, key=lambda d: d.name, reverse=True)

    return render_template('search.html', doctors=doctors)





@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
<<<<<<< HEAD
    if not isinstance(current_user, Doctor):
        # Перенаправление не-врачей на главную страницу
        return redirect(url_for('index'))

    # Получаем заявки, адресованные текущему врачу
    appointments = Appointment.query.filter_by(doctor_id=current_user.id).all()

    # Получаем отзывы, оставленные для врача
    reviews = Review.query.filter_by(doctor_id=current_user.id).all()

    # Формируем данные для отображения в шаблоне
    appointments_data = []
    for appointment in appointments:
        patient = User.query.get(appointment.patient_id)
        appointments_data.append({
            'appointment_id': appointment.id,
            'patient_name': patient.full_name,
            'date': appointment.date.strftime("%Y-%m-%d %H:%M"),
            'status': appointment.status
        })

    return render_template('doctor_dashboard.html', appointments=appointments_data, reviews=reviews)
=======
    logger.debug("Доступ к странице doctor_dashboard пользователем: %s", current_user.get_id())
    real_user = db.session.query(Doctor).get(current_user.get_id())
    if real_user:
        appointments = (db.session.query(Appointment, User)
                    .join(User, Appointment.patient_id == User.id)
                    .filter(Appointment.doctor_id == real_user.id)
                    .all())

        appointments_data = [{
            'appointment_id': appointment.id,
            'patient_name': patient.full_name,
            'patient_phone': patient.phone_number,
            'date': appointment.date.strftime("%Y-%m-%d %H:%M"),
            'status': appointment.status
            } for appointment, patient in appointments]
        logger.debug("Заявки для врача с ID %s: %s", real_user.id, appointments_data)
        return render_template('doctor_dashboard.html', appointments=appointments_data)
    else:
        logger.warning("Врач с ID %s не найден", current_user.get_id())
        return redirect(url_for('index'))
>>>>>>> origin/develop


@app.route('/doctor/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
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
    if not doctor.available:
        flash("Врач в данный момент недоступен", "error")
        return redirect(url_for('doctor_profile', doctor_id=doctor_id))
    if request.method == 'POST':
        try:
            if 'date' not in request.form:
                raise ValueError("Дата не указана")
            visit_date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
            new_call = Appointment(patient_id=current_user.id, doctor_id=doctor.id, date=visit_date, status='Запланировано')
            db.session.add(new_call)
            db.session.commit()
            flash("Вы успешно записались на прием к врачу", "success")
            logger.info(f"Заявка от пациента с ID {current_user.id} для врача с ID {doctor.id} на {visit_date} успешно создана.")
        except ValueError as e:
            flash(f"Ошибка при создании заявки: {e}", "error")
            logger.error(f"Ошибка при создании заявки: {e}")
        return redirect(url_for('doctor_profile', doctor_id=doctor_id))
    return render_template('call_doctor.html', doctor=doctor)

@app.route('/edit_doctor_profile/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def edit_doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        doctor.name = request.form.get('name')
        doctor.specialization = request.form.get('specialization')
        doctor.about = request.form.get('about')
        doctor.location = request.form.get('location')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
<<<<<<< HEAD
        doctor.available = 'available' in request.form
=======
        
        doctor.available = request.form.get('available') == 'on'
>>>>>>> origin/develop

        doctor.lat = float(lat) if lat and lat != 'None' else None
        doctor.lng = float(lng) if lng and lng != 'None' else None
        db.session.commit()
        return redirect(url_for('doctor_dashboard'))

    return render_template('edit_doctor_profile.html', doctor=doctor)
<<<<<<< HEAD

=======
>>>>>>> origin/develop



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
