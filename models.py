from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


from datetime import datetime

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    module = db.Column(db.String(50), nullable=False)
    user_input = db.Column(db.Text, nullable=False)
    ai_output = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


from database import db
from datetime import datetime

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)

    image = db.Column(db.String(200))
    prediction = db.Column(db.String(100))
    fertilizer = db.Column(db.String(200))
    quantity = db.Column(db.String(200))

    date = db.Column(db.DateTime, default=datetime.utcnow)