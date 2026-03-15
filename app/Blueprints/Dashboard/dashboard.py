from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify, session, current_app
from app.Blueprints.Authentications.decorators import login_required, roles_required, flash
from app.Database.database import DatabaseManager
from app.Database.encrypter import Cryptography
from app.API.SMTP import MAIL_SERVER
import os
from uuid import uuid4
from werkzeug.utils import secure_filename

# Blueprint initialization
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

# Encryption instance
cryptographer = Cryptography()

# Database instance
db_manager = DatabaseManager()

mail_server = MAIL_SERVER()

# Base directory of the project 
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")

)

STORAGE_DIR = os.path.join(BASE_DIR, "Storage")

UPLOAD_ITEM_FOUND_FOLDER = os.path.join(STORAGE_DIR, "item_found")
UPLOAD_PFP_FOLDER = os.path.join(STORAGE_DIR, "pfp")



os.makedirs(UPLOAD_ITEM_FOUND_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_PFP_FOLDER, exist_ok=True)



@dashboard_bp.route('/sys/dashboard')
@login_required
def dashboard():
    current_user = g.current_user
    return render_template('dashboard.html',
                           current_user = current_user)

@dashboard_bp.route('/sys/profile')
@login_required
def profile():
    current_user = g.current_user
    return render_template('profile.html',
                           current_user = current_user                      
                           )

@dashboard_bp.route('/settings/profile/upload_photo', methods=['POST'])
def upload_profile_photo():
    file = request.files.get('profile_picture')
    if not file:
        return jsonify({'success': False, 'feedback': 'No file uploaded'})

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'feedback': 'User not logged in'})

    try:
        # Generate new file name
        new_filename = f"{uuid4().hex}.png"
        save_path = os.path.join(UPLOAD_PFP_FOLDER, new_filename)

        # Save new file first
        file.save(save_path)

        # Update DB and get old picture
        success, old_picture = db_manager.update_user_profile_picture(user_id, new_filename)
        if not success:
            # Roll back: delete the newly saved file
            if os.path.exists(save_path):
                os.remove(save_path)
            return jsonify({'success': False, 'feedback': 'Database update failed'})

        # Delete old picture if it exists
        if old_picture:
            old_path = os.path.join(UPLOAD_PFP_FOLDER, old_picture)
            if os.path.exists(old_path):
                os.remove(old_path)

        return jsonify({'success': True, 'feedback': 'Profile picture updated successfully!'})

    except Exception as e:
        print("[ERROR]", e)
        return jsonify({'success': False, 'feedback': 'Upload failed'})
    
@dashboard_bp.route('/sys/system_user')
@login_required
def system_user():
    current_user = g.current_user    
    sys_users=db_manager.get_system_users()
    sys_roles = db_manager.get_system_roles()
    users = db_manager.get_system_user_info()
    total_system_users = db_manager.get_total_system_users()
    admin_users_count = db_manager.get_admin_users_count()
    system_maintainer_count = db_manager.get_system_maintainer_count()
    blocked_users_count = db_manager.get_blocked_users_count()
    return render_template('system_user.html',
                           current_user = current_user,
                           sys_users=sys_users,
                           sys_roles=sys_roles,
                           users=users,
                           total_system_users = total_system_users, 
                           admin_users_count = admin_users_count,
                           system_maintainer_count = system_maintainer_count,
                           blocked_users_count = blocked_users_count)

@dashboard_bp.route('/sys/change_status', methods=['POST'])
def change_user_status():
    data = request.get_json()
    status = data.get('status')
    user_id = data.get('user_id')
    success, feedback = db_manager.change_user_status(user_id, status)
    if success:
        return jsonify({'success': success, 'feedback': feedback})
    return jsonify({'success': False, 'feedback': feedback}), 400

@dashboard_bp.route('/sys/add_user', methods=['POST'])
def add_system_user():
    # Get form data
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    sur_name = request.form.get('sur_name')
    gender = request.form.get('gender')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    user_role = request.form.get('user_role')
    password = request.form.get('password')

    success, message = db_manager.add_system_user(
        first_name=first_name,
        middle_name=middle_name,
        sur_name=sur_name,
        gender=gender,
        email=email,
        phone_number=phone_number,
        role_id=user_role,
        password=password
    )

    if success:
        full_name = f"{first_name} {sur_name}"
        login_link = url_for(
        'auth.logout',
        _external=True
        )

        mail_server.send_html_email(
            email,
            "Your system account has been created!",
            f"""
            <p>Hi {full_name},</p>

            <p>Your account has been successfully created on the system.</p>

            <p><b>Login Email:</b> {email}</p>
            <p><b>Temporary Password:</b> {password}</p>

            <p>Please log in and change your password immediately for security reasons.</p>

            <p>
            <br>
                <a href="{login_link}" 
                   style="padding:10px 16px;background:#3085d6;color:#fff;text-decoration:none;border-radius:4px;">
                   Login to System
                </a>
            </p>
            <br>
            <p>Best regards,<br><strong>
            SYSTEM MAINTAINER</strong></p>
            """
        )

    return jsonify({
        "success": success,
        "message": message
    })
    
