from flask import make_response, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user, login_required
from health import app, db
from health.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, UpdateUserRoleForm, EditUserForm, WorkoutForm
from health.models import User, Workout
from health.utils import admin_required, send_email
from health.send_email import send_password_reset_email
from io import StringIO
import csv
from flask import render_template, send_file
from health.data_analysis import load_workouts_as_dataframe, plot_workouts_per_day, plot_calories_burned

@app.route('/', endpoint='index')
def home():
    return render_template('index.html', current_user=current_user)

@app.route('/about', endpoint='about')
def about():
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
        app.logger.info('Login successful!')
        flash('Login successful!')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout', endpoint='logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
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
                is_admin=form.is_admin.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            app.logger.info('User registered successfully')
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
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password.')
        else:
            flash('User not found.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('The reset password link is invalid or has expired. Please try again.')
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)

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
    users = User.query.all()
    return render_template('admin/admin_console.html', users=users)

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
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
    return redirect(url_for('admin_console'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} has been deleted.')
    return redirect(url_for('admin_console'))


@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User information has been updated.')
        return redirect(url_for('admin_console'))
    return render_template('admin/edit_user.html', form=form, user=user)

@app.route('/workouts')
@login_required
def workouts():
    user_workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return render_template('workouts.html', workouts=user_workouts)

# calibrated dictionary for excersises
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
    return response
@app.route('/analytics')
def analytics():
    df = load_workouts_as_dataframe()
    plot_workouts_per_day(df)
    plot_calories_burned(df)
    return render_template('analytics.html')

@app.route('/workout_analysis')
def workout_analysis():
    df = load_workouts_as_dataframe()
    # Graph generation workouts_per_day
    workouts_per_day_img = plot_workouts_per_day(df)
    # Graph generation calories_burned
    calories_burned_img = plot_calories_burned(df)

    return render_template('workout_analysis.html', workouts_per_day_img=workouts_per_day_img, calories_burned_img=calories_burned_img)