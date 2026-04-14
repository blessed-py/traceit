from flask import Flask
from flask import send_from_directory, abort, render_template
from dotenv import load_dotenv
import os

load_dotenv('.env')

from bundle.Blueprints.Authentications.decorators import login_required
from bundle.Blueprints.Authentications.decorators import time_ago

from bundle.Blueprints.Dashboard.dashboard import dashboard_bp
from bundle.Blueprints.Authentications.auth import auth_bp
from bundle.Blueprints.Public.public import public_bp
from bundle.Blueprints.Settings.settings import settings_bp
from bundle.Blueprints.Support.support import support_bp
from bundle.Database.database import DatabaseManager



app = Flask(__name__, static_folder='bundle/static/')
app.config['SECRET_KEY'] = 'JKKEBJKBJRBKJRBLKJRCBLRCBLKJCRL4Y4479272949474JBCKEHCEV'

# Register Jinja filter
app.jinja_env.filters['timeago'] = time_ago

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "bundle", "Storage")

@app.route('/Storage/<path:filename>')
def serve_storage(filename):
    return send_from_directory(STORAGE_DIR, filename)


# Initialize database automatically


db_manager = DatabaseManager()
db_manager.initialize()




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
    app.run(debug=True, host='0.0.0.0', port=1234)