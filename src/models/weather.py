from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    temperature_2m = db.Column(db.Float, nullable=False)
    relative_humidity_2m = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WeatherData {self.timestamp} - {self.temperature_2m}°C, {self.relative_humidity_2m}%>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'temperature_2m': self.temperature_2m,
            'relative_humidity_2m': self.relative_humidity_2m,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

