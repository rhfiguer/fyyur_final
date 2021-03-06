#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser 
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
import datetime


from models import app, db, Venue, Artist, Show  # Olouge E mentor mentioned this to connect models.py to app.py: https://knowledge.udacity.com/questions/89940


db.init_app(app)
db.app = app

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO [!! DONE    ]: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#Moved Models to models.py



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO : replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  #We group venues by city and state. Source for this code was Juliano V in Udacity Technincal Support: https://knowledge.udacity.com/questions/501471 
  locals = []
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()
  for place in places:
    locals.append({
      'city':place.city,
      'state': place.state,
      'venues':[{
        'id':venue.id,
        'name':venue.name
      } for venue in venues if venue.city ==place.city and venue.state ==place.state
      ]
    })

 #data=[{
 #  "city": "San Francisco",
 #  "state": "CA",
 #  "venues": [{
 #    "id": 1,
 #    "name": "The Musical Hop",
 #    "num_upcoming_shows": 0,
 #  }, {
 #    "id": 3,
 #    "name": "Park Square Live Music & Coffee",
 #    "num_upcoming_shows": 1,
 #  }]
 #}, {
 #  "city": "New York",
 #  "state": "NY",
 #  "venues": [{
 #    "id": 2,
 #    "name": "The Dueling Pianos Bar",
 #    "num_upcoming_shows": 0,
 #  }]
 #}]
  
  
  return render_template('pages/venues.html', areas=locals)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term', ' ')
  search = "%{0}%".format(search_term) #Partial string search. One of teh sources for this code was: https://stackoverflow.com/questions/14971619/proper-use-of-mysql-full-text-search-with-sqlalchemy
  response = Venue.query.filter(Venue.name.ilike(search)).all() # Case insensitive. I googled how to query for text case insesnsitive and found ilike.
  counts = Venue.query.filter(Venue.name.ilike(search)).count() #Counting responses



  #response= 
 #{
 #  "count": 1,
 #  "data": [{
 #    "id": 2,
 #    "name": "The Dueling Pianos Bar",
 #    "num_upcoming_shows": 0,
 #  }]
 #}
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term, count = counts)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  '''
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  '''
  venue = Venue.query.filter_by(id=venue_id).first()
  data = {
            'id': venue.id,
            'name': venue.name,
            'genres': venue.genres,
            'address': venue.address,
            'city': venue.city,
            'state': venue.state,
            'phone': venue.phone,
            'website': venue.website_link,
            'facebook_link': venue.facebook_link,
            'image_link': venue.image_link,

    }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  error = False
  data = request.form
  vname = data['name']
  vcity = data['city']
  vstate = data['state']
  vaddress = data['address']
  vphone = data['phone']
  vgenres = data['genres']
  vfb_link = data['facebook_link']
  wlink = data['website_link']
  vimage_link = data['image_link']
  
  try:
      db.session.add(Venue(
          city=vcity,
          state=vstate,
          name=vname,
          address=vaddress,
          phone=vphone,
          facebook_link=vfb_link,
          genres=vgenres,
          website_link = wlink,
          image_link = vimage_link
  
      ))
      
  finally:
      if not error:
          db.session.commit()
          flash('Venue ' + request.form['name'] +' was successfully listed!')
      else:
          flash('An error occurred. Venue ' + vname + ' could not be listed.')
          db.session.rollback()
  
  return render_template('pages/home.html')


 ## TODO: [DONE!!!] on unsuccessful db insert, flash an error instead.
##e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
##see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
  # TODO: [DONE!!!] insert form data as a new Venue record in the db, instead 
  # TODO: [DONE!!!] modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO [??????DONE]: replace with real data returned from querying the database
  data=Artist.query.all()
 #[{
 #  "id": 4,
 #  "name": "Guns N Petals",
 #}, {
 #  "id": 5,
 #  "name": "Matt Quevedo",
 #}, {
 #  "id": 6,
 #  "name": "The Wild Sax Band",
 #}]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', ' ')
  search = "%{0}%".format(search_term) #Partial string search. One of teh sources for this code was: https://stackoverflow.com/questions/14971619/proper-use-of-mysql-full-text-search-with-sqlalchemy
  response = Artist.query.filter(Artist.name.ilike(search)).all() # Case insensitive. I googled how to query for text case insesnsitive and found ilike.
  counts = Artist.query.filter(Artist.name.ilike(search)).count() #Counting responses


