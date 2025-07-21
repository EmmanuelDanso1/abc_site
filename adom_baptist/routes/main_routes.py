from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from flask_mail import Mail,Message
from extensions import mail
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

# contact
@main_bp.route('/submit', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message_body = request.form['message']

    msg = Message(
        subject=f"Contact Form: {subject}",
        sender=email,
        recipients=[os.getenv('MAIL_USERNAME')]
    )

    msg.body = f"""
    You have received a new message from your website contact form:

    Name: {name}
    Email: {email}
    Subject: {subject}
    Message:
    {message_body}
    """

    try:
        mail.send(msg)
        flash("Your message has been sent to Realmindx successfully!", "success")
    except Exception as e:
        print(f"Mail sending failed: {e}")
        flash("An error occurred while sending your message. Please try again later.", "danger")

    return redirect(url_for('main.contact'))