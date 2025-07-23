from flask import Blueprint, render_template, session, redirect, url_for,jsonify, flash, send_from_directory, abort, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
# using the imports from __init__.py file
from adom_baptist.models import Admin, Sermon
from adom_baptist.forms import SermonForm
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

@admin_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('admin/settings.html')

# Sermon
@admin_bp.route('/upload-sermon', methods=['GET', 'POST'])
@login_required
def upload_sermon():
    form = SermonForm()
    if form.validate_on_submit():
        file = form.audio_file.data
        filename = secure_filename(file.filename)

        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'sermons')
        os.makedirs(upload_folder, exist_ok=True)

        full_path = os.path.join(upload_folder, filename)
        file.save(full_path)

        # Save only the filename
        sermon = Sermon(
            title=form.title.data,
            preacher=form.preacher.data,
            created_at=form.created_at.data,
            description=form.description.data,
            audio_file=filename,  
            admin_id=current_user.id
        )
        db.session.add(sermon)
        db.session.commit()
        flash('Sermon uploaded successfully!', 'success')
        return redirect(url_for('admin.upload_sermon'))

    return render_template('admin/upload_sermon.html', form=form)

# manage sermon
@admin_bp.route('/sermons/manage')
@login_required
def manage_sermons():
    sermons = Sermon.query.order_by(Sermon.created_at.desc()).all()
    return render_template('admin/manage_sermons.html', sermons=sermons)

# edit sermon
@admin_bp.route('/admin/sermons/<int:sermon_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_sermon(sermon_id):
    sermon = Sermon.query.get_or_404(sermon_id)

    if request.method == 'POST':
        # check for CSRF manually if implemented
        # token = session.get('_csrf_token')
        # if not token or token != request.form.get('csrf_token'):
        #     flash('Invalid CSRF token', 'danger')
        #     return redirect(url_for('admin.edit_sermon', sermon_id=sermon.id))

        sermon.title = request.form.get('title', '').strip()
        sermon.preacher = request.form.get('preacher', '').strip()
        sermon.description = request.form.get('description', '').strip()

        # Parse date safely
        created_at_str = request.form.get('created_at', '')
        try:
            sermon.created_at = datetime.strptime(created_at_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return render_template('admin/edit_sermon.html', sermon=sermon)

        # Commit changes
        db.session.commit()
        flash('Sermon updated successfully.', 'success')
        return redirect(url_for('admin.manage_sermons'))

    return render_template('admin/edit_sermon.html', sermon=sermon)

# delete
@admin_bp.route('/admin/sermons/<int:sermon_id>/delete', methods=['POST'])
@login_required
def delete_sermon(sermon_id):
    sermon = Sermon.query.get_or_404(sermon_id)
    db.session.delete(sermon)
    db.session.commit()
    flash('Sermon deleted successfully.', 'success')
    return redirect(url_for('admin.manage_sermons'))


