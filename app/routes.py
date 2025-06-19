from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from . import db, bcrypt, mail
from .models import User, LifestyleData, Doctor, Appointment
from .predictor import predict_health
from sqlalchemy import func
from datetime import datetime, date, timedelta
import numpy as np
from flask import make_response
from flask_mail import Message
from xhtml2pdf import pisa
from io import BytesIO

auth = Blueprint('auth', __name__)




















# Chatbot response logic
def get_chatbot_response(message):
    message = message.lower().strip()

    responses = {
        "hi": "Hello! I'm ChronoCare's Health Assistant. How can I help you today with your health?",
        "hello": "Hi there! I'm here to assist with your health questions. What would you like to know?",
        "diet tips": "Here are some diet tips:\n- Eat a balanced diet with plenty of fruits and vegetables.\n- Limit processed foods and sugars.\n- Stay hydrated by drinking 8 glasses of water daily.\n- Include lean proteins like chicken, fish, or beans.\nWould you like more specific advice?",
        "health tips": "Here are some general health tips:\n- Aim for 7–8 hours of sleep each night.\n- Exercise at least 30 minutes a day.\n- Manage stress with mindfulness or meditation.\n- Get regular check-ups with your doctor.\nAnything specific you’d like to focus on?",
        "nutrition": "For better nutrition:\n- Focus on whole foods like grains, nuts, and seeds.\n- Avoid trans fats and limit saturated fats.\n- Include healthy fats from avocados, olive oil, and fish.\n- Watch portion sizes to avoid overeating.\nWould you like a meal plan suggestion?",
        "exercise": "Regular exercise is key! Here are some tips:\n- Aim for 150 minutes of moderate activity weekly (like brisk walking).\n- Include strength training twice a week.\n- Stretch daily to improve flexibility.\n- Find an activity you enjoy to stay motivated.\nNeed a workout plan?",
        "stress": "Managing stress is important for your health:\n- Try deep breathing exercises or meditation.\n- Take short breaks during work to relax.\n- Stay connected with friends and family.\n- Consider journaling to process your thoughts.\nWould you like more stress-relief techniques?",
        "sleep": "Good sleep is crucial:\n- Stick to a consistent sleep schedule.\n- Avoid screens 1 hour before bed.\n- Create a relaxing bedtime routine.\n- Keep your bedroom dark and cool.\nHaving trouble sleeping?",
        "weight loss": "For healthy weight loss:\n- Focus on a calorie deficit (burn more than you consume).\n- Eat high-fiber foods to stay full longer.\n- Exercise regularly, mixing cardio and strength training.\n- Avoid crash diets; aim for sustainable changes.\nNeed a personalized plan?",
        "thank you": "You're welcome! If you have more questions, feel free to ask. Stay healthy!",
        "bye": "Goodbye! Take care of your health, and feel free to come back anytime!"
    }

    for key, response in responses.items():
        if key in message:
            return response

    return "I'm sorry, I didn't understand that. Could you please ask about health tips, diet, exercise, or stress management? I'm here to help!"

@auth.route('/')
def redirect_to_intro():
    return redirect(url_for('auth.intro'))

@auth.route('/intro')
def intro():
    return render_template('intro.html')

@auth.route('/home')
def home():
    return render_template('index.html')

