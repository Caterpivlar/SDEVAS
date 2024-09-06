from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CARDS(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	deck_id = db.Column(db.String(100), nullable=False)
	username = db.Column(db.String(100), nullable=False)
	cards = db.Column(db.String, nullable=False)
	datetime = db.Column(db.DateTime, nullable=False)