from datetime import datetime

from extensions import db
class Sermon(db.Model):
    __tablename__ = 'sermons'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    preacher = db.Column(db.String(150), nullable=False)
    date_preached = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.Text)
    audio_file = db.Column(db.String(255), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
