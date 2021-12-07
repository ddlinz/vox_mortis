import time
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from flask import Flask, render_template, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# #
db = SQLAlchemy()

# #
@dataclass
class Entry:
    type = ""

    def __repr__(self):
        return


# #
@dataclass
class TagEntry(db.Model):
    __tablename__: str = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tag_type = db.Column(db.String(50), nullable=True)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Playlist %r>" % self.id


# #
@dataclass
class PlayListEntry(db.Model):

    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    origin_uri = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Playlist %r>" % self.id


# Users that are in the system, probably not widely used for now #
@dataclass
class UserEntry(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User %r>" % self.id


# class representing the track #
@dataclass
class TrackEntry(db.Model):

    __tablename__ = "track_entry"
    id = db.Column(db.Integer, primary_key=True)
    relative_path = db.Column(db.String(200), nullable=False)
    origin_uri = db.Column(db.String(200), nullable=True)
    service = db.Column(
        db.String(200), nullable=True
    )  # playlists have one and only one service (YT, odysee)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Track %r>" % self.id
