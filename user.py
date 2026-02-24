from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    sales = db.relationship('Sale', backref='owner', lazy=True, cascade="all, delete-orphan")
    expenses = db.relationship('Expense', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        from app.extensions import bcrypt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        from app.extensions import bcrypt
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'business_name': self.business_name,
            'email': self.email
        }