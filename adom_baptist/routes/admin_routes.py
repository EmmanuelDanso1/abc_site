from flask import Blueprint, render_template, redirect, url_for,jsonify, flash, send_from_directory, abort, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
# using the imports from __init__.py file
from adom_baptist.models import Admin
from adom_baptist import db, mail
from flask_mail import Message

from flask_wtf.csrf import generate_csrf,validate_csrf, CSRFError
import os
import json
from datetime import datetime
import requests

from adom_baptist.utils.util import UPLOAD_FOLDER, allowed_profile_pic,allowed_image_file, allowed_document, allowed_file

admin_bp = Blueprint('admin', __name__)

# admin dashbaord
@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if isinstance(current_user, Admin):
        return render_template('admin/admin_dashboard.html', admin=current_user)


# Profile picture upload
@admin_bp.route('/upload_admin_profile_pic', methods=['POST'])
@login_required
def upload_admin_profile_pic():
    if 'profile_pic' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    file = request.files['profile_pic']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.root_path, 'static/uploads/', filename)
        file.save(upload_path)

        # Delete old picture if it exists
        if current_user.profile_pic:
            try:
                old_path = os.path.join(current_app.root_path, 'static/uploads/', current_user.profile_pic)
                if os.path.exists(old_path):
                    os.remove(old_path)
            except Exception:
                pass

        current_user.profile_pic = filename
        db.session.commit()
        flash('Profile picture updated!', 'success')

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/delete_admin_profile_pic', methods=['POST'])
@login_required
def delete_admin_profile_pic():
    if current_user.profile_pic:
        try:
            os.remove(os.path.join(current_app.root_path, 'static/uploads/', current_user.profile_pic))
        except Exception:
            pass

        current_user.profile_pic = None
        db.session.commit()
        flash('Profile picture deleted.', 'info')

    return redirect(url_for('admin.admin_dashboard'))
