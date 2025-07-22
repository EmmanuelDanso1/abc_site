from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message
# using the content from __init__.py
from adom_baptist.models import Admin
from adom_baptist.forms import PasswordResetRequestForm, LoginForm, AdminSignupForm, PasswordResetForm
from adom_baptist import db, mail
import os

auth_bp = Blueprint('auth', __name__)
s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

@auth_bp.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    form = AdminSignupForm()
    if form.validate_on_submit():
        existing_admin = Admin.query.filter_by(email=form.email.data).first()
        if existing_admin:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('auth.admin_login'))

        hashed_pw = generate_password_hash(form.password.data)
        new_admin = Admin(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_admin)
        db.session.commit()

        login_user(new_admin)
        flash('Admin account created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))  

    return render_template('admin/admin_signup.html', form=form)

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('admin.admin_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('admin/admin_login.html', form=form)

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))  # adjust as needed

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin:
            token = s.dumps(admin.email, salt='password-reset-salt')
            reset_link = url_for('auth.reset_password', token=token, _external=True)

            try:
                msg = Message(
                    subject="Password Reset Request",
                    sender=os.getenv('MAIL_USERNAME'),
                    recipients=[admin.email]
                )
                msg.body = f"""
Hello {admin.username},

We received a request to reset your password.

Click the link below to reset it:
{reset_link}

If you did not request this, simply ignore this email.

Regards,
RealmIndx Support Team
"""
                mail.send(msg)
                flash('Password reset link has been sent to your email.', 'info')
            except Exception as e:
                print(f"Email sending failed: {e}")
                flash('Could not send email. Please try again later.', 'danger')
        else:
            flash('No account found with that email.', 'danger')
        return redirect(url_for('auth.admin_login'))

    return render_template('admin/forgot_password.html', form=form)

# password reset
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=email).first_or_404()
        admin.set_password(form.password.data)  # Ensure `set_password()` hashes and sets the password
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('auth.user_login'))

    return render_template('admin/reset_password.html', form=form)
