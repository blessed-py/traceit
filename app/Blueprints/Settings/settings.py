from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from app.Blueprints.Authentications.decorators import login_required, roles_required, flash
from app.Database.database import DatabaseManager
from app.Database.encrypter import Cryptography
import os
from uuid import uuid4
from werkzeug.utils import secure_filename

# Blueprint initialization
settings_bp = Blueprint('settings', __name__, template_folder='templates')


# Base directory of your project (contentpro)
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

STORAGE_DIR = os.path.join(BASE_DIR, "Storage")

UPLOAD_PFP_FOLDER = os.path.join(STORAGE_DIR, "pfp")



# Database instance
db_manager = DatabaseManager()
# Encryption instance
cryptographer = Cryptography()

@settings_bp.route('/settings/manage_testimonial')
@login_required
def manage_testimonial():
    current_user = g.current_user
    sys_testimonials = db_manager.get_system_testimonials()
    total_testimonials = db_manager.get_total_testimonials_count()
    pending_testimonials = db_manager.get_pending_testimonials_count()
    approved_testimonials =  db_manager.get_approved_testimonials_count()
    hidden_testimonials = db_manager.get_hidden_testimonials_count()
    return render_template('manage_testimonial.html',
                           current_user = current_user,
                           sys_testimonials=sys_testimonials,
                           total_testimonials = total_testimonials,
                           pending_testimonials = pending_testimonials,
                           approved_testimonials = approved_testimonials,
                           hidden_testimonials = hidden_testimonials                      
                           )

# ===========================
# Admin: Add Testimonial
# ===========================
@settings_bp.route('/settings/add_testimonial', methods=['POST'])
def add_testimonial():
    name = request.form['name']
    job_title = request.form['job_title']
    message = request.form['message']

    testimonial_id = cryptographer.generate_unique_id()

    success, feedback = db_manager.add_testimonial(
        testimonial_id=testimonial_id,
        name=name,
        job_title=job_title,
        message=message,
        consent=1  # admin always public
    )

    return jsonify({'success': success, 'feedback': feedback})


@settings_bp.route('/settings/edit_testimonial', methods=['POST'])
def edit_testimonial():
    try:
        data = request.get_json()

        testimonial_id = data.get('testimonial_id')
        name = data.get('name')
        job_title = data.get('job_title')
        message = data.get('message')
        status = data.get('status')
        priority = data.get('priority')

        # Convert priority to int if provided
        if priority in (None, '', 'null'):
            priority = None
        else:
            try:
                priority = int(priority)
            except ValueError:
                return jsonify({'success': False, 'feedback': 'Invalid priority value.'}), 400

        success, feedback = db_manager.edit_testimonial(
            testimonial_id, name, job_title, message, status, priority
        )

        if success:
            return jsonify({'success': True, 'feedback': feedback})
        else:
            return jsonify({'success': False, 'feedback': feedback}), 400

    except Exception as e:
        print("[ERROR] Editing testimonial:", e)
        return jsonify({'success': False, 'feedback': 'Unexpected error occurred.'}), 500


@settings_bp.route('/settings/delete_testimonial', methods=['POST'])
def delete_testimonial():
    try:
        data = request.get_json()
        testimonial_id = data.get('testimonial_id')

        if not testimonial_id:
            return jsonify({'success': False, 'feedback': 'Testimonial ID is required.'}), 400

        # Call DB function
        success, feedback = db_manager.delete_testimonial(testimonial_id)

        return jsonify({'success': success, 'feedback': feedback}), (200 if success else 400)

    except Exception as e:
        print("[ERROR] Deleting testimonial:", e)
        return jsonify({'success': False, 'feedback': 'Unexpected error occurred.'}), 500