@auth.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Send email
        msg = Message(
            subject=subject,
            recipients=['sushanthreddy717@gmail.com'],
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        try:
            mail.send(msg)
            flash('Your message has been sent! We will get back to you soon.', 'success')
        except Exception as e:
            flash('Failed to send your message. Please try again later.', 'danger')
            print(f"Error sending email: {str(e)}")

        return redirect(url_for('auth.home'))

    return render_template('contact.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, username=username, password=hashed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('auth.lifestyle_form'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')
"""

#use eprevious login route if u ahve any issues, this altest with login error message sif wrong details
#also i adeed  6 lines of code to login.html for this at 35th line

"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('auth.lifestyle_form'))
            else:
                flash('Incorrect password. Please try again.', 'danger')
        else:
            flash('No account found with this email.', 'danger')

    return render_template('login.html')

"""


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle JSON request (API)
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            user = User.query.filter_by(email=email).first()

            if user and bcrypt.check_password_hash(user.password, password):
                return jsonify({"token": "mocked_token"}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401

        # Handle form submission (HTML form)
        else:
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user:
                if bcrypt.check_password_hash(user.password, password):
                    session['user_id'] = user.id
                    return redirect(url_for('auth.lifestyle_form'))
                else:
                    flash('Incorrect password. Please try again.', 'danger')
            else:
                flash('No account found with this email.', 'danger')

    return render_template('login.html')



@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.home'))

@auth.route('/lifestyle_form')
def lifestyle_form():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('lifestyle_form.html')

@auth.route('/lifestyle', methods=['POST'])
def lifestyle():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    entry = LifestyleData(
        user_id=session['user_id'],
        sleep_hours=float(request.form['sleep_hours']),
        diet_quality=request.form['diet_quality'],
        exercise_minutes=int(request.form['exercise_minutes']),
        stress_level=request.form['stress_level'],
        timestamp=datetime.utcnow()
    )
    db.session.add(entry)
    db.session.commit()

    flash('Lifestyle data submitted successfully!', 'success')
    return redirect(url_for('auth.dashboard'))

@auth.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    uid = session['user_id']

    entries = LifestyleData.query.filter_by(user_id=uid) \
        .order_by(LifestyleData.timestamp.desc()).all()

    avg_sleep = db.session.query(func.avg(LifestyleData.sleep_hours)) \
                    .filter_by(user_id=uid).scalar() or 0
    avg_exercise = db.session.query(func.avg(LifestyleData.exercise_minutes)) \
                       .filter_by(user_id=uid).scalar() or 0

    raw_stress = db.session.query(
        LifestyleData.stress_level,
        func.count().label('count')
    ).filter_by(user_id=uid).group_by(LifestyleData.stress_level).all()
    stress_labels = [lvl for lvl, _ in raw_stress]
    stress_counts = [cnt for _, cnt in raw_stress]

    suggestions = []
    if avg_sleep < 7:
        suggestions.append("Try to get at least 7–8 hours of sleep each night.")
    elif avg_sleep > 9:
        suggestions.append("Aim for 7–9 hours of sleep.")
    if avg_exercise < 30:
        suggestions.append("Increase exercise to ≥30 mins/day.")
    else:
        suggestions.append("Great job on exercise!")
    if raw_stress:
        top = max(raw_stress, key=lambda x: x[1])[0].lower()
        if top == 'high':
            suggestions.append("Practice stress‐reduction techniques.")
        elif top == 'moderate':
            suggestions.append("Maintain your stress‐management habits.")
        else:
            suggestions.append("Your stress levels are low—well done!")

    valid_entries = [e for e in entries if e.timestamp is not None]
    chart_labels = [e.timestamp.strftime("%Y-%m-%d") for e in valid_entries]
    sleep_data = [e.sleep_hours for e in valid_entries]
    exercise_data = [e.exercise_minutes for e in valid_entries]

    return render_template('dashboard.html',
                           avg_sleep=round(avg_sleep, 2),
                           avg_exercise=round(avg_exercise, 2),
                           suggestions=suggestions,
                           chart_labels=chart_labels,
                           sleep_data=sleep_data,
                           exercise_data=exercise_data,
                           stress_labels=stress_labels,
                           stress_counts=stress_counts,
                           entries=entries)

@auth.route('/predict')
def predict():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    uid = session['user_id']

    data_entries = LifestyleData.query.filter_by(user_id=uid) \
        .order_by(LifestyleData.timestamp.desc()).all()
    data = [{
        'sleep_hours': e.sleep_hours,
        'exercise_minutes': e.exercise_minutes,
        'stress_level': e.stress_level
    } for e in data_entries]

    result = predict_health(data)
    return render_template('predict.html',
                           health_score=result['health_score'],
                           years_left=result['years_left'],
                           recommendations=result['recommendations'])

@auth.route('/forecast')
def forecast():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    uid = session['user_id']

    raw_entries = (LifestyleData.query
                   .filter_by(user_id=uid)
                   .order_by(LifestyleData.timestamp.asc())
                   .all())

    entries = [e for e in raw_entries if e.timestamp is not None]

    if len(entries) < 2:
        flash("Not enough data to forecast. Submit more lifestyle entries first.", "warning")
        return redirect(url_for('auth.dashboard'))

    x = np.arange(len(entries))
    sleep_y = np.array([e.sleep_hours for e in entries])
    exercise_y = np.array([e.exercise_minutes for e in entries])

    sleep_coef = np.polyfit(x, sleep_y, 1)
    exer_coef = np.polyfit(x, exercise_y, 1)

    future_x = np.arange(len(entries), len(entries) + 7)
    sleep_forecast = list(np.polyval(sleep_coef, future_x))
    exer_forecast = list(np.polyval(exer_coef, future_x))

    last_date = entries[-1].timestamp
    future_dates = [
        (last_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(1, 8)
    ]

    past_labels = [e.timestamp.strftime("%Y-%m-%d") for e in entries]
    past_sleep = [e.sleep_hours for e in entries]
    past_exercise = [e.exercise_minutes for e in entries]

    return render_template('forecast.html',
                           past_labels=past_labels,
                           past_sleep=past_sleep,
                           past_exercise=past_exercise,
                           future_labels=future_dates,
                           sleep_forecast=sleep_forecast,
                           exer_forecast=exer_forecast)

@auth.route('/insights')
def insights():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    entries = LifestyleData.query.filter_by(user_id=user_id).order_by(LifestyleData.timestamp.desc()).limit(7).all()

    if not entries:
        flash("No lifestyle entries found to analyze.", "warning")
        return redirect(url_for('auth.dashboard'))

    avg_sleep = sum(e.sleep_hours for e in entries) / len(entries)
    avg_exercise = sum(e.exercise_minutes for e in entries) / len(entries)
    stress_levels = [e.stress_level for e in entries]

    if avg_sleep >= 8:
        sleep_quality = "Excellent"
        sleep_tip = "Great job maintaining a healthy sleep schedule!"
    elif avg_sleep >= 6.5:
        sleep_quality = "Good"
        sleep_tip = "Doing well! Try sticking to consistent sleep hours."
    elif avg_sleep >= 5:
        sleep_quality = "Average"
        sleep_tip = "Try going to bed earlier and avoiding screens at night."
    else:
        sleep_quality = "Poor"
        sleep_tip = "Lack of sleep can hurt your health. Try to sleep more."

    if avg_exercise >= 30:
        exercise_tip = "You're getting solid daily exercise! Keep it up."
    elif avg_exercise >= 15:
        exercise_tip = "Some activity is better than none—try increasing it a bit!"
    else:
        exercise_tip = "Very low activity—start with short walks or stretches."

    stress_summary = {
        "Low": stress_levels.count("Low"),
        "Moderate": stress_levels.count("Moderate"),
        "High": stress_levels.count("High")
    }

    return render_template("insights.html",
                           avg_sleep=round(avg_sleep, 1),
                           avg_exercise=round(avg_exercise, 1),
                           sleep_quality=sleep_quality,
                           sleep_tip=sleep_tip,
                           exercise_tip=exercise_tip,
                           stress_summary=stress_summary)

@auth.route('/report')
def generate_report():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    uid = session['user_id']

    entries = LifestyleData.query.filter_by(user_id=uid).order_by(LifestyleData.timestamp.desc()).limit(7).all()

    if not entries:
        flash("No data found for report.", "warning")
        return redirect(url_for('auth.dashboard'))

    avg_sleep = round(sum(e.sleep_hours for e in entries) / len(entries), 2)
    avg_exercise = round(sum(e.exercise_minutes for e in entries) / len(entries), 2)
    most_common_stress = max(set([e.stress_level for e in entries]), key=[e.stress_level for e in entries].count)
    diet_qualities = [e.diet_quality for e in entries]
    most_common_diet = max(set(diet_qualities), key=diet_qualities.count)

    sleep_tip = "Try to get more rest." if avg_sleep < 7 else "Great sleep habits!"
    exercise_tip = "Aim for 30+ mins daily." if avg_exercise < 30 else "Excellent activity levels!"
    stress_tip = f"Stress Level: {most_common_stress}"

    entries_full = LifestyleData.query.filter_by(user_id=uid).order_by(LifestyleData.timestamp.asc()).all()
    x = np.arange(len(entries_full))
    sleep_y = np.array([e.sleep_hours for e in entries_full])
    exercise_y = np.array([e.exercise_minutes for e in entries_full])
    sleep_forecast = list(np.polyval(np.polyfit(x, sleep_y, 1), np.arange(len(entries_full), len(entries_full) + 7)))
    exer_forecast = list(np.polyval(np.polyfit(x, exercise_y, 1), np.arange(len(entries_full), len(entries_full) + 7)))

    forecast = list(zip(
        [(entries_full[-1].timestamp + timedelta(days=i + 1)).strftime("%Y-%m-%d") for i in range(7)],
        sleep_forecast,
        exer_forecast
    ))

    data = [{
        'sleep_hours': e.sleep_hours,
        'exercise_minutes': e.exercise_minutes,
        'stress_level': e.stress_level
    } for e in entries]
    result = predict_health(data)

    html = render_template("report_template.html",
                           avg_sleep=avg_sleep,
                           avg_exercise=avg_exercise,
                           diet=most_common_diet,
                           stress=most_common_stress,
                           sleep_tip=sleep_tip,
                           exercise_tip=exercise_tip,
                           stress_tip=stress_tip,
                           forecast=forecast,
                           health_score=result['health_score'],
                           years_left=result['years_left'],
                           recommendations=result['recommendations'])

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)
    if pisa_status.err:
        flash("PDF generation failed.", "danger")
        return redirect(url_for('auth.dashboard'))

    pdf.seek(0)
    response = make_response(pdf.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=lifestyle_report.pdf'
    return response


#Appoinments

@auth.route('/appointments')
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']

    doctors = Doctor.query.all()
    user_appointments = Appointment.query.filter_by(user_id=user_id, status='booked').all()
    return render_template('appointment.html', doctors=doctors, appointments=user_appointments)

@auth.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'specialty': d.specialty
    } for d in doctors])

