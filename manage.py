from flask import Flask
from flask import send_from_directory, abort, render_template
from app.Blueprints.Dashboard.dashboard import dashboard_bp
from app.Blueprints.Authentications.auth import auth_bp
from app.Blueprints.Public.public import public_bp
from app.Blueprints.Settings.settings import settings_bp
from app.Blueprints.Support.support import support_bp
from app.Database.database import DatabaseManager
from app.Blueprints.Authentications.decorators import login_required
from app.Blueprints.Authentications.decorators import time_ago


import os


app = Flask(__name__, static_folder='app/static/')
app.config['SECRET_KEY'] = 'JKKEBJKBJRBKJRBLKJRCBLRCBLKJCRL4Y4479272949474JBCKEHCEV'

# Register Jinja filter
app.jinja_env.filters['timeago'] = time_ago

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "app", "Storage")

@app.route('/Storage/<path:filename>')
def serve_storage(filename):
    import os
    full_path = os.path.join(STORAGE_DIR, filename)
    print("Looking for:", full_path)
    print("Exists:", os.path.exists(full_path))
    return send_from_directory(STORAGE_DIR, filename)


# Initialize database automatically

try:
    db_manager = DatabaseManager()
    db_manager.initialize()
except Exception as e:
    print(f"❌ Database initialization failed: {e}")
    exit(1)



@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404



# Blueprint registration

app.register_blueprint(dashboard_bp)
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(support_bp)


# Main route
if __name__ == '__main__':
   #app.run(debug=True, host='0.0.0.0', port=1234)
   app.run()