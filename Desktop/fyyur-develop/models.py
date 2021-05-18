#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# Config
#----------------------------------------------------------------------------#
app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable = False )
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  address = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120), nullable=True)
  genres=db.Column(db.String(120), nullable=True)
  image_link = db.Column(db.String(500), nullable = True)
  facebook_link = db.Column(db.String(500), nullable = True)
  website_link = db.Column(db.String(500), nullable = True)
  seeking_talent = db.Column(db.Boolean, default=False, nullable = True)
  seeking_description= db.Column(db.String(500), nullable = True)
  Show = db.relationship('Show', backref = 'venue', lazy="joined" )



    # TODO [¡¡¡¡¡DONE]: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable = False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable = True)
    facebook_link = db.Column(db.String(500), nullable = True)
    website_link = db.Column(db.String(500), nullable = True)
    seeking_venue = db.Column(db.Boolean, nullable = True, default = False)
    seeking_description = db.Column(db.String(120), nullable = True)
    Show = db.relationship('Show', backref = 'artist', lazy="joined" )

class Show(db.Model):
  __tablename__= 'Shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)  
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)  
  start_time= db.Column(db.DateTime, nullable=False)


    # TODO [¡¡¡¡DONE]: implement any missing fields, as a database migration using Flask-Migrate

# TODO [¡¡¡¡DONE] Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

