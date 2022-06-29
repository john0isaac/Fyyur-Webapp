#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime, timezone
from sqlalchemy import or_
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# TODO: connect to a local postgresql database
from models import db, Artist, Venue, Show
migrate = Migrate(app, db)

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  cities = db.session.query(Venue.city).group_by(Venue.city).all()
  current_time = datetime.now(timezone.utc)
  current_city=' '
  data=[]
  for city in cities:
      venues = db.session.query(Venue).filter(Venue.city == city[0]).order_by('id').all()
      for venue in venues:
          num_upcoming_shows = venue.shows.filter(Show.start_time > current_time).all()       
          if current_city != venue.city:
                data.append({
                "city":venue.city,
                "state":venue.state,
                "venues":[{
                "id": venue.id,
                "name":venue.name,
                "num_upcoming_shows": len(num_upcoming_shows)}]
                })
                current_city=venue.city
          else: 
            data[len(data) - 1]["venues"].append({
                "id": venue.id,
                "name":venue.name,
                "num_upcoming_shows": len(num_upcoming_shows)
              })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  term = request.form.get('search_term')
  search = "%{}%".format(term.lower())
  res= Venue.query.filter(or_(Venue.name.ilike(search), Venue.city.ilike(search), Venue.state.ilike(search))).all()
  response = {'count':len(res),'data':res}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = db.session.query(Venue).filter(Venue.id == venue_id).all()
  current_time = datetime.now(timezone.utc)
  data= {}
  down_show = []
  up_show = []
  for col in venue:
        upcoming_shows = col.shows.filter(Show.start_time > current_time).all()
        past_shows = col.shows.filter(Show.start_time < current_time).all()
        data.update({
        "id": col.id,
        "name": col.name,
        "genres": col.genres.split(", "),
        "address": col.address,
        "city": col.city,
        "state": col.state,
        "phone": col.phone,
        "website": col.website,
        "facebook_link": col.facebook_link,
        "seeking_talent": col.seeking_talent,
        "seeking_description": col.seeking_description,
        "image_link": col.image_link,
        })
        for show in upcoming_shows:
            if len(upcoming_shows) == 0:
                  data.update({"upcoming_shows": [],})
            else:
                  artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == show.artist_id).one()
                  up_show.append({
                  "artist_id": show.artist_id,
                  "artist_name": artist.name,
                  "artist_image_link": artist.image_link,
                  "start_time": show.start_time.strftime('%m/%d/%Y'),
                  })
        for show in past_shows:
            if len(past_shows) == 0:
                  data.update({"past_shows": [],})
            else:
                  artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == show.artist_id).one()
                  down_show.append({
                  "artist_id": show.artist_id,
                  "artist_name": artist.name,
                  "artist_image_link": artist.image_link,
                  "start_time": show.start_time.strftime('%m/%d/%Y'),
                  })
        data.update({"upcoming_shows": up_show})
        data.update({"past_shows": down_show})
        data.update({"past_shows_count": len(past_shows), "upcoming_shows_count": len(upcoming_shows),})
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
  try:
    data = Venue()
    data.name = request.form.get('name')
    data.genres = ', '.join(request.form.getlist('genres'))
    data.address = request.form.get('address')
    data.city = request.form.get('city')
    data.state = request.form.get('state')
    data.phone = request.form.get('phone')
    data.facebook_link = request.form.get('facebook_link')
    data.image_link = request.form.get('image_link')
    data.website = request.form.get('website_link')
    data.seeking_talent = True if request.form.get('seeking_talent')!= None else False
    data.seeking_description = request.form.get('seeking_description')

    db.session.add(data)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + request.form.get('name') + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    abort(500)
  return render_template('pages/home.html')
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  if not error:
    return render_template('pages/home.html'), 200
  else:
    abort(500)
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[]
  artists = db.session.query(Artist).order_by('id').all()
  for artist in artists:   
      data.append({
          "id":artist.id,
          "name":artist.name,
          })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  term = request.form.get('search_term')
  search = "%{}%".format(term.lower())
  res= Artist.query.filter(or_(Artist.name.ilike(search), Artist.city.ilike(search), Artist.state.ilike(search))).all()
  response = {'count':len(res),'data':res}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = db.session.query(Artist).filter(Artist.id == artist_id).all()
  current_time = datetime.now(timezone.utc)
  data= {}
  down_show = []
  up_show = []
  for col in artist:
        upcoming_shows = col.shows.filter(Show.start_time > current_time).all()
        past_shows = col.shows.filter(Show.start_time < current_time).all()
        data.update({
        "id": col.id,
        "name": col.name,
        "genres": col.genres.split(", "),
        "city": col.city,
        "state": col.state,
        "phone": col.phone,
        "website": col.website,
        "facebook_link": col.facebook_link,
        "seeking_venue": col.seeking_venue,
        "seeking_description": col.seeking_description,
        "image_link": col.image_link,
        })
        for show in upcoming_shows:
            if len(upcoming_shows) == 0:
                  data.update({"upcoming_shows": [],})
            else:
                  venue = db.session.query(Venue.name, Venue.image_link).filter(Venue.id == show.venue_id).one()
                  up_show.append({
                  "venue_id": show.venue_id,
                  "venue_name": venue.name,
                  "venue_image_link": venue.image_link,
                  "start_time": show.start_time.strftime('%m/%d/%Y'),
                  })
        for show in past_shows:
            if len(past_shows) == 0:
                  data.update({"past_shows": [],})
            else:
                  venue = db.session.query(Venue.name, Venue.image_link).filter(Venue.id == show.venue_id).one()
                  down_show.append({
                  "venue_id": show.venue_id,
                  "venue_name": venue.name,
                  "venue_image_link": venue.image_link,
                  "start_time": show.start_time.strftime('%m/%d/%Y'),
                  })
        data.update({"upcoming_shows": up_show})
        data.update({"past_shows": down_show})
        data.update({"past_shows_count": len(past_shows), "upcoming_shows_count": len(upcoming_shows),})
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  data = Artist.query.get(artist_id)
  artist={
    "id": data.id,
    "name": data.name,
    "genres": data.genres.split(", "),
    "city": data.city,
    "state": data.state,
    "phone": data.phone,
    "website_link": data.website,
    "facebook_link": data.facebook_link,
    "seeking_venue": data.seeking_venue,
    "seeking_description": data.seeking_description,
    "image_link": data.image_link,
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    data = Artist.query.get(artist_id)

    # using request.form.get is safer than accessing the value directly to handel null cases
    data.name = request.form.get('name')
    data.genres = ', '.join(request.form.getlist('genres'))
    data.city = request.form.get('city')
    data.state = request.form.get('state')
    data.phone = request.form.get('phone')
    data.facebook_link = request.form.get('facebook_link')
    data.image_link = request.form.get('image_link')
    data.website = request.form.get('website_link')
    data.seeking_venue = True if request.form.get('seeking_venue')!=None else False
    data.seeking_description = request.form.get('seeking_description')
    db.session.add(data)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  data = Venue.query.get(venue_id)
  venue={
    "id": data.id,
    "name": data.name,
    "genres": data.genres.split(", "),
    "address": data.address,
    "city": data.city,
    "state": data.state,
    "phone": data.phone,
    "website": data.website,
    "facebook_link": data.facebook_link,
    "seeking_talent": data.seeking_talent,
    "seeking_description": data.seeking_description,
    "image_link": data.image_link,
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    data = Venue.query.get(venue_id)

    data.name = request.form.get('name')
    data.genres = ', '.join(request.form.getlist('genres'))
    data.address = request.form.get('address')
    data.city = request.form.get('city')
    data.state = request.form.get('state')
    data.phone = request.form.get('phone')
    data.facebook_link = request.form.get('facebook_link')
    data.image_link = request.form.get('image_link')
    data.website = request.form.get('website_link')
    data.seeking_talent = True if request.form.get('seeking_talent')!=None else False
    data.seeking_description = request.form.get('seeking_description')
    db.session.add(data)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
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
  error = False
  try:
    data = Artist()
    data.name = request.form.get('name')
    data.genres = ', '.join(request.form.getlist('genres'))
    data.city = request.form.get('city')
    data.state = request.form.get('state')
    data.phone = request.form.get('phone')
    data.facebook_link = request.form.get('facebook_link')
    db.session.add(data)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Artist ' + request.form.get('name') + ' was successfully listed!')
  else:
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
    abort(500)
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/artists/<artist_id>/delete', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  if not error:
    return render_template('pages/home.html'), 200
  else:
    abort(500)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows = db.session.query(Show).all()
  for show in shows:
        artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == show.artist_id).one()
        venue = db.session.query(Venue.name).filter(Venue.id == show.venue_id).one()
        data.append({
          "venue_id": show.venue_id,
          "venue_name": venue.name,
          "artist_id": show.artist_id,
          "artist_name":artist.name,
          "artist_image_link": artist.image_link,
          "start_time": show.start_time.strftime('%m/%d/%Y')
        })
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
  try:
    data = Show()
    data.venue_id = request.form.get('venue_id')
    data.artist_id = request.form.get('artist_id')
    data.start_time = request.form.get('start_time')
    db.session.add(data)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
    abort(500)
  return render_template('pages/home.html')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

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
