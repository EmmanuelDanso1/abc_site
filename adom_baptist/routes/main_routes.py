from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from flask_mail import Mail,Message
from extensions import mail, db
from adom_baptist.models import Sermon
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    if current_user.is_authenticated and current_user.is_admin:
        # Redirect admin to the member dashboard
        return redirect(url_for('admin.manage_members'))  # or your renamed route
    return render_template('home.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

# sermon playback
@main_bp.route('/sermons/<int:sermon_id>')
def sermon_playback(sermon_id):
    sermon = Sermon.query.get_or_404(sermon_id)
    return render_template('sermon_playback.html', sermon=sermon)

# search for preacher or date
@main_bp.route('/sermons')
def sermons():
    preacher = request.args.get('preacher')
    date = request.args.get('date')
    
    query = Sermon.query

    if preacher:
        query = query.filter(Sermon.preacher.ilike(f'%{preacher}%'))
    if date:
        # db.func.date(...) extracts only the date part from a DateTime column.
        # <- Updated for date string matching
        query = query.filter(db.func.date(Sermon.created_at) == date)  

    sermons = query.order_by(Sermon.created_at.desc()).all() 
    return render_template('sermons.html', sermons=sermons)


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