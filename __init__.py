from flask import Flask, render_template
from .config import config_by_name
from .extensions import db, bcrypt, jwt, cors


def create_app(config_name='dev'):
    # Explicit template folder (important for factory structure)
    app = Flask(__name__, template_folder='templates')

    # Load Configuration
    if config_name in config_by_name:
        app.config.from_object(config_by_name[config_name])
    else:
        app.config.from_object(config_by_name['dev'])

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Register Blueprints (API Routes)
    from .routes.auth_routes import auth_bp
    from .routes.dashboard_routes import dashboard_bp
    from .routes.finance_routes import finance_bp
    from .routes.report_routes import report_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(finance_bp, url_prefix='/api/finance')
    app.register_blueprint(report_bp, url_prefix='/api/reports')

    # Create Database Tables (if they don't exist)
    with app.app_context():
        db.create_all()

    # Root Route (Frontend)
    @app.route('/')
    def index():
        return render_template('index.html')

    return app