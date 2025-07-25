from datetime import datetime
from extensions import db

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    membership_status = db.Column(db.String(20), nullable=False, default='Visitor')  # Baptised / Not Baptised / Visitor
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Foreign key to Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    admin = db.relationship('Admin', back_populates='members')


    def __repr__(self):
        return f"<Member {self.full_name} - {self.membership_status}>"
