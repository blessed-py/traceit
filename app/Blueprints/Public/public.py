from flask import Blueprint, render_template, request, jsonify
from app.Database.database import DatabaseManager
from app.Database.encrypter import Cryptography
from app.API.SMTP import MAIL_SERVER
import os
from uuid import uuid4
from app.Blueprints.Authentications.decorators import time_ago



# Blueprint initialization
public_bp = Blueprint('public', __name__, template_folder='templates')

# Database instance

db_manager = DatabaseManager()
mail_server = MAIL_SERVER()
# Encryption instance
cryptographer = Cryptography()

# Base directory of the project 
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")

)

STORAGE_DIR = os.path.join(BASE_DIR, "Storage")

UPLOAD_ITEM_FOUND_FOLDER = os.path.join(STORAGE_DIR, "item_found")
UPLOAD_CLAIM_ITEM_FOLDER = os.path.join(STORAGE_DIR, "claim_item")
UPLOAD_PFP_FOLDER = os.path.join(STORAGE_DIR, "pfp")



os.makedirs(UPLOAD_ITEM_FOUND_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_CLAIM_ITEM_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_PFP_FOLDER, exist_ok=True)





@public_bp.route('/')
def index():
    sys_items = db_manager.get_latest_items_found()
    return render_template('index.html',
                           sys_items = sys_items)

@public_bp.route('/about')
def about():
    return render_template('about.html')    

@public_bp.route('/report_lost')
def report_lost():
    return render_template('report_lost.html')

@public_bp.route('/find_item')
def find_item():
    sys_items = db_manager.get_system_items_found()
    return render_template('find_item.html',
                           sys_items = sys_items)

@public_bp.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@public_bp.route('/contact')
def contact():
    return render_template('contact.html')


@public_bp.route('/view_detail/<item_id>')
def view_detail(item_id):
    item = db_manager.get_item_found_by_id(item_id)

    return render_template('view_detail.html',
                            item=item)

@public_bp.route('/report_found', methods=["GET","POST"])
def report_found():
    return render_template('report_found.html')

@public_bp.route('/report_item_found', methods=['POST'])
def report_item_found():

    item_name = request.form.get('item_name')
    category = request.form.get('category')
    color = request.form.get('color')
    description = request.form.get('description')

    location = request.form.get('location')
    latitude = float(request.form.get('latitude')) if request.form.get('latitude') else None
    longitude = float(request.form.get('longitude')) if request.form.get('longitude') else None

    date_found = request.form.get('date_found')
    time_found = request.form.get('time_found')

    finder_name = request.form.get('finder_name')
    finder_email = request.form.get('finder_email')
    finder_phone_number = request.form.get('finder_phone_number')

    image = request.files.get('image')

    unique_filename = None

    if image and image.filename != "":
        ext = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid4().hex}{ext}"

        image_path = os.path.join(UPLOAD_ITEM_FOUND_FOLDER, unique_filename)

        try:
            image.save(image_path)
        except Exception as e:
            print("[ERROR] Saving item image:", e)
            return jsonify({'success': False, 'feedback': 'Failed to save image'}), 500

    item_found_id = cryptographer.generate_unique_id()

    success, feedback = db_manager.add_item_found(
        item_found_id=item_found_id,
        item_name=item_name,
        category=category,
        color=color,
        description=description,
        image=unique_filename,
        location=location,
        latitude=latitude,
        longitude=longitude,
        date_found=date_found,
        time_found=time_found,
        finder_name=finder_name,
        finder_email=finder_email,
        finder_phone_number=finder_phone_number
    )

    return jsonify({'success': success, 'feedback': feedback})


@public_bp.route('/report_found/thank_you')
def thank_you_report_found():
    return render_template('thankyou_report_found.html')



@public_bp.route('/claim_item/<item_id>')
def claim_item(item_id):
    item = db_manager.get_item_found_by_id(item_id)
    return render_template('claim_item.html',
                           item = item)

@public_bp.route('/add_claim_item', methods=['POST'])
def add_claim_item():

    claimant_name = request.form.get('claimant_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    item_description = request.form.get('item_description')

    loss_detail = request.form.get('loss_detail')

    item_found_id = request.form.get('item_found_id')

    image = request.files.get('image')

    unique_filename = None

    if image and image.filename != "":
        ext = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid4().hex}{ext}"

        image_path = os.path.join(UPLOAD_CLAIM_ITEM_FOLDER, unique_filename)

        try:
            image.save(image_path)
        except Exception as e:
            print("[ERROR] Saving item image:", e)
            return jsonify({'success': False, 'feedback': 'Failed to save image'}), 500

    claim_item_id = cryptographer.generate_unique_id()

    success, feedback = db_manager.add_claim_item(
    claim_item_id = claim_item_id, 
    item_found_id = item_found_id, 
    claimant_name = claimant_name, 
    email = email, 
    phone_number = phone_number, 
    item_description = item_description, 
    loss_detail = loss_detail, 
    image = unique_filename
    )

    return jsonify({'success': success, 'feedback': feedback})