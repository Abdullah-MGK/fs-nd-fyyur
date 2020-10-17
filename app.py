#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# [DONE] TODO: connect to a local postgresql database
db = SQLAlchemy(app)

#migration
migrate = Migrate(app, db)

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
  shows = db.relationship('Show', backref='venue', lazy=True)
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
  shows = db.relationship('Show', backref='artist', lazy=True)
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
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  
  def __repr__(self):
    return f'<id: {self.id}, start: {self.start_time}, artist: {self.artist_id}, venue: {self.venue_id}>'  


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
    format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
    format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#  Home / Index
#  ----------------------------------------------------------------

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Show Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # [DONE] TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  '''
  venues = Venue.query.order_by("name").all()
  print(venues, file = sys.stderr)
  then create a dictionary {city:state} and iterate on that dictionary to get the venues related to it from venues
  '''
  '''
  venues_area = Venue.query.filter_by(state=area.state).filter_by(city=area.city).all()
  '''
  
  areas = Venue.query.with_entities(Venue.city, Venue.state).group_by('city', 'state').all()
  print(areas, file = sys.stderr)
  
  '''
    inside the loop (as in the next method)
    for show in venue.shows:
      print(show, file = sys.stderr)
      if show.start_time > datetime.now():
        upcoming_shows += 1
  '''
  '''
    outside the loop (as in this method)
    upcoming_shows = Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all()
  '''
  
  data = []
  
  for area in areas:
    venues_area = Venue.query.filter_by(state=area.state).filter_by(city=area.city).all()
    venue_data = []
    
    for venue in venues_area:
      venue_data.append({
        "id": venue.id,
        "name": venue.name, 
        "num_upcoming_shows": len(Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now()).all())
      })
    
    data.append({
      "city": area.city,
      "state": area.state, 
      "venues": venue_data
    })
  
  return render_template('pages/venues.html', areas=data)


#  View Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  
  # [DONE] TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  print(venue, file = sys.stderr)
  
  '''
    outside the loop
    upcoming_shows = Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all()
    past_shows = Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time < datetime.now()).all()
  '''
  '''
    inside the loop
    if show.start_time > datetime.now():
      past_shows.append(show_data)
    else:
      upcoming_shows.append(show_data)
  '''
  
  past_shows = []
  upcoming_shows = []
  
  for show in venue.shows:
    print(show, file = sys.stderr)
    
    show_data = {
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time))
    }
    
    if show.start_time > datetime.now():
      upcoming_shows.append(show_data)
    else:
      past_shows.append(show_data)
  
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "city": venue.city,
    "state": venue.state,
    "address": venue.address,
    "phone": venue.phone,
    "website": venue.website,
    "image_link": venue.image_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)


#  Search Venue
#  ----------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # [DONE] TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term', '')
  result_venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []
  
  for venue in result_venues:
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all())
    })
  
  response = {
    "count": len(result_venues),
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  # renders form. do not touch.
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # called upon submitting the new venue listing form
  
  '''
  print(form.name.data, file = sys.stderr)
  # no form: name 'form' is not defined
  # form = VenueForm(): "data"
  # form = VenueForm(request.form): "data"
  print(form['name'], file = sys.stderr)
  # no form: name 'form' is not defined
  # form = VenueForm(): "the whole form object"
  # form = VenueForm(request.form): "the whole form object"
  print(request.form['gg'], file = sys.stderr)
  # no form: "data"
  # form = VenueForm(): "data"
  # form = VenueForm(request.form): "data"
  print(request.form.get('gg'), file = sys.stderr)
  # no form: "data"
  # form = VenueForm(): "data"
  # form = VenueForm(request.form): "data"
  '''
  
  form = VenueForm()
  #form = VenueForm(request.form)
  error = False
  
  try:
    # [DONE] TODO: insert form data as a new Venue record in the db
    # [DONE] TODO: modify data to be the data object returned from db insertion
    print("try", file = sys.stderr)
    
    print(form.errors, file = sys.stderr)
    if not form.validate_on_submit():
      print("invalid form", file = sys.stderr)
      error = True
      print(form.errors, file = sys.stderr)
      raise Exception("invalid data")
    
    new_venue = Venue(
      name = request.form['name'],
      genres = request.form.getlist('genres'),
      city = request.form['city'],
      state = request.form['state'],
      address = request.form['address'],
      phone = request.form['phone'],
      facebook_link = request.form['facebook_link']
    )
    
    db.session.add(new_venue)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  except:
    # [DONE] TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    print("except", file = sys.stderr)
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  
  finally:
    print("finally", file = sys.stderr)
    db.session.close()
  
  if error:
    return render_template('forms/new_venue.html', form=form)
  
  return render_template('pages/home.html')


#  Delete Venue
#  ----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # [DONE] TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  
  error = False
  
  try:
    print("try", file = sys.stderr)
    venue = Venue.query.get(venue_id)
    venue_name = venue.name
    print(venue, file = sys.stderr)
    
    db.session.delete(venue)
    #Venue.query.filter_by(id=venue_id).delete()
    
    db.session.commit()
    flash('Venue ' + venue_name + ' was deleted')
    
  except:
    print("except", file = sys.stderr)
    error = True
    flash('could not delete Venue ' + venue_name)
    db.session.rollback()
  
  finally:
    print("finally", file = sys.stderr)
    db.session.close()

  if error:
    return jsonify({'success': False})
  
  return jsonify({'success': True})


#  Edit Venue
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  
  form.name.data = venue.name
  form.genres.data = venue.genres
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.website.data = venue.website
  form.facebook_link.data = venue.facebook_link
  # [DONE] TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  error = False
  form = VenueForm()
  
  try:
    # [DONE] TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    print("try", file = sys.stderr)
    
    print(form.errors, file = sys.stderr)
    if not form.validate_on_submit():
      print("invalid form", file = sys.stderr)
      error = True
      print(form.errors, file = sys.stderr)
      raise Exception("invalid data")
    
    venue = Venue.query.get(venue_id)
    
    venue.name = request.form['name'],
    venue.genres = request.form.getlist('genres'),
    venue.city = request.form['city'],
    venue.state = request.form['state'],
    venue.address = request.form['address'],
    venue.phone = request.form['phone'],
    venue.website = request.form['website'],
    venue.facebook_link = request.form['facebook_link']
    
    db.session.commit()
    
    # on successful db update, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  
  except:
    # [DONE] TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    print("except", file = sys.stderr)
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  
  finally:
    print("finally", file = sys.stderr)
    db.session.close()
  
  if error:
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)
  
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Show Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  # [DONE] TODO: replace with real data returned from querying the database
  
  data = Artist.query.with_entities(Artist.id, Artist.name).order_by("name").all()
  print(data, file = sys.stderr)
  
  return render_template('pages/artists.html', artists=data)


#  View Artist
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  
  # [DONE] TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  print(artist, file = sys.stderr)
  
  '''
    outside the loop
    upcoming_shows = Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).all()
    past_shows = Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time < datetime.now()).all()
  '''
  '''
    inside the loop
    if show.start_time > datetime.now():
      past_shows.append(show_data)
    else:
      upcoming_shows.append(show_data)
  '''
  
  past_shows = []
  upcoming_shows = []
  
  for show in artist.shows:
    print(show, file = sys.stderr)
    
    show_data = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": format_datetime(str(show.start_time))
    }
    
    if show.start_time > datetime.now():
      upcoming_shows.append(show_data)
    else:
      past_shows.append(show_data)
  
  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "image_link": artist.image_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)


#  Search Artist
#  ----------------------------------------------------------------

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # [DONE] TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form.get('search_term', '')
  result_artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []
  
  for artist in result_artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": len(Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).all())
    })
  
  response = {
    "count": len(result_artists),
    "data": data
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  # renders form. do not touch.
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  
  '''
  print(form.name.data, file = sys.stderr)
  # no form: name 'form' is not defined
  # form = VenueForm(): "data"
  # form = VenueForm(request.form): "data"
  print(form['name'], file = sys.stderr)
  # no form: name 'form' is not defined
  # form = VenueForm(): "the whole form object"
  # form = VenueForm(request.form): "the whole form object"
  print(request.form['gg'], file = sys.stderr)
  # no form: "data"
  # form = VenueForm(): "data"
  # form = VenueForm(request.form): "data"
  print(request.form.get('gg'), file = sys.stderr)
  # no form: "data"
  # form = VenueForm(): "data"
  # form = VenueForm(request.form): "data"
  '''
  
  form = ArtistForm()
  #form = ArtistForm(request.form)
  error = False
  
  try:
    # [DONE] TODO: insert form data as a new Venue record in the db
    # [DONE] TODO: modify data to be the data object returned from db insertion
    print("try", file = sys.stderr)

    print(form.errors, file = sys.stderr)
    if not form.validate_on_submit():
      print("invalid form", file = sys.stderr)
      error = True
      print(form.errors, file = sys.stderr)
      raise Exception("invalid data")
    
    new_artist = Artist(
      name = request.form['name'],
      genres = request.form.getlist('genres'),
      city = request.form['city'],
      state = request.form['state'],
      phone = request.form['phone'],
      facebook_link = request.form['facebook_link']
    )
    
    db.session.add(new_artist)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  
  except:
    # [DONE] TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    print("except", file = sys.stderr)
    error = True
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  
  finally:
    print("finally", file = sys.stderr)
    db.session.close()
  
  if error:
    return render_template('forms/new_artist.html', form=form)
  
  return render_template('pages/home.html')


#  Delete Artist
#  ----------------------------------------------------------------

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail
  # BONUS CHALLENGE: Implement a button to delete an Artist on an Artist Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  
  error = False
  
  try:
    print("try", file = sys.stderr)
    artist = Artist.query.get(artist_id)
    artist_name = artist.name
    print(artist, file = sys.stderr)
    
    db.session.delete(artist)
    #Venue.query.filter_by(id=artist_id).delete()
    
    db.session.commit()
    flash('Artist ' + artist_name + ' was deleted')
    
  except:
    print("except", file = sys.stderr)
    error = True
    flash('could not delete Artist ' + artist_name)
    db.session.rollback()
    
  finally:
    print("finally", file = sys.stderr)
    db.session.close()
    
  if error:
   return jsonify({'success': False})
  
  return jsonify({'success': True})


#  Edit Artist
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  
  form.name.data = artist.name
  form.genres.data = artist.genres
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.facebook_link.data = artist.facebook_link
  # [DONE] TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
  error = False
  form = ArtistForm()
  
  try:
    # [DONE] TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    print("try", file = sys.stderr)

    print(form.errors, file = sys.stderr)
    if not form.validate_on_submit():
      print("invalid form", file = sys.stderr)
      error = True
      print(form.errors, file = sys.stderr)
      raise Exception("invalid data")
    
    artist = Artist.query.get(artist_id)
    
    artist.name = request.form['name'],
    artist.genres = request.form.getlist('genres'),
    artist.city = request.form['city'],
    artist.state = request.form['state'],
    artist.phone = request.form['phone'],
    artist.facebook_link = request.form['facebook_link']
    
    db.session.commit()
    
    # on successful db update, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  
  except:
    # [DONE] TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    print("except", file = sys.stderr)
    error = True
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  
  finally:
    print("finally", file = sys.stderr)
    db.session.close()
  
  if error:
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)
  
  return redirect(url_for('show_artist', artist_id=artist_id))


#  Show Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # [DONE] TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  shows = Show.query.order_by("start_time").all()
  print(shows, file = sys.stderr)
  data = []
  
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time))
    })
  
  return render_template('pages/shows.html', shows=data)


#  Create Show
#  ----------------------------------------------------------------

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  
  form = ShowForm()
  #form = VenueForm(request.form)
  error = False
  
  try:
    # [DONE] TODO: insert form data as a new Show record in the db
    # [DONE] TODO: modify data to be the data object returned from db insertion
    print("try", file = sys.stderr)
    
    new_show = Show(
      start_time = request.form['start_time'],
      artist_id = request.form['artist_id'],
      venue_id = request.form['venue_id']
    )
    
    db.session.add(new_show)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  
  except:
    # [DONE] TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    print("except", file = sys.stderr)
    error = True
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  
  finally:
    print("finally", file = sys.stderr)
    db.session.close()
  
  if error:
    return render_template('forms/new_show.html', form=form)
  
  return render_template('pages/home.html')


#  Error Handlers
#  ----------------------------------------------------------------

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
