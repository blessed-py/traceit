from mysql.connector import connect, Error, IntegrityError
from app.Database.encrypter import Cryptography
from flask import session
from datetime import date, datetime, timedelta
import uuid
import secrets
import os



# Encryption instance
cryptographer = Cryptography()



  #Connect to the database and initialize one user(email and password) when user.count==0
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")

DB_NAME = os.environ.get("DB_NAME")
DB_PWD = os.environ.get("DB_PWD")

EMAIL = os.environ.get("EMAIL")
EMAIL_PWD = os.environ.get("EMAIL_PWD")

db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PWD,
    'database': DB_NAME,
}

class DatabaseManager():
    def initialize(self):
        connection = None
        try:
            # Connect to the database
            connection = connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PWD,
                database=DB_NAME
            )

            cursor = connection.cursor()
            # Create a cursor
            '''
            cursor.execute('CREATE DATABASE IF NOT EXISTS lost_found_db')
            cursor.execute('USE lost_found_db')
            '''

            
            # CREATE Tables
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS user (
                           id INT AUTO_INCREMENT UNIQUE NOT NULL, 
                           first_name VARCHAR(255), 
                           middle_name VARCHAR(255), 
                           sur_name VARCHAR(255), 
                           gender ENUM("Male", "Female") DEFAULT NULL,
                           status ENUM("Active", "Blocked") DEFAULT "Active",
                           user_id VARCHAR(255) PRIMARY KEY)''') 

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profile (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE,
                    phone_number VARCHAR(255),
                    profile_picture VARCHAR(255),
                    user_id VARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS item_found (
                    id INT AUTO_INCREMENT NOT NULL UNIQUE,
                    item_name VARCHAR(255) NOT NULL,
                    category VARCHAR(255),
                    color VARCHAR(255), 
                    description TEXT,
                    image VARCHAR(255) NOT NULL,
                    location VARCHAR(255),
                    latitude  DECIMAL(10,8),
                    longitude DECIMAL(11,8),
                    date_found DATE,
                    time_found TIME,
                    finder_name VARCHAR(255),
                    finder_email VARCHAR(255),
                    finder_phone_number VARCHAR(255),
                    status ENUM('available','claimed','returned') DEFAULT 'available',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    item_found_id VARCHAR(255) PRIMARY KEY
                );
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS testimonial (
                    id INT AUTO_INCREMENT UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    job_title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    consent BOOLEAN DEFAULT 0,
                    status ENUM('Pending','Approved','Hidden') DEFAULT 'Pending',
                    priority INT NULL UNIQUE,
                    created_at DATE,
                    testimonial_id VARCHAR(255) PRIMARY KEY
                );        
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS social (
                           id INT AUTO_INCREMENT UNIQUE,
                           social_name VARCHAR(255),
                           social_link VARCHAR(255),
                           social_id VARCHAR(255) PRIMARY KEY
                           )
            ''')

            cursor.execute('SELECT COUNT(*) FROM social')
           
            social = cursor.fetchone()[0]

            if social == 0:
                cursor.execute(
                    '''
                    INSERT INTO social (social_id, social_name, social_link)
                    VALUES
                    (%s, %s, %s),
                    (%s, %s, %s),
                    (%s, %s, %s),
                    (%s, %s, %s)
                    ''',
                    (
                        cryptographer.generate_unique_id(), "Whatsapp", "https://www.whatsapp.com/", 
                        cryptographer.generate_unique_id(), "Facebook", "https://www.facebook.com/",
                        cryptographer.generate_unique_id(), "Instagram", "https://www.instagram.com/",
                        cryptographer.generate_unique_id(), "Linkedin", "https://www.linkedin.com/",
                    )
                )

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team (
                           id INT AUTO_INCREMENT UNIQUE NOT NULL,
                           name VARCHAR(255) UNIQUE NOT NULL,
                           title VARCHAR(255) NOT NULL,
                           image VARCHAR(255) NOT NULL,
                           priority INT NULL UNIQUE,
                           status ENUM('active', 'inactive') DEFAULT 'active',
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           team_id VARCHAR(255) PRIMARY KEY
                           )        
            ''') 

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS item (
                    id INT AUTO_INCREMENT NOT NULL UNIQUE,
                    title VARCHAR(255),
                    description TEXT,
                    category VARCHAR(255),
                    unique_identifier VARCHAR(255),
                    type ENUM('lost','found'),
                    status ENUM('open','matched','returned','closed'),
                    location VARCHAR(255),
                    date_lost DATE NOT NULL,
                    date_found DATE,
                    image VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    item_id VARCHAR(255) PRIMARY KEY)
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS support_ticket (
                           id INT AUTO_INCREMENT UNIQUE NOT NULL,
                           name VARCHAR(255) NOT NULL,
                           email VARCHAR(255) NOT NULL,
                           phone_number VARCHAR(255),
                           subject VARCHAR(255) NOT NULL,
                           service VARCHAR(255) NOT NULL,
                           category VARCHAR(255) NOT NULL,
                           message TEXT NOT NULL,
                           status ENUM('new', 'in_progress', 'resolved') DEFAULT 'new',
                           created_at DATE,
                           support_ticket_id VARCHAR(255) PRIMARY KEY )
            ''') 

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contact_category (
                    id INT AUTO_INCREMENT UNIQUE,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    status ENUM('active', 'inactive') DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    contact_category_id VARCHAR(255) PRIMARY KEY
                );
            ''')



            cursor.execute('CREATE TABLE IF NOT EXISTS user_auth (id INT AUTO_INCREMENT UNIQUE NOT NULL, password VARCHAR(255), user_id VARCHAR(255), FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE)') 
            
            cursor.execute('CREATE TABLE IF NOT EXISTS role (id INT AUTO_INCREMENT UNIQUE NOT NULL, role_name VARCHAR(255), description VARCHAR(255), role_id VARCHAR(255) PRIMARY KEY)')

            cursor.execute('CREATE TABLE IF NOT EXISTS user_role (id INT AUTO_INCREMENT UNIQUE NOT NULL, role_id VARCHAR(255), user_id VARCHAR(255), FOREIGN KEY(role_id) REFERENCES role(role_id) ON DELETE CASCADE, FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE)')

            # Check if there are any roles in the table
            cursor.execute('SELECT COUNT(*) FROM role')
            count = cursor.fetchone()[0]
            
            # Insert default roles only if none exist
            if count == 0:
                admin_id = cryptographer.generate_unique_id()
                user_id = cryptographer.generate_unique_id()
                system_maintainer_id = cryptographer.generate_unique_id()
                
                cursor.execute(f'''INSERT INTO role (role_name, description, role_id) VALUES
                           ("Admin", "System Administrator has full access to the system and manage system users", "{admin_id}"),
                           ("User", "User has access to view his/her profile, initiate workflow, and attend assigned tasks ONLY", "{user_id}"),
                           ("SYSTEM MAINTAINER", "System Maintainer is responsible for maintaining the health of the system, making potential updates and patch fixes", "{system_maintainer_id}")''')

            cursor.execute('SELECT COUNT(*) FROM user')
            count = cursor.fetchone()[0]
            # Insert SYSTEM MAINTAINER only if none exist
            if count == 0:
                # Generate unique user_id
                admin_user_id = cryptographer.generate_unique_id()

                # Generate hashed password
                password_hash = cryptographer.generate_key(EMAIL_PWD)

                # Insert into user table
                cursor.execute(
                    'INSERT INTO user (user_id, first_name, middle_name, sur_name, status) VALUES (%s, %s, %s, %s, %s)',
                    (admin_user_id, "SYSTEM", "", "MAINTAINER", "Active")
                )

                # Insert into user_profile
                cursor.execute(
                    'INSERT INTO user_profile (user_id, email, profile_picture) VALUES (%s, %s, %s)',
                    (admin_user_id, EMAIL, "sys.png")
                )

                # Insert into user_auth
                cursor.execute(
                    'INSERT INTO user_auth (user_id, password) VALUES (%s, %s)',
                    (admin_user_id, password_hash)
                )

                # Link to SYSTEM MAINTAINER role
                cursor.execute('SELECT role_id FROM role WHERE role_name = "SYSTEM MAINTAINER"')
                role_id = cursor.fetchone()[0]
                cursor.execute(
                    'INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)',
                    (admin_user_id, role_id)
                )
                connection.commit()

        except Error as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection and connection.is_connected():
                connection.close()

    def get_system_roles(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM role')
            role = cursor.fetchall()
            return role
        except Error as e:
            print("[ERROR] An error occurred while fetching system roles:", e)
            return []

    def get_system_users(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user')
            user = cursor.fetchall()
            return user
        except Error as e:
            print("[ERROR] An error occurred while fetching system users:", e)
            return [] 

    def get_total_system_users(self):
        try:    
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM user')
            total = cursor.fetchone()[0]
            return total
        except Error as e:
            print("[ERROR] An error occurred while fetching total system users:", e)
            return 0

    def get_admin_users_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(DISTINCT u.user_id)
                FROM user u
                INNER JOIN user_role ur ON u.user_id = ur.user_id
                INNER JOIN role r ON ur.role_id = r.role_id
                WHERE r.role_name = %s
            """, ("Admin",))

            return cursor.fetchone()[0]

        except Error as e:
            print("[ERROR] An error occurred while fetching admin users count:", e)
            return 0                

    def get_system_maintainer_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(DISTINCT u.user_id)
                FROM user u
                INNER JOIN user_role ur ON u.user_id = ur.user_id
                INNER JOIN role r ON ur.role_id = r.role_id
                WHERE r.role_name = %s
            """, ("SYSTEM MAINTAINER",))

            return cursor.fetchone()[0]

        except Error as e:
            print("[ERROR] An error occurred while fetching system maintainer count:", e)
            return 0

    def get_blocked_users_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM user
                WHERE status != %s
            """, ("Active",))

            return cursor.fetchone()[0]

        except Error as e:
            print("[ERROR] An error occurred while fetching blocked users count:", e)
            return 0

    def add_system_user(self, first_name, middle_name, sur_name, gender,
                        email, phone_number, role_id, password):
        connection = None

        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            user_id = cryptographer.generate_unique_id()
            hashed_password = cryptographer.generate_key(password)

            # Insert into user table
            cursor.execute(
                """
                INSERT INTO user (user_id, first_name, middle_name, sur_name, gender)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, first_name, middle_name, sur_name, gender)
            )

            # Insert into user_profile
            cursor.execute(
                """
                INSERT INTO user_profile (user_id, email, phone_number)
                VALUES (%s, %s, %s)
                """,
                (user_id, email, phone_number)
            )

            # Insert into user_auth
            cursor.execute(
                """
                INSERT INTO user_auth (user_id, password)
                VALUES (%s, %s)
                """,
                (user_id, hashed_password)
            )

            # Insert into user_role
            cursor.execute(
                """
                INSERT INTO user_role (user_id, role_id)
                VALUES (%s, %s)
                """,
                (user_id, role_id)
            )

            connection.commit()
            return True, "System User added successfully!"

        except Error as e:
            if connection:
                connection.rollback()

            error_message = str(e)
            print("[ERROR] Add system user failed:", error_message)

            # Duplicate email or unique key
            if e.errno == 1062:
                if "email" in error_message:
                    return False, "Email already exists!"
                return False, "Duplicate entry detected!"

            return False, "Failed to add user. Please try again."

    def role_exists(self, role_id):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(
                'SELECT 1 FROM role WHERE role_id = %s LIMIT 1',
                (role_id,)
            )
            return cursor.fetchone() is not None
        except Error as e:
            print("[ERROR] role_exists:", e)
            return False

    def edit_system_user(
        self, user_id, first_name, middle_name, sur_name,
        gender, email, phone_number, role_id, status
    ):
        connection = None

        try:
            if not self.role_exists(role_id):
                return False, "Invalid role selected!"

            email = email.lower()

            connection = connect(**db_config)
            cursor = connection.cursor()

            # Update user table
            cursor.execute("""
                UPDATE user
                SET first_name=%s,
                    middle_name=%s,
                    sur_name=%s,
                    gender=%s,
                    status=%s
                WHERE user_id=%s
            """, (first_name, middle_name, sur_name, gender, status, user_id))

            # Update profile
            cursor.execute("""
                UPDATE user_profile
                SET email=%s,
                    phone_number=%s
                WHERE user_id=%s
            """, (email, phone_number, user_id))

            # ✅ CHECK role existence explicitly
            cursor.execute("""
                SELECT 1 FROM user_role WHERE user_id=%s
            """, (user_id,))
            role_exists = cursor.fetchone()

            if role_exists:
                cursor.execute("""
                    UPDATE user_role
                    SET role_id=%s
                    WHERE user_id=%s
                """, (role_id, user_id))
            else:
                cursor.execute("""
                    INSERT INTO user_role (user_id, role_id)
                    VALUES (%s, %s)
                """, (user_id, role_id))

            connection.commit()
            return True, "User updated successfully!"

        except Error as e:
            if connection:
                connection.rollback()

            print("[ERROR] Edit system user:", e)

            if "Duplicate entry" in str(e) and "email" in str(e):
                return False, "Email already exists in the system!"

            return False, "An error occurred while updating the user."
        
    def delete_system_user(self, user_id):
        try:
            connection = connect(**db_config)

            cursor = connection.cursor() 

            cursor.execute(
                "DELETE FROM user WHERE user_id = %s",
                (user_id,)
            )
            connection.commit()

            if cursor.rowcount == 0:
                return False, "User not found!"

            return True, "System User deleted successfully!"

        except Exception as e:
            print("[ERROR] An error occurred while deleting system user:", e)
            return False, "An unexpected error occurred."          

    def get_user_by_email(self, email):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            cursor.execute('''SELECT * FROM user_profile WHERE email = %s ''',
                (email,)
            )
            user = cursor.fetchone()
            return user

        except Error as e:
            print("[ERROR] Fetching user by email:", e)
            return None


    def get_user_role_by_id(self, user_id):
        try:
            connection = connect(**db_config)    
            cursor = connection.cursor()
            cursor.execute(f'SELECT role.role_name, role.role_id FROM role INNER JOIN user_role ON role.role_id = user_role.role_id WHERE user_role.user_id = "{user_id}"')
            result = cursor.fetchone()
            return result[0]
        except Error as e:
            print("[ERROR] An error occurred while fetching user role:", e)
            return [] 

    def get_user_by_id(self, user_id):
        """Fetch a single user's full info by user_id"""
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = '''
                SELECT 
                    u.user_id,
                    u.first_name,
                    u.middle_name,
                    u.sur_name,
                    u.gender,
                    u.status,
                    up.email,
                    up.phone_number,
                    up.profile_picture,
                    r.role_name,
                    r.description AS role_description
                FROM user u
                LEFT JOIN user_profile up ON u.user_id = up.user_id
                LEFT JOIN user_role ur ON u.user_id = ur.user_id
                LEFT JOIN role r ON ur.role_id = r.role_id
                WHERE u.user_id = %s
                LIMIT 1
            '''
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user

        except Error as e:
            print("[ERROR] An error occurred while fetching user by ID:", e)
            return None        
        
    def get_system_user_info(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = '''
                SELECT 
                    u.user_id,
                    u.first_name,
                    u.middle_name,
                    u.sur_name,
                    u.gender,
                    u.status,
                    up.email,
                    up.phone_number,
                    up.profile_picture,
                    r.role_name,
                    r.description AS role_description
                FROM user u
                LEFT JOIN user_profile up ON u.user_id = up.user_id
                LEFT JOIN user_role ur ON u.user_id = ur.user_id
                LEFT JOIN role r ON ur.role_id = r.role_id
            '''
            cursor.execute(query)
            users = cursor.fetchall()
            return users

        except Error as e:
            print("[ERROR] An error occurred while fetching system user info:", e)
            return []    

    #Authentication
    def authenticate_user(self, email, plain_password):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            # Get user
            cursor.execute(
                'SELECT user_id FROM user_profile WHERE email=%s',
                (email.lower(),)
            )
            row = cursor.fetchone()

            if not row:
                return False, "Invalid email or password.", None

            user_id = row[0]

            # Get password
            cursor.execute(
                'SELECT password FROM user_auth WHERE user_id=%s',
                (user_id,)
            )
            row = cursor.fetchone()

            if not row:
                return False, "Authentication data missing.", None

            db_password = row[0]

            # Check status
            cursor.execute(
                'SELECT status FROM user WHERE user_id=%s',
                (user_id,)
            )
            status = cursor.fetchone()[0]

            if status != 'Active':
                return False, "Your account is blocked. Please contact admin!", None

            # ✅ VERIFY PASSWORD (not re-hash)
            if not cryptographer.verify_key(plain_password, db_password):
                return False, "Invalid email or password.", None

            return True, "Login successful", user_id

        except Exception as e:
            print("[AUTH ERROR]", e)
            return False, "Authentication failed.", None        

    def get_system_support_tickets(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""SELECT * FROM support_ticket ORDER BY 
                    CASE status
                        WHEN 'new' THEN 1
                        WHEN 'in_progress' THEN 2
                        WHEN 'resolved' THEN 3
                        ELSE 4
                    END,
                    created_at DESC
            """)

            result = cursor.fetchall()
            return result

        except Error as e:
            print("[ERROR] Fetching system support tickets:", e)
            return []

    def add_support_ticket(self, support_ticket_id, name, email, phone_number, subject, service, category, message):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(
                '''INSERT INTO support_ticket (support_ticket_id, name, email, phone_number, subject, service, category, message, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())''',
                (support_ticket_id, name, email, phone_number, subject, service, category, message)
            )
            connection.commit()
            return True, "Message sent successfully!"
        except Error as e:
            print("[ERROR] An error occurred while sending message:", e)
            return False, "An unexpected error occurred."

    def get_total_support_tickets(self):
        try:    
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM support_ticket')
            total = cursor.fetchone()[0]
            return total
        except Error as e:
            print("[ERROR] An error occurred while fetching total support_tickets:", e)
            return 0    

    def get_new_support_tickets(self):
        try:    
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM support_ticket WHERE status="new"')
            new = cursor.fetchone()[0]
            return new
        except Error as e:
            print("[ERROR] An error occurred while fetching new support tickets:", e)
            return 0  

    def get_in_progress_support_tickets(self):
        try:    
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM support_ticket WHERE status="in_progress"')
            in_progress = cursor.fetchone()[0]
            return in_progress
        except Error as e:
            print("[ERROR] An error occurred while fetching in_progress support tickets:", e)
            return 0 

    def get_resolved_support_tickets(self):
        try:    
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM support_ticket WHERE status="resolved"')
            resolved = cursor.fetchone()[0]
            return resolved
        except Error as e:
            print("[ERROR] An error occurred while fetching resolved support tickets:", e)
            return 0                                         
        
    def advance_support_ticket_status(self, support_ticket_id):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE support_ticket
                SET status = 'in_progress'
                WHERE support_ticket_id = %s
                AND status = 'new'
            """, (support_ticket_id,))

            connection.commit()
            return cursor.rowcount > 0

        except Error as e:
            print("[ERROR] Status update failed:", e)
            return False
        
    def resolve_support_ticket(self, support_ticket_id):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute(
                "UPDATE support_ticket SET status = %s WHERE support_ticket_id = %s AND status = %s",
                ('resolved', support_ticket_id, 'in_progress')
            )

            connection.commit()
            return cursor.rowcount > 0  

        except Error as e:
            print(f"[ERROR] Resolving support ticket {support_ticket_id}: {e}")
            return False        

    def delete_support_ticket(self, support_ticket_id):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM support_ticket WHERE support_ticket_id="{support_ticket_id}"')
            connection.commit()
            return True
        except Error as e:
            print("[ERROR] An error occurred while deleting system ssupport ticket:", e)
            return False  

    def get_system_contact_categories(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            cursor.execute(""" SELECT * FROM contact_category ORDER BY created_at DESC
            """)
            result = cursor.fetchall()
            return result

        except Error as e:
            print("[ERROR] An error occurred while fetching contact categories:", e)
            return []

    def get_active_contact_categories(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            cursor.execute(""" SELECT * FROM contact_category WHERE status='Active'
            """)
            result = cursor.fetchall()
            return result

        except Error as e:
            print("[ERROR] An error occurred while fetching active contact categories:", e)
            return []


    def get_total_contact_category_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) AS total FROM contact_category")
            result = cursor.fetchone()
            return result[0]  # total count

        except Error as e:
            print("[ERROR] An error occurred while counting contact categories:", e)
            return 0

    def get_active_contact_category_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM contact_category WHERE status='active'")
            result = cursor.fetchone()
            return result[0] 

        except Error as e:
            print("[ERROR] An error occurred while counting contact categories:", e)
            return 0

    def get_inactive_contact_category_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM contact_category WHERE status='inactive'")
            result = cursor.fetchone()
            return result[0] 

        except Error as e:
            print("[ERROR] An error occurred while counting contact categories:", e)
            return 0

    def add_contact_category(self, contact_category_id, name):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute('''INSERT INTO contact_category
                (contact_category_id, name)
                VALUES (%s, %s)
                ''',
                (contact_category_id, name)
            )

            connection.commit()
            return True

        except Error as e:
            print("[ERROR] An error occurred while adding contact category:", e)
            return False

    def edit_contact_category(self, contact_category_id, name, status):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute('''UPDATE contact_category SET name = %s, status = %s
                WHERE contact_category_id = %s
                ''',
                (name, status, contact_category_id)
            )
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print("[ERROR] An error occurred while updating contact category:", e)
            return False

    def delete_contact_category(self, contact_category_id):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()

            cursor.execute(
                '''
                DELETE FROM contact_category
                WHERE contact_category_id = %s
                ''',
                (contact_category_id,)
            )

            connection.commit()
            return cursor.rowcount > 0

        except Error as e:
            print("[ERROR] An error occurred while deleting contact category:", e)
            return False  

    def update_user_profile_picture(self, user_id, profile_picture):
        connection = None
        cursor = None
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            # Fetch existing profile picture
            cursor.execute(
                "SELECT profile_picture FROM user_profile WHERE user_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            old_picture = result['profile_picture'] if result else None

            if result:
                # Update existing profile
                cursor.execute(
                    "UPDATE user_profile SET profile_picture = %s WHERE user_id = %s",
                    (profile_picture, user_id)
                )
            else:
                # Insert new profile record
                cursor.execute(
                    "INSERT INTO user_profile (profile_picture, user_id) VALUES (%s, %s)",
                    (profile_picture, user_id)
                )

            connection.commit()
            return True, old_picture

        except Error as e:
            print("[ERROR] An error occurred while updating profile picture:", e)
            return False, None   

    def get_system_testimonials(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT *
                FROM testimonial
                ORDER BY 
                    CASE 
                        WHEN status = 'Pending' THEN 0
                        WHEN status = 'Approved' THEN 1
                        ELSE 2
                    END ASC,
                    priority ASC
            ''')
            return cursor.fetchall()
        except Error as e:
            print("[ERROR] Fetching system testimonials:", e)
            return []

    def get_approved_testimonials(self):
        try:    
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM testimonial WHERE status="Approved" ORDER BY priority ASC, created_at DESC')
            return cursor.fetchall()
        except Error as e:
            print("[ERROR] Fetching approved testimonials:", e)
            return []


    def get_first_three_testimonials(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT * FROM testimonial
                WHERE status = 'Approved'
                ORDER BY priority ASC, created_at DESC
                LIMIT 3
            """
            cursor.execute(query)
            return cursor.fetchall()

        except Error as e:
            print("[ERROR] Fetching first three testimonials:", e)
            return []

    def get_total_testimonials_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM testimonial")
            return cursor.fetchone()[0]
        except Error as e:
            print("[ERROR] Fetching total testimonials:", e)
            return 0
        
    def get_pending_testimonials_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM testimonial WHERE status='Pending'")
            return cursor.fetchone()[0]
        except Error as e:
            print("[ERROR] Fetching pending testimonials:", e)
            return 0
        
    def get_approved_testimonials_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM testimonial WHERE status='Approved'")
            return cursor.fetchone()[0]
        except Error as e:
            print("[ERROR] Fetching approved testimonials count:", e)
            return 0
        
    def get_hidden_testimonials_count(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM testimonial WHERE status='Hidden'")
            return cursor.fetchone()[0]
        except Error as e:
            print("[ERROR] Fetching hidden testimonials:", e)
            return 0
        
    # --- Add Testimonial ---
    def add_testimonial(self, testimonial_id, name, job_title, message, consent=0):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            # New testimonial is always Pending, so priority is None
            priority = None
            status = 'Pending'

            cursor.execute("""
                INSERT INTO testimonial
                (testimonial_id, name, job_title, message, consent, priority, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
            """, (
                testimonial_id,
                name,
                job_title,
                message,
                consent,
                priority,
                status
            ))

            connection.commit()
            return True, "Testimonial added successfully!"

        except Error as e:
            print("[ERROR] Adding testimonial:", e)
            return False, "An unexpected error occurred."

    def edit_testimonial(self, testimonial_id, name, job_title, message, status=None, new_priority=None):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            # Fetch current testimonial
            cursor.execute('SELECT status, priority, consent FROM testimonial WHERE testimonial_id=%s', (testimonial_id,))
            row = cursor.fetchone()
            if not row:
                return False, "Testimonial not found."

            current_status = row['status']
            current_priority = row['priority']  # can be None
            consent = row['consent']

            # --- Update basic fields ---
            if consent == 0:
                # Non-public testimonial: hide and remove priority
                cursor.execute('''
                    UPDATE testimonial
                    SET name=%s, job_title=%s, message=%s, status='Hidden', priority=NULL
                    WHERE testimonial_id=%s
                ''', (name, job_title, message, testimonial_id))
            else:
                # Public testimonial
                cursor.execute('''
                    UPDATE testimonial
                    SET name=%s, job_title=%s, message=%s, status=%s
                    WHERE testimonial_id=%s
                ''', (name, job_title, message, status, testimonial_id))

                # --- Handle Pending or Hidden ---
                if status in ('Pending', 'Hidden') and current_priority is not None:
                    cursor.execute('UPDATE testimonial SET priority=NULL WHERE testimonial_id=%s', (testimonial_id,))
                    # Shift other priorities up
                    cursor.execute('''
                        UPDATE testimonial
                        SET priority = priority - 1
                        WHERE priority > %s AND status='Approved'
                    ''', (current_priority,))

                # --- Handle Approved ---
                elif status == 'Approved':
                    if new_priority is None:
                        # Auto-assign max priority +1
                        cursor.execute('SELECT COALESCE(MAX(priority),0)+1 AS next_priority FROM testimonial WHERE status="Approved"')
                        new_priority = cursor.fetchone()['next_priority']

                    if current_priority is None:
                        # Previously Pending or Hidden → just assign
                        cursor.execute('UPDATE testimonial SET priority=%s WHERE testimonial_id=%s', (new_priority, testimonial_id))
                    elif new_priority != current_priority:
                        # Temporarily free slot
                        cursor.execute('UPDATE testimonial SET priority=-1 WHERE testimonial_id=%s', (testimonial_id,))

                        if new_priority < current_priority:
                            # Moving up: shift others down
                            cursor.execute('''
                                UPDATE testimonial
                                SET priority = priority + 1
                                WHERE priority >= %s AND priority < %s AND status='Approved'
                            ''', (new_priority, current_priority))
                        else:
                            # Moving down: shift others up
                            cursor.execute('''
                                UPDATE testimonial
                                SET priority = priority - 1
                                WHERE priority <= %s AND priority > %s AND status='Approved'
                            ''', (new_priority, current_priority))

                        # Set final priority
                        cursor.execute('UPDATE testimonial SET priority=%s WHERE testimonial_id=%s', (new_priority, testimonial_id))

            connection.commit()
            return True, "Testimonial updated successfully!"

        except Error as e:
            print("[ERROR] Editing testimonial:", e)
            if connection:
                connection.rollback()
            return False, "An unexpected error occurred."
        
    def delete_testimonial(self, testimonial_id):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            # Fetch the testimonial
            cursor.execute("SELECT status, priority FROM testimonial WHERE testimonial_id=%s", (testimonial_id,))
            testimonial = cursor.fetchone()
            if not testimonial:
                return False, "Testimonial not found."

            deleted_priority = testimonial['priority']
            deleted_status = testimonial['status']

            # Delete the testimonial
            cursor.execute("DELETE FROM testimonial WHERE testimonial_id=%s", (testimonial_id,))
            connection.commit()

            # If it was Approved and had a priority, shift others
            if deleted_status == 'Approved' and deleted_priority is not None:
                cursor.execute("""
                    UPDATE testimonial
                    SET priority = priority - 1
                    WHERE status='Approved' AND priority > %s
                """, (deleted_priority,))
                connection.commit()

            return True, "Testimonial deleted successfully!"

        except Error as e:
            print("[ERROR] Deleting testimonial:", e)
            if connection:
                connection.rollback()
            return False, "An unexpected error occurred while deleting testimonial."     

    def get_system_items_found(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM item_found')
            result = cursor.fetchall()
            return result
        except Error as e:
            print("[ERROR] An error occurred while fetching system items found:", e)
            return [] 
        
    def get_latest_items_found(self):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT * 
                FROM item_found
                ORDER BY date_found DESC
                LIMIT 3
            """)

            return cursor.fetchall()

        except Error as e:
            print("[ERROR] Fetching latest items found:", e)
            return [] 

    def get_item_found_by_id(self, item_found_id):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM item_found WHERE item_found_id = %s"
            cursor.execute(query, (item_found_id,))

            return cursor.fetchone()

        except Error as e:
            print("[ERROR] Fetching item by ID:", e)
            return None             

    def add_item_found(self, item_found_id, item_name, category, color, description, image, location, latitude, longitude, date_found, time_found, finder_name, finder_email, finder_phone_number):
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary = True)  
            cursor.execute(
                '''INSERT INTO item_found (item_found_id, item_name, category, color, description, image, location, latitude, longitude, date_found, time_found, finder_name, finder_email, finder_phone_number, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())''',
                (item_found_id, item_name, category, color, description, image, location, latitude, longitude, date_found, time_found, finder_name, finder_email, finder_phone_number)
            )
            connection.commit()
            return True, "Item Added Successfully!"
        except Error as e:
            print("[ERROR] An error occurred while adding item found:", e)
            return False, "An unexpected error occurred."