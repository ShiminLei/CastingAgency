from flask import Flask
from flask_sqlalchemy import SQLAlchemy


database_path = 'postgresql://postgres:e2806387@localhost:5432/capstone'
db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Helper table

actors = db.Table('actors', db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
                  db.Column('movie_id', db.Integer, db.ForeignKey(
                      'movie.id'), primary_key=True)

                  )

# Actor


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    def attributes(self):
        return {
            'id' : self.id, 
            'name' : self.name, 
            'age' : self.age,
            'gender' : self.gender, 
            'movies' : [movie.attributes for movie in self.movies]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# Movie


class Movie(db.Model):
    __tablename = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    release_date = db.Column(db.DateTime())
    actors = db.relationship('Actor', secondary=actors, lazy='dynamic',
                             backref=db.backref('movies'), cascade='delete-orphan')

    def attributes(self):
        return {
            'id' : self.id, 
            'title' : self.title, 
            'release_date' : self.release_date,
            'actors' : [ actor.attributes for actor in self.actors]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
