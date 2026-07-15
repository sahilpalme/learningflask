from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required

db = SQLAlchemy()
login_manager = LoginManager()