from flask import Flask
from models import User
from extensions import db, login_manager
from routes import bp

app= Flask(__name__)
app.register_blueprint(bp)

app.secret_key= "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # database path

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "main.login"




@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()




if __name__ == "__main__":

    app.run(debug=True)
