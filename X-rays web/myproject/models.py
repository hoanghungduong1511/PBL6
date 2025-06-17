from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.types import Enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    birth_day = db.Column(db.Date, nullable=False)
    gender = db.Column(Enum('Male', 'Female', 'Other', name='gender_types'), nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    diagnose_name = db.Column(db.String(128))
    diagnose_image = db.Column(db.String(128))
    role = db.Column(db.String(50))  # 'doctor' or 'patient'

    def __init__(self, email, phone_number, birth_day, gender, name, username, password,role='patient',diagnose_name=None,diagnose_image=None):
        self.email = email
        self.phone_number = phone_number
        self.birth_day = birth_day
        self.gender = gender
        self.name = name
        self.username = username
        self.role = role
        self.diagnose_name = diagnose_name
        self.diagnose_image = diagnose_image
        self.set_password(password)  # Sử dụng hàm set_password để mã hóa mật khẩu

    def set_password(self, password):
        """Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Kiểm tra mật khẩu người dùng nhập vào có khớp với hash trong cơ sở dữ liệu không."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