#slots...
@auth.route('/api/slots/<int:doctor_id>', methods=['GET'])
def get_slots(doctor_id):
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    all_slots = ["09:00 AM", "10:00 AM", "11:00 AM"]
    booked_slots = Appointment.query.filter_by(doctor_id=doctor_id, date=selected_date, status='booked').all()
    booked_times = [slot.time_slot for slot in booked_slots]

    available_slots = [slot for slot in all_slots if slot not in booked_times]
    return jsonify({'slots': available_slots})

@auth.route('/api/appointments/book', methods=['POST'])
def book_appointment():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    doctor_id = data.get('doctor_id')
    date_str = data.get('date')
    time_slot = data.get('time_slot')

    if not all([doctor_id, date_str, time_slot]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    existing = Appointment.query.filter_by(
        doctor_id=doctor_id,
        date=selected_date,
        time_slot=time_slot,
        status='booked'
    ).first()
    if existing:
        return jsonify({'error': 'Slot already booked'}), 400

    appointment = Appointment(
        user_id=session['user_id'],
        doctor_id=doctor_id,
        date=selected_date,
        time_slot=time_slot,
        status='booked'
    )
    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment booked successfully'})

@auth.route('/api/appointments/cancel/<int:appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403

    appointment.status = 'cancelled'
    db.session.commit()

    return jsonify({'message': 'Appointment cancelled successfully'})

@auth.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if 'chatbot_visited' not in session:
        session['chatbot_visited'] = True
        initial_message = "Hello! I'm ChronoCare's Health Assistant. How can I help you today with your health?"
    else:
        initial_message = None

    user_message = None
    bot_response = None

    if request.method == 'POST':
        user_message = request.form.get('message')
        if user_message:
            bot_response = get_chatbot_response(user_message)

    return render_template('chatbot.html', initial_message=initial_message, user_message=user_message, bot_response=bot_response)

















@auth.route('/farewell')
def farewell():
    return render_template('farewell.html')