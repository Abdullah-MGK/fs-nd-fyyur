#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import babel
import dateutil.parser
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
#from app import db

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#  Venue
#  ----------------------------------------------------------------

# [DONE] TODO: implement any missing fields, as a database migration using Flask-Migrate
class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  genres = db.Column(db.ARRAY(db.String))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  website = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  shows = db.relationship('Show', backref='venue', lazy=True, cascade="all, delete-orphan")
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String)
  
  def __repr__(self):
    return f'<id: {self.id}, name: {self.name}, shows: {self.shows}>'


#  Artist
#  ----------------------------------------------------------------

# [DONE] TODO: implement any missing fields, as a database migration using Flask-Migrate
class Artist(db.Model):
  __tablename__ = 'Artist'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  genres = db.Column(db.ARRAY(db.String))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  website = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  shows = db.relationship('Show', backref='artist', lazy=True, cascade="all, delete-orphan")
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String)
  
  def __repr__(self):
    return f'<id: {self.id}, name: {self.name}, shows: {self.shows}>'


#  Show
#  ----------------------------------------------------------------

# [DONE] TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# [DONE] TODO: implement any missing fields, as a database migration using Flask-Migrate
class Show(db.Model):
  __tablename__ = 'Show'
  
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete="CASCADE"), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete="CASCADE"), nullable=False)
  
  def __repr__(self):
    return f'<id: {self.id}, start: {self.start_time}, artist: {self.artist_id}, venue: {self.venue_id}>'  

