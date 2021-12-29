"""
This is the directors module and supports all the REST actions for the
directors data
"""

from flask import make_response, abort
from config import db
from models import Director, Movie, MovieSchema


def read_all():
    """
    This function responds to a request for /api/directors/movies
    with the complete list of movies, sorted by id

    :return:                json list of all movies for all directors
    """
    # Query the database for all the movies
    movies = Movie.query.order_by(db.desc(Movie.id)).limit(10)

    # Serialize the list of movies from our data
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data

def read_top_revenue():
    """
    This function responds to a request for /api/directors/movies/revenue
    with the complete list of movies, sorted by revenue

    :return:                json list of all movies for all directors
    """
    # Query the database for all the movies
    movies = Movie.query.order_by(db.desc(Movie.revenue)).limit(5)

    # Serialize the list of movies from our data
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data

def read_bot_revenue():
    """
    This function responds to a request for /api/directors/movies/revenue
    with the complete list of movies, sorted by revenue

    :return:                json list of all movies for all directors
    """
    # Query the database for all the movies
    movies = Movie.query.order_by(db.asc(Movie.revenue)).limit(5)

    # Serialize the list of movies from our data
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data


def read_one(director_id, id):
    """
    This function responds to a request for
    /api/directors/{director_id}/movies/{id}
    with one matching movie for the associated director

    :param director_id:       Id of director the movie is related to
    :param movie_id:         Id of the movie
    :return:                json string of movie contents
    """
    # Query the database for the movie
    movie = (
        Movie.query.join(Director, Director.id == Movie.director_id)
        .filter(Director.id == director_id)
        .filter(Movie.id == id)
        .one_or_none()
    )

    # Was a movie found?
    if movie is not None:
        movie_schema = MovieSchema()
        data = movie_schema.dump(movie)
        return data

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {id}")


def create(director_id, movie):
    """
    This function creates a new movie related to the passed in director id.

    :param director_id:       Id of the director the movie is related to
    :param movie:            The JSON containing the movie data
    :return:                201 on success
    """
    # get the parent director
    director = Director.query.filter(Director.id == director_id).one_or_none()

    # Was a director found?
    if director is None:
        abort(404, f"Director not found for Id: {director_id}")

    # Create a movie schema instance
    schema = MovieSchema()
    new_movie = schema.load(movie, session=db.session)

    # Add the movie to the director and database
    director.movies.append(new_movie)
    db.session.commit()

    # Serialize and return the newly created movie in the response
    data = schema.dump(new_movie)

    return data, 201


def update(director_id, id, movie):
    """
    This function updates an existing movie related to the passed in
    director id.

    :param director_id:       Id of the director the movie is related to
    :param movie_id:         Id of the movie to update
    :param content:            The JSON containing the movie data
    :return:                200 on success
    """
    update_movie = (
        Movie.query.filter(Director.id == director_id)
        .filter(Movie.id == id)
        .one_or_none()
    )

    # Did we find an existing movie?
    if update_movie is not None:

        # turn the passed in movie into a db object
        schema = MovieSchema()
        update = schema.load(movie, session=db.session)

        # Set the id's to the movie we want to update
        update.director_id = update_movie.director_id
        update.id = update_movie.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated movie in the response
        data = schema.dump(update_movie)

        return data, 200

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {id}")


def delete(director_id, id):
    """
    This function deletes a movie from the movie structure

    :param director_id:   Id of the director the movie is related to
    :param movie_id:     Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the note requested
    # note = (
    #     Note.query.filter(Person.person_id == person_id)
    #     .filter(Note.note_id == note_id)
    #     .one_or_none()
    # )
    movie = (
        Movie.query.filter(Movie.director_id== director_id)
        .filter(Movie.id == id)
        .one_or_none())


    # did we find a movie?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {id} deleted".format(id=id), 200
        )

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {id}")