# response={
#   "count": 1,
#   "data": [{
#     "id": 4,
#     "name": "Guns N Petals",
#     "num_upcoming_shows": 0,
#   }]
# }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term, count = counts)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
# data1={
#   "id": 4,
#   "name": "Guns N Petals",
#   "genres": ["Rock n Roll"],
#   "city": "San Francisco",
#   "state": "CA",
#   "phone": "326-123-5000",
#   "website": "https://www.gunsnpetalsband.com",
#   "facebook_link": "https://www.facebook.com/GunsNPetals",
#   "seeking_venue": True,
#   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#   "past_shows": [{
#     "venue_id": 1,
#     "venue_name": "The Musical Hop",
#     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#     "start_time": "2019-05-21T21:30:00.000Z"
#   }],
#   "upcoming_shows": [],
#   "past_shows_count": 1,
#   "upcoming_shows_count": 0,
# }
# data2={
#   "id": 5,
#   "name": "Matt Quevedo",
#   "genres": ["Jazz"],
#   "city": "New York",
#   "state": "NY",
#   "phone": "300-400-5000",
#   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
#   "seeking_venue": False,
#   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#   "past_shows": [{
#     "venue_id": 3,
#     "venue_name": "Park Square Live Music & Coffee",
#     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     "start_time": "2019-06-15T23:00:00.000Z"
#   }],
#   "upcoming_shows": [],
#   "past_shows_count": 1,
#   "upcoming_shows_count": 0,
# }
# data3={
#   "id": 6,
#   "name": "The Wild Sax Band",
#   "genres": ["Jazz", "Classical"],
#   "city": "San Francisco",
#   "state": "CA",
#   "phone": "432-325-5432",
#   "seeking_venue": False,
#   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#   "past_shows": [],
#   "upcoming_shows": [{
#     "venue_id": 3,
#     "venue_name": "Park Square Live Music & Coffee",
#     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     "start_time": "2035-04-01T20:00:00.000Z"
#   }, {
#     "venue_id": 3,
#     "venue_name": "Park Square Live Music & Coffee",
#     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     "start_time": "2035-04-08T20:00:00.000Z"
#   }, {
#     "venue_id": 3,
#     "venue_name": "Park Square Live Music & Coffee",
#     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     "start_time": "2035-04-15T20:00:00.000Z"
#   }],
#   "past_shows_count": 0,
#   "upcoming_shows_count": 3,
# }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  
  artist = Artist.query.filter_by(id=artist_id).first()
  data = {
  'id': artist.id,
  'name': artist.name,
  'city': artist.city,
  'state': artist.state,
  'genres': artist.genres,
  'phone': artist.phone,
  'website': artist.website_link,
  'facebook_link': artist.facebook_link,
  'image_link': artist.image_link
  }

  return render_template('pages/show_artist.html', artist = data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
#artist={
#  "id": 4,
#  "name": "Guns N Petals",
#  "genres": ["Rock n Roll"],
#  "city": "San Francisco",
#  "state": "CA",
#  "phone": "326-123-5000",
#  "website": "https://www.gunsnpetalsband.com",
#  "facebook_link": "https://www.facebook.com/GunsNPetals",
#  "seeking_venue": True,
#  "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#  "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
#}

  #Query model using variable to be passed
  artist = Artist.query.get(artist_id)
  
  #Definining vars in DATA to be sent to JINJA
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }

  # TODO: populate form with fields from artist with ID <artist_id>
  
  #Sending final view to Jinja
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error=False
  artist = Artist.query.get(artist_id)
  artist.name = request.form['name']
  artist.city = request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  artist.facebook_link = request.form['facebook_link']
  artist.genres = request.form['genres']
  artist.image_link = request.form['image_link']
  artist.website = request.form['website_link']
  
  #Updating through commit
  try:
    db.session.commit()

  finally:
    if not error:

      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully edited!')
      db.session.close()
    else:
      # TODO: on unsuccessful db insert, flash an error instead.
# e.g., 
      flash('An error occurred. Artist ' + data.name + ' could not be edited.')
      db.session.rollback()

  #Sending variables to Jinja

  return redirect(url_for('show_artist', artist_id=artist_id))





  return redirect(url_for('show_artist', artist=data))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