@dashboard_bp.route('/sys/edit_user', methods=['POST'])
def edit_user():
    try:
        data = request.get_json() 

        user_id = data.get('user_id')
        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        sur_name = data.get('sur_name')
        gender = data.get('gender')
        email = data.get('email')
        phone_number = data.get('phone_number')
        status = data.get('status')
        role_id = data.get('role_id')

        # Basic validation
        if not all([user_id, first_name, sur_name, gender, email, phone_number, status, role_id]):
            return jsonify({
                'success': False,
                'feedback': 'All required fields must be filled.'
            }), 400

        success, feedback = db_manager.edit_system_user(
            user_id=user_id,
            first_name=first_name,
            middle_name=middle_name,
            sur_name=sur_name,
            gender=gender,
            email=email,
            phone_number=phone_number,
            role_id=role_id,
            status=status
        )

        if success:
            return jsonify({'success': True, 'feedback': feedback}), 200

        return jsonify({'success': False, 'feedback': feedback}), 400

    except Exception as e:
        print("[ERROR] Editing user failed:", e)
        return jsonify({
            'success': False,
            'feedback': 'An unexpected error occurred.'
        }), 500

@dashboard_bp.route('/sys/delete_user', methods=['POST'])
def delete_system_user_route():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify(success=False, message="Invalid user ID")

    success, message = db_manager.delete_system_user(user_id)
    return jsonify(success=success, message=message)    

@dashboard_bp.route('/sys/roles')
@login_required
def roles():
    current_user = g.current_user
    sys_roles = db_manager.get_system_roles()
    total_system_users = db_manager.get_total_system_users()
    admin_users_count = db_manager.get_admin_users_count()
    system_maintainer_count = db_manager.get_system_maintainer_count()
    blocked_users_count = db_manager.get_blocked_users_count()
    return render_template('roles.html',
                            current_user = current_user,
                            sys_roles=sys_roles,
                            total_system_users = total_system_users,
                            admin_users_count = admin_users_count,
                            system_maintainer_count = system_maintainer_count,
                            blocked_users_count = blocked_users_count)


@dashboard_bp.route('/sys/item_lost')
@login_required
def item_lost():
    current_user = g.current_user
    sys_testimonials = db_manager.get_system_testimonials()
    total_testimonials = db_manager.get_total_testimonials_count()
    pending_testimonials = db_manager.get_pending_testimonials_count()
    approved_testimonials =  db_manager.get_approved_testimonials_count()
    hidden_testimonials = db_manager.get_hidden_testimonials_count()
    return render_template('item_lost.html',
                           current_user = current_user,
                           sys_testimonials=sys_testimonials,
                           total_testimonials = total_testimonials,
                           pending_testimonials = pending_testimonials,
                           approved_testimonials = approved_testimonials,
                           hidden_testimonials = hidden_testimonials                      
                           )                            

@dashboard_bp.route('/sys/item_found')
@login_required
def item_found():
    current_user = g.current_user
    sys_items_found = db_manager.get_system_items_found()
    items_found_count = db_manager.get_total_items_found_count()
    print(sys_items_found)
    return render_template('item_found.html',
                           current_user = current_user,
                           sys_items_found=sys_items_found,
                           items_found_count = items_found_count
                           ) 

@dashboard_bp.route('/sys/add_item_found', methods=['POST'])
def add_item_found():
    item_name = request.form.get('item_name')
    category = request.form.get('category')
    color = request.form.get('color')
    description = request.form.get('description')
    image = request.files.get('image')
    location = request.form.get('location')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    longitude = request.form.get('longitude')
    date_found = request.form.get('date_found')
    time_found = request.form.get('time_found')
    finder_name = request.form.get('finder_name')
    finder_email = request.form.get('finder_email')
    finder_phone_number = request.form.get('finder_phone_number')


    # Generate a unique filename using UUID
    ext = os.path.splitext(image.filename)[1]  # keep original extension
    unique_filename = f"{uuid4().hex}{ext}"  

    image_path = os.path.join(UPLOAD_ITEM_FOUND_FOLDER, unique_filename)
    try:
        image.save(image_path)
    except Exception as e:
        print("[ERROR] Saving item found image:", e)
        return jsonify({'success': False, 'feedback': 'Failed to save item found image'}), 500

    # Generate partner ID
    item_found_id = cryptographer.generate_unique_id()

    # Add partner to the database
    success, feedback = db_manager.add_item_found(
                    item_found_id = item_found_id, 
                    item_name = item_name, 
                    category = category, 
                    color = color, 
                    description = description, 
                    image = unique_filename, 
                    location = location, 
                    latitude = latitude, 
                    longitude = longitude, 
                    date_found = date_found, 
                    time_found = time_found, 
                    finder_name=finder_name, 
                    finder_email = finder_email, 
                    finder_phone_number = finder_phone_number
    )

    return jsonify({'success': success, 'feedback': feedback})