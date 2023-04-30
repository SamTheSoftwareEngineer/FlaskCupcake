"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cupcake(db.Model):
    """Cupcake model for application."""
    
    __tablename__ = 'cupcakes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500), nullable=False, default='https://tinyurl.com/demo-cupcake')
    
    def to_dict(self):
        """Serialize cupcake to a dictionary of cupcake info."""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image or "https://tinyurl.com/demo-cupcake"
        }

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