# venue={
#   "id": 1,
#   "name": "The Musical Hop",
#   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#   "address": "1015 Folsom Street",
#   "city": "San Francisco",
#   "state": "CA",
#   "phone": "123-123-1234",
#   "website": "https://www.themusicalhop.com",
#   "facebook_link": "https://www.facebook.com/TheMusicalHop",
#   "seeking_talent": True,
#   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
# }
  
  #QUERY MODEL TO GET PROCEED WITH DATA
  artist = Venue.query.get(venue_id)
  data = {
  'id': artist.id,
  'name': artist.name,
  'city': artist.city,
  'state': artist.state,
  'genres': artist.genres,
  'phone': artist.phone,
  'website': artist.website_link,
  'facebook_link': artist.facebook_link,
  'image_link': artist.image_link
  }

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  error=False
  artist = Venue.query.get(venue_id)
  artist.name = request.form['name']
  artist.city = request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  artist.facebook_link = request.form['facebook_link']
  artist.genres = request.form['genres']
  artist.image_link = request.form['image_link']
  artist.website = request.form['website_link']
  
  #Updating through commit
  try:
    db.session.commit()

  finally:
    if not error:

      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully edited!')
      db.session.close()
    else:
      # TODO: on unsuccessful db insert, flash an error instead.
# e.g., 
      flash('An error occurred. Venue ' + data.name + ' could not be edited.')
      db.session.rollback()

  #Sending variables to Jinja
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error=False
  data = request.form
  aname=data['name']
  acity=data['city']
  astate=data['state']
  aphone=data['phone']
  agenres=data['genres']
  aimage_link=data['image_link']
  afacebook_link =data['facebook_link']
  awebsite_link = data['website_link']
  #alooking_venues=data['seeking_venue']
  aseeking_description=data['seeking_description']
  try:
    db.session.add(Artist(
      city = acity,
      name = aname,
      state = astate,
      phone = aphone,
      genres = agenres,
      image_link = aimage_link,
      facebook_link = afacebook_link,
      website_link = awebsite_link,
      #seeking_venue = alooking_venues,
      seeking_description = aseeking_description
    ))

  finally:
    if not error:
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      db.session.close()

    else:
      # TODO: on unsuccessful db insert, flash an error instead.
# e.g., 
      flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      db.session.rollback()
  
  return render_template('pages/home.html')
      


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  shows = Show.query.all() 
  data = [] #Source for append solution was Ahmed Sharshar on Fyyur project: https://github.com/mahmoud-sharshar/Fyyur-Artist-Booking-Site/blob/master/app.py
  for show in shows:
    data.append({
      "start_time": str(show.start_time),
      "venue_id": show.venue_id,
      "artist_image_link": show.artist.image_link,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name
      })
  
# data=[{
#  "venue_id": 1,
#  "venue_name": "The Musical Hop",
#  "artist_id": 4,
#  "artist_name": "Guns N Petals",
#  "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#  "start_time": "2019-05-21T21:30:00.000Z"
#}, {
#  "venue_id": 3,
#  "venue_name": "Park Square Live Music & Coffee",
#  "artist_id": 5,
#  "artist_name": "Matt Quevedo",
#  "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#  "start_time": "2019-06-15T23:00:00.000Z"
#}, {
#  "venue_id": 3,
#  "venue_name": "Park Square Live Music & Coffee",
#  "artist_id": 6,
#  "artist_name": "The Wild Sax Band",
#  "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#  "start_time": "2035-04-01T20:00:00.000Z"
#}, {
#  "venue_id": 3,
#  "venue_name": "Park Square Live Music & Coffee",
#  "artist_id": 6,
#  "artist_name": "The Wild Sax Band",
#  "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#  "start_time": "2035-04-08T20:00:00.000Z"
#}, {
#  "venue_id": 3,
#  "venue_name": "Park Square Live Music & Coffee",
#  "artist_id": 6,
#  "artist_name": "The Wild Sax Band",
#  "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#  "start_time": "2035-04-15T20:00:00.000Z"
#}]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error=False
  data = request.form
  artist_id=data['artist_id']
  venue_id=data['venue_id']
  start_time=data['start_time']
  try:
    db.session.add(Show(
    artist_id=artist_id,
    venue_id=venue_id,
    start_time = start_time
   ))

  finally:
    if not error:
      db.session.commit()
#     # on successful db insert, flash success
      flash('Show was successfully listed!')
#   
    else:
#     # TODO: on unsuccessful db insert, flash an error instead.
# e.g., 
      flash('An error occurred. Show could not be listed.')
      db.session.rollback()
# # on successful db insert, flash success
# 
# # TODO: on unsuccessful db insert, flash an error instead.
# # e.g., flash('An error occurred. Show could not be listed.')
# # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
