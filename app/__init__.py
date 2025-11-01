from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from datetime import datetime
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()  # ✅ create mail instance

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)  # ✅ initialize mail with app
    
    # Register custom filters
    @app.template_filter('number_format')
    def number_format(value):
        try:
            return "{:,.0f}".format(float(value))
        except (ValueError, TypeError):
            return value
    
    @app.template_filter('format_number')
    def format_number(value):
        try:
            if value is None:
                return "0"
            return "{:,}".format(int(value))
        except (ValueError, TypeError):
            return str(value)
    @app.template_filter('format_datetime')
    def format_datetime(value):
        """Format datetime string for display"""
        try:
            if isinstance(value, str):
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            else:
                dt = value
                
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return value

    
    # Register blueprints
    from app.auth import routes as auth_routes
    from app.main import routes as main_routes
    from app.projects import routes as projects_routes
    from app.admin import routes as admin_routes
    
    # Import and register teams blueprint
    from app.teams import routes as teams_routes
    
    app.register_blueprint(auth_routes.auth)
    app.register_blueprint(main_routes.main)
    app.register_blueprint(projects_routes.projects)
    app.register_blueprint(admin_routes.admin)
    app.register_blueprint(teams_routes.teams, url_prefix='/teams')  # Add this line
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/403.html'), 401  # Reuse 403 template

    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('errors/400.html'), 400  # You can create a 400 page too

    return app
    
