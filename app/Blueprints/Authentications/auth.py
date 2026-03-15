from flask import Blueprint, render_template, session, redirect, request, url_for, jsonify, flash
from app.Database.database import DatabaseManager
from app.Database.encrypter import Cryptography
#from app.API.SMTP import MAIL_SERVER
import secrets               
from datetime import datetime, timedelta, timezone 
from uuid import uuid4


# Blueprint initialization
auth_bp = Blueprint('auth', __name__, template_folder="templates")

cryptographer = Cryptography()
db_manager = DatabaseManager()
#mail_server = MAIL_SERVER()

# Login route
@auth_bp.route('/sys/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('login.html')



@auth_bp.route('/sys/reset_password')
def reset_password():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('reset_password.html')

@auth_bp.route('/sys/verify_email')
def verify_email():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('verify_email.html')

@auth_bp.route('/sys/login/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']

    success, feedback, user_id = db_manager.authenticate_user(email, password)

    if not success:
        return jsonify({'success': False, 'feedback': feedback}), 401

    # Store user in session
    session['user_id'] = user_id

    return jsonify({'success': True, 'feedback': feedback}), 200
    

@auth_bp.route('/sys/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/sys/forgot_password')
def forgot_password():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('forgot_password.html')
'''

@auth_bp.route('/sys/forgot_password', methods=['POST'])
def forgot_password_post():
    email = request.form.get('email', '').strip().lower()

    if not email:
        return jsonify({
            'success': False,
            'feedback': 'Please enter your email address.'
        }), 400

    # Always return the same response to prevent email enumeration
    generic_response = {
        'success': True,
        'feedback': 'If the email exists, a password reset link has been sent.'
    }

    user = db_manager.get_user_by_email(email)
    if not user:
        return jsonify(generic_response), 200

    # Generate reset token
    token = db_manager.create_password_reset_token(user['user_id'])
    print(token)
    if not token:
        print("[ERROR] Failed to create password reset token")
        return jsonify({
            'success': False,
            'feedback': 'Unable to process your request at the moment.'
        }), 500

    reset_link = url_for(
        'auth.reset_password_page',
        token=token,
        _external=True
    )

    # Send email safely
    try:
        mail_server.send_html_email(
            email,
            "Password Reset Request – ContentPro",
            f"""
            <p>Hello,</p>

            <p>We received a request to reset the password for your ContentPro account.</p>

            <p>To proceed, please click the button below to set a new password:</p>

            <p><a href="{reset_link}" style=" display: inline-block; padding: 12px 24px; background-color: #dc3545; color: #ffffff; text-decoration: none; font-weight: 600; border-radius: 6px; font-family: Arial, Helvetica, sans-serif;"> Reset Password </a></p>

            <p>If the button does not work, you may copy and paste the following link into your browser:</p>
            <p>{reset_link}</p>

            <p>For security reasons, this link will expire after a limited time. If you did not request a password reset, no action is required and your account will remain secure.</p>

            <p>If you need assistance, please contact our support team.</p>

            <p>Best regards,<br><strong>ContentPro Team</strong></p>
            """
        )
    except Exception as e:
        # Do NOT expose email failure to user
        print("[EMAIL ERROR] Password reset email failed:", e)

    return jsonify(generic_response), 200

@auth_bp.route('/sys/reset_password/<token>')
def reset_password_page(token):
    reset = db_manager.validate_password_reset_token(token)
    if not reset:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)

@auth_bp.route('/sys/reset_password/<token>', methods=['POST'])
def reset_password_submit(token):
    password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm_password', '').strip()

    if not password or not confirm:
        return jsonify({'success': False, 'feedback': 'All fields are required.'}), 400
    if password != confirm:
        return jsonify({'success': False, 'feedback': 'Passwords do not match.'}), 400

    reset = db_manager.validate_password_reset_token(token)
    if not reset:
        return jsonify({'success': False, 'feedback': 'Invalid or expired token.'}), 400

    user_id = reset['user_id']

    try:
        # Hash password and update
        hashed_password = cryptographer.generate_key(password)
        success = db_manager.update_user_password(user_id, hashed_password)
        if not success:
            return jsonify({'success': False, 'feedback': 'Failed to update password. Please try again.'}), 500

        # Mark token as used
        db_manager.mark_reset_token_used(token)

        # Send confirmation email safely
        try:
            reset_user = db_manager.get_user_by_id(user_id)
            email = reset_user.get('email')
            if email:
                mail_server.send_html_email(
                    email,
                    "Your ContentPro Password Was Changed Successfully!",
                    f"""
                    <p>Hi {reset_user.get('first_name', '')},</p>
                    <p>Your password for your ContentPro account has been successfully updated.</p>
                    <p>If you did not perform this action, please contact support immediately.</p>
                    <p>Best regards,<br><strong>Support Team</strong></p>
                    """
                )
        except Exception as email_error:
            print("[WARNING] Failed to send password change email:", email_error)

        return jsonify({'success': True, 'feedback': 'Password updated successfully!'}), 200

    except Exception as e:
        print("[ERROR] Reset password failed:", e)
        return jsonify({'success': False, 'feedback': 'Something went wrong. Please try again.'}), 500
        '''