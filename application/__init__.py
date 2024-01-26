from flask import Flask
from application.database import db
from application.models import *

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['secret_key'] = 'rkddjv7qwhiwjpowhuyudhf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.secret_key = "secret key"

db.init_app(app)

def create_su_admin():
    user = User.query.filter_by(role="super_admin").first()
    if user:
        return
    user = User("Admin", "1234567890", "admin@admin.com", "admin", "admin", "super_admin")
    db.session.add(user)
    db.session.commit()


with app.app_context():
    db.create_all()
    create_su_admin()



 