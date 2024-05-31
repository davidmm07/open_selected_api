from app import db
#from sqlalchemy.orm import relationship

class FavoriteMovie(db.Model):
    __tablename__ = 'favorite_movies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)