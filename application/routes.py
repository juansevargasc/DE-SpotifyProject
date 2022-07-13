from application import app
from flask import jsonify, request
from application.spotipy_methods import *
from application.models import *
from application.iso_country_codes import CC

# ROUTES
# Health - ping tests
@app.route('/ping')
def ping_route():
    db.engine.execute('SELECT 1')
    return ''

# Testing get request
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'msg': 'Hello World'})



# ARTIST
# Create
@app.route('/artists', methods=['POST'])
def add_artist():
    id = request.json['id']
    name = request.json['name']
    image_url = request.json['image_url']
    followers = request.json['followers']

    new_artist = Artist(id, name, image_url, followers)

    db.session.add(new_artist)
    db.session.commit()


    return artist_schema.jsonify(new_artist)
# Read all
@app.route('/artists', methods=['GET'])
def get_artists():
    if len( Artist.query.all() ) != 0:
        all_artists = Artist.query.all()
        result = artists_schema.dump(all_artists)
        return jsonify(result)


# Read one
@app.route('/artists/<id>', methods=['GET'])
def get_artist(id):
    artist = Artist.query.get(id)
    return artist_schema.jsonify(artist)
# Update one
@app.route('/artists/<id>', methods=['PUT'])
def update_artist(id):
    # Get artist
    artist = Artist.query.get(id)

    name = request.json['name']
    image_url = request.json['image_url']
    followers = request.json['followers']

    # Update python class
    artist.name = name
    artist.image_url = image_url
    artist.followers = followers

    # Update on DB
    db.session.commit()

    return artist_schema.jsonify(artist)
# Delete one
@app.route('/artists/<id>', methods=['DELETE'])
def delete_artist(id):
    # Get artist
    artist = Artist.query.get(id)
    # Delete that artist
    db.session.delete(artist)

    # Commit that change
    db.session.commit()

    return artist_schema.jsonify(artist)

#COUNTRY
# Read all
@app.route('/countries', methods=['GET'])
def get_countries():
    if len( Country.query.all() ) != 0:
        all_countries = Country.query.all()
        result = countries_schema.dump(all_countries)

        return jsonify(result)
    else:
        countries = get_countries_from_spotify()
        for idx, country in enumerate(countries):
            id = idx
            code = country
            name = CC[code]

            new_coutry = Country(id, code, name)

            db.session.add(new_coutry)
            db.session.commit()
        return 'Success'
        

# ALBUM ###################
# # Create
# @app.route('/albums', methods=['POST'])
# def add_artist():
#     id = request.json['id']
#     name = request.json['name']
#     url = request.json['url']
#     followers = request.json['followers']

#     new_artist = Artist(id, name, url, followers)

#     db.session.add(new_artist)
#     db.session.commit()

#     return artist_schema.jsonify(new_artist)
# # Read all
# @app.route('/artists', methods=['GET'])
# def get_artists():
#     all_artists = Artist.query.all()
#     result = artists_schema.dump(all_artists)

#     return jsonify(result)
# # Read one
# @app.route('/artists/<id>', methods=['GET'])
# def get_artist(id):
#     artist = Artist.query.get(id)
#     return artist_schema.jsonify(artist)
# # Update one
# @app.route('/artists/<id>', methods=['PUT'])
# def update_artist(id):
#     # Get artist
#     artist = Artist.query.get(id)

#     name = request.json['name']
#     url = request.json['url']
#     followers = request.json['followers']

#     # Update python class
#     artist.name = name
#     artist.url = url
#     artist.followers = followers

#     # Update on DB
#     db.session.commit()

#     return artist_schema.jsonify(artist)
# # Delete one
# @app.route('/artists/<id>', methods=['DELETE'])
# def delete_artist(id):
#     # Get artist
#     artist = Artist.query.get(id)
#     # Delete that artist
#     db.session.delete(artist)

#     # Commit that change
#     db.session.commit()

#     return artist_schema.jsonify(artist)

