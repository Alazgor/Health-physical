from flask import make_response, flash, redirect, url_for, render_template, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from health import app, db
from health.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, UpdateUserRoleForm, EditUserForm, WorkoutForm, VerifySecretForm
from health.models import User, Workout
from health.utils import admin_required, generate_token, verify_token
from io import StringIO
import csv
from health.data_analysis import load_workouts_as_dataframe, plot_workouts_per_day, plot_calories_burned, analyze_workouts


@app.route('/', endpoint='index')
def home():
    app.logger.info(f'Home page accessed by user: {current_user}')
    return render_template('index.html', current_user=current_user)

@app.route('/about', endpoint='about')
def about():
    app.logger.info('About page accessed')
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            app.logger.info('Invalid email or password')
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        app.logger.info(f'User {user.email} logged in successfully')
        flash('Login successful!')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        app.logger.info(f'User {current_user.email} logged out')
        logout_user()
        flash('You have been logged out.')
    else:
        flash('No authenticated user.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                birth_date=form.birth_date.data,
                secret_question=form.secret_question.data  # Добавление secret_question
            )
            user.set_password(form.password.data)
            user.set_secret_answer(form.secret_answer.data)  # Установка секретного ответа
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            app.logger.info(f'User {user.email} registered successfully')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while registering the user: {str(e)}', 'danger')
            app.logger.error(f'Error during user registration: {str(e)}')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

