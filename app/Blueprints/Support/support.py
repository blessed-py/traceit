from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from app.Blueprints.Authentications.decorators import login_required, roles_required, flash
from app.Database.database import DatabaseManager
from app.Database.encrypter import Cryptography
#from app.API.SMTP import MAIL_SERVER
import os

# Blueprint initialization
support_bp = Blueprint('support', __name__, template_folder='templates')

#RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# Database instance
db_manager = DatabaseManager()
# Encryption instance
cryptographer = Cryptography()

#mail_server = MAIL_SERVER()

@support_bp.route('/support/customer_support')
#@login_required
def customer_support():

    sys_support_tickets = db_manager.get_system_support_tickets()
    total_support_tickets = db_manager.get_total_support_tickets()
    new_support_tickets = db_manager.get_new_support_tickets()
    in_progress_support_tickets = db_manager.get_in_progress_support_tickets()
    resolved_support_tickets = db_manager.get_resolved_support_tickets()
    active_categories = db_manager.get_active_contact_categories()
    return render_template('customer_support.html',

                           sys_support_tickets = sys_support_tickets, 
                           total_support_tickets = total_support_tickets,
                           new_support_tickets = new_support_tickets,
                           in_progress_support_tickets = in_progress_support_tickets,
                           resolved_support_tickets = resolved_support_tickets,
                           active_categories = active_categories)
'''
@support_bp.route('/support/send_message', methods=['POST'])
def add_support_ticket():

    recaptcha_token = request.form.get("g-recaptcha-response")
    if not recaptcha_token:
        return jsonify({
            "success": False,
            "feedback": "Please verify that you are not a robot."
        })

    if not cryptographer.verify_recaptcha(
        recaptcha_token,
        os.getenv("RECAPTCHA_SECRET_KEY"),
        request.remote_addr
    ):
        return jsonify({
            "success": False,
            "feedback": "reCAPTCHA verification failed. Please try again."
        })

    name = request.form['name']
    email = request.form['email']
    phone_number = request.form.get('phone_number')
    subject = request.form['subject']
    service = request.form['service']
    category = request.form['category']
    message = request.form['message']

    support_ticket_id = cryptographer.generate_unique_id()

    success, feedback = db_manager.add_support_ticket(
        support_ticket_id,
        name,
        email,
        phone_number,
        subject,
        service,
        category,
        message
    )

    if success:
        try:
            mail_server.send_html_email(
                email,
                "Thank you for contacting us!",
                f"""
                <p>Hi {name},</p>

                <p>Thank you for reaching out to us. We have received your message and our support team will get back to you shortly.</p>

                <p>Best regards,<br>
                Support Team</p>
                """
            )
        except Exception as e:
            print("[EMAIL ERROR] Support confirmation email failed:", e)

    return jsonify({
        "success": success,
        "feedback": feedback
    })

'''
@support_bp.route('/support/advance_status/<support_ticket_id>', methods=['POST'])
def advance_status(support_ticket_id):
    success = db_manager.advance_support_ticket_status(support_ticket_id)
    return jsonify({"success": success})

@support_bp.route('/support/resolve_ticket/<support_ticket_id>', methods=['POST'])
def resolve_support_ticket(support_ticket_id):
    try:
        success = db_manager.resolve_support_ticket(support_ticket_id)
        if success:
            return jsonify({"success": True, "feedback": "Support ticket resolved successfully!"})
        else:
            return jsonify({"success": False, "feedback": "Failed to resolve support ticket."})
    except Exception as e:
        print("[ERROR] Resolving support ticket:", e)
        return jsonify({"success": False, "feedback": "An error occurred."})

@support_bp.route('/support/delete_support_ticket', methods=['POST'])
def delete_support_ticket():
    if request.method == 'POST':
        data = request.get_json()
        support_ticket_id = data.get('support_ticket_id')
        if db_manager.delete_support_ticket(support_ticket_id):
            return jsonify({'success': True, 'feedback': 'Ticket deleted successfully!'})  
        return jsonify({'success': False, 'feedback': 'Ticket not deleted successfully!'}) 
    return jsonify({'success': False, 'feedback': 'Method not allowed!'}), 405

@support_bp.route('/support/contact_category')
@login_required
def contact_category():
    current_user = g.current_user
    sys_contact_categories = db_manager.get_system_contact_categories()
    total_categories = db_manager.get_active_contact_category_count()
    active_categories = db_manager.get_active_contact_category_count()
    inactive_categories = db_manager.get_inactive_contact_category_count()
    return render_template('contact_category.html',
                           current_user = current_user,
                           sys_contact_categories = sys_contact_categories,
                           total_categories=total_categories,
                           active_categories = active_categories,
                           inactive_categories = inactive_categories)

@support_bp.route('/support/add_contact_category', methods=['POST'])
def add_contact_category():
    name = request.form.get('name')
    if not name:
        return jsonify({
            "success": False,
            "message": "Category name is required."
        })
    contact_category_id = cryptographer.generate_unique_id()

    success = db_manager.add_contact_category(
        contact_category_id=contact_category_id,
        name=name
    )

    if success:
        return jsonify({
            "success": True,
            "message": "Contact category added successfully!"
        })

    return jsonify({
        "success": False,
        "message": "Failed to add contact category. It may already exist."
    })

@support_bp.route('/support/edit_contact_category', methods=['POST'])
def edit_contact_category():
    contact_category_id = request.form.get('contact_category_id')
    name = request.form.get('name', '').strip()
    status = request.form.get('status')

    if not contact_category_id or not name or not status:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        })

    success = db_manager.edit_contact_category(
        contact_category_id=contact_category_id,
        name=name,
        status=status
    )

    if success:
        return jsonify({
            "success": True,
            "message": "Contact category updated successfully!"
        })

    return jsonify({
        "success": False,
        "message": "Failed to update contact category."
    })

@support_bp.route('/support/delete_contact_category', methods=['POST'])
def delete_contact_category():
    data = request.get_json()
    contact_category_id = data.get('contact_category_id')

    if not contact_category_id:
        return jsonify({"success": False, "message": "Category ID is required!"})

    success = db_manager.delete_contact_category(contact_category_id)

    if success:
        return jsonify({"success": True, "message": "Contact category deactivated successfully!"})
    else:
        return jsonify({"success": False, "message": "Failed to deactivate contact category."})