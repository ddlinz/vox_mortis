import time
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from flask import Flask, render_template, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


# Example of playlist information here
# playtlist_template = {'_type': 'playlist', 
#  'entries': [], 
#  'id': 'PLRbcQXWEJAJodbx1C5k...FEivYlVCvZ', 
#  'title': 'free_classical', 
#  'uploader': 'The Distributist', 
#  'uploader_id': 'UCdHT7KB1gDAXZYpPW71fn0Q', 
#  'uploader_url': 'https://www.youtube....stributist', 
#  'extractor': 'youtube:tab', 
#  'webpage_url': 'https://www.youtube....FEivYlVCvZ', 
#  'webpage_url_basename': 
#  'playlist', 
# #  'extractor_key': 'YoutubeTab'}

playtlist_template = {
    '_type':'playlist', 
    'entries':[], 
    'id': None, 
    'title': None, 
    'uploader': None,
    'uploader_id':None,
    'uploader_url':None,
    'extractor': None,
    'webpage_url': None, 
    'webpage_url_basename': None,
    'extractor_key': None,
}

track_template =  {
    'id':None, 
	'title':None, 
	'formats': [], 
	'thumbnails':None, 
	'description':None, 
	'upload_date':None, 
	'uploader':None, 
	'uploader_id':None, 
	'uploader_url':None, 
	'channel_id':None, 
	'channel_url':None, 
	'duration':None, 
	'view_count':None, 
	'average_rating':None, 
	'age_limit':None, 
	'webpage_url':None, 
	'categories':None, 
	'tags':None, 
	'is_live':None, 
	'like_count':None, 
	'channel':None, 
	'track':None, 
	'artist':None, 
	'album':None, 
	'creator':None, 
	'alt_title':None, 
	'extractor':None, 
	'webpage_url_basename':None, 
	'extractor_key':None, 
	'n_entries':None, 
	'playlist':None, 
	'playlist_id':None, 
	'playlist_title':None, 
	'playlist_uploader':None, 
	'playlist_uploader_id':None, 
	'playlist_index':None, 
	'thumbnail':None, 
	'display_id':None, 
	'requested_subtitles':None, 
	'requested_formats':None, 
	'format':None, 
	'format_id':None, 
	'width':None, 
	'height':None, 
	'resolution':None, 
	'fps':None, 
	'vcodec':None, 
	'vbr':None, 
	'stretched_ratio':None, 
	'acodec':None, 
	'abr': None, 
	'ext': None
 }

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

# webpage_url #
@dataclass
class PlayListEntry(db.Model):


    # '_type', 'entries', 'id', 'title', 'uploader', 'uploader_id', 
    # 'uploader_url', 'extractor', 'webpage_url', 'webpage_url_basename', 'extractor_key

    # a dictionary to describe the mappings from the YT object #
    usable_entry_list_yt = {'title':'title', 'id':'archive_id', 'entries':'noref', 'uploader':'author', 'webpage_url':'origin_uri'}


    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    origin_uri = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    native_id = db.Column(db.String(200), nullable=True)

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
    # ['id', 'title', 'formats', 'thumbnails', 'description', 'upload_date', 'uploader', 'uploader_id', 'uploader_url', 
    # 'channel_id', 'channel_url', 'duration', 'view_count', 'average_rating', 'age_limit', 'webpage_url', 'categories', 'tags',
    # 'is_live', 'like_count', 'channel', 'track', 'artist', 'album', 'creator', 'alt_title', 'extractor', 'webpage_url_basename',
    # 'extractor_key', 'n_entries', 'playlist', 'playlist_id', 'playlist_title', 'playlist_uploader', 'playlist_uploader_id', 'playlist_index',
    # 'thumbnail', 'display_id', 'requested_subtitles', 'requested_formats', 'format', 'format_id', 'width', 'height', 'resolution', 'fps', 
    # 'vcodec', 'vbr', 'stretched_ratio', 'acodec', 'abr', 'ext']
    # 'id', 'title', 'formats',


    __tablename__ = "track_entry"
    id = db.Column(db.Integer, primary_key=True)
    # relative_path = db.Column(db.String(200), nullable=False)
    origin_uri = db.Column(db.String(200), nullable=True)
    playlist_origin =  db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Track %r>" % self.id


# class representing the track #
@dataclass
class ArchiveEntry(db.Model):
    __tablename__ = "archive_entry"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=False)
    archive_type = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # archives have one and only one service (YT, odysee, harddrive)
    service = db.Column(
        db.String(200), nullable=True
    )  

    def __repr__(self):
        return "<Archive %r>" % self.id

# #
@dataclass
class TrackPlaylistLink(db.Model):
    __tablename__ = "track_playlist_link"
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('track_entry.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))

    def __repr__(self):
        return "<Link %r>" % self.id

# #
@dataclass
class TrackArchiveLink(db.Model):
    __tablename__ = "track_archive_link"
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('track_entry.id'))
    archive_id = db.Column(db.Integer, db.ForeignKey('archive_entry.id'))

    def __repr__(self):
        return "<Link %r>" % self.id