@app.route('/request_reset_password', methods=['GET', 'POST'])
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Генерация токена и редирект на страницу ввода ответа на секретный вопрос
            token = generate_token(user.email)
            return redirect(url_for('verify_secret', token=token))
        else:
            flash('User with this email not found.')
            app.logger.warning(f'User with email {form.email.data} not found')

    return render_template('request_reset_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    email = verify_token(token)
    if email is None:
        flash('The reset password link is invalid or has expired.', 'danger')
        return redirect(url_for('request_reset_password'))
    user = User.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. Please log in with your new password.', 'success')
        return redirect(url_for('index'))
    return render_template('reset_password.html', form=form, token=token)



@app.route('/verify_secret/<token>', methods=['GET', 'POST'])
def verify_secret(token):
    email = verify_token(token)
    if email is None:
        flash('The reset password link is invalid or has expired.')
        return redirect(url_for('request_reset_password'))

    user = User.query.filter_by(email=email).first_or_404()
    form = VerifySecretForm(secret_question=user.secret_question)

    if form.validate_on_submit():
        if user.check_secret_answer(form.secret_answer.data):
            flash('Verification successful. Please set a new password.')
            return redirect(url_for('reset_password', token=token))
        else:
            flash('Incorrect answer to secret question.')

    return render_template('verify_secret.html', form=form, token=token)


@app.route('/admin/update_user_role', methods=['GET', 'POST'])
@login_required
@admin_required
def update_user_role():
    form = UpdateUserRoleForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.role = form.role.data
            db.session.commit()
            flash('User role updated successfully.')
        else:
            flash('User not found.')
        return redirect(url_for('admin_console'))
    return render_template('admin/update_user_role.html', form=form)

@app.route('/admin/admin_console')
@login_required
@admin_required
def admin_console():
    app.logger.info(f'Admin console accessed by user: {current_user}')
    users = User.query.all()
    return render_template('admin/admin_console.html', users=users)

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    app.logger.info(f'Admin dashboard accessed by user: {current_user}')
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@app.route('/admin/promote_to_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def promote_to_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.role = 'admin'
    db.session.commit()
    flash(f'{user.email} has been promoted to admin.')
    app.logger.info(f'User {user.email} promoted to admin by {current_user.email}')
    return redirect(url_for('admin_console'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} has been deleted.')
    app.logger.info(f'User {user.email} deleted by {current_user.email}')
    return redirect(url_for('admin_console'))


@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        app.logger.info('Form validated successfully.')
        app.logger.info(f'Form data: {form.data}')

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.birth_date = form.birth_date.data
        user.role = form.role.data

        # Обновление пароля, если он введен
        if form.password.data:
            app.logger.info(f'Updating password for user: {user.email}')
            user.set_password(form.password.data)

        db.session.commit()
        flash('User information has been updated.')
        return redirect(url_for('admin_console'))

    app.logger.info(f'Editing user {user.email}')
    return render_template('admin/edit_user.html', form=form, user=user)

@app.route('/workouts')
@login_required
def workouts():
    user_workouts = Workout.query.filter_by(user_id=current_user.id).all()
    app.logger.info(f'Workouts page accessed by user: {current_user.email}')
    return render_template('workouts.html', workouts=user_workouts)

calories_per_minute = {
    'bench_press': 0.106,
    'squats': 0.095,
    'deadlift': 0.125,
    'running': 0.15,
    'cycling': 0.12,
    'swimming': 0.13,
    'pull_ups': 0.1,
    'push_ups': 0.09,
    'jumping_jacks': 0.11,
    'burpees': 0.14,
    'rowing': 0.13,
    'yoga': 0.05
}

@app.route('/add_workout', methods=['GET', 'POST'])
@login_required
def add_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout_type = form.workout_type.data
        duration = float(form.duration.data)
        calories = duration * calories_per_minute[workout_type]
        workout = Workout(
            user_id=current_user.id,
            workout_type=workout_type,
            duration=duration,
            calories=calories,
            date=form.date.data
        )
        db.session.add(workout)
        db.session.commit()
        flash('Workout added successfully!', 'success')
        app.logger.info(f'Workout added for user: {current_user.email}')
        return redirect(url_for('index'))
    return render_template('add_workout.html', form=form)

@app.route('/export_csv')
@login_required
def export_csv():
    user_workouts = Workout.query.filter_by(user_id=current_user.id).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Workout Type', 'Duration (minutes)', 'Calories Burned'])
    for workout in user_workouts:
        cw.writerow([workout.date, workout.workout_type, workout.duration, workout.calories])
    response = make_response(si.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=workouts.csv'
    response.headers['Content-type'] = 'text/csv'
    app.logger.info(f'CSV export accessed by user: {current_user.email}')
    return response

@app.route('/analytics')
def analytics():
    df = load_workouts_as_dataframe()
    plot_workouts_per_day(df)
    plot_calories_burned(df)
    app.logger.info('Analytics page accessed')
    return render_template('analytics.html')

@app.route('/workout_analysis')
def workout_analysis():
    df = load_workouts_as_dataframe()
    workouts_per_day_img = plot_workouts_per_day(df)
    calories_burned_img = plot_calories_burned(df)
    app.logger.info('Workout analysis page accessed')
    return render_template('workout_analysis.html', workouts_per_day_img=workouts_per_day_img, calories_burned_img=calories_burned_img)

@app.route('/plot_workouts')
def plot_workouts():
    df = load_workouts_as_dataframe()
    img_bytes = plot_workouts_per_day(df)
    app.logger.info('Workouts plot accessed')
    return send_file(img_bytes, mimetype='image/png')

@app.route('/plot_calories')
def plot_calories():
    df = load_workouts_as_dataframe()
    img_bytes = plot_calories_burned(df)
    app.logger.info('Calories plot accessed')
    return send_file(img_bytes, mimetype='image/png')

@app.route('/delete_workout', methods=['POST'])
def delete_workout():
    data = request.get_json()
    date = data['date']
    workout_type = data['workout_type']
    workout = Workout.query.filter_by(date=date, workout_type=workout_type).first()
    if workout:
        db.session.delete(workout)
        db.session.commit()
        app.logger.info(f'Workout deleted: {date}, {workout_type} by user {current_user.email}')
        return jsonify({'success': True}), 200
    else:
        app.logger.info(f'Workout not found: {date}, {workout_type}')
        return jsonify({'error': 'Workout not found'}), 404

@app.route('/recommendations')
def recommendations_view():
    df = load_workouts_as_dataframe()
    recommendations = analyze_workouts(df)
    return render_template('recommendations.html', recommendations=recommendations)




