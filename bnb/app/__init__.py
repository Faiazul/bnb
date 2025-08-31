import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max size
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # redirect unauthorized users

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.property import property_bp  
    app.register_blueprint(property_bp, url_prefix='/property')

    from app.routes.profile import profile_bp
    app.register_blueprint(profile_bp)

    from app.routes.booking import booking_bp
    app.register_blueprint(booking_bp, url_prefix='/booking')

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.review import review_bp
    app.register_blueprint(review_bp)

    from app.routes.wishlist import wishlist_bp
    app.register_blueprint(wishlist_bp)

    from app.routes.message import message_bp
    app.register_blueprint(message_bp, url_prefix='/messages')

    with app.app_context():
        db.create_all()
    
    return app
