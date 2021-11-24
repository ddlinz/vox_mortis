from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from vox.data_entry import db
from vox.data_entry import TrackEntry, PlayListEntry, TagEntry
from flask import Blueprint
from vox.create_app import socketio

reporting = Blueprint("reporting", __name__)


@reporting.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":

        name_input = request.form["sub_type"]

        if name_input == "Add Playlist":
            playlist_content = request.form["content"]
            new_playlist = PlayListEntry(origin_uri=playlist_content)

            try:
                db.session.add(new_playlist)
                db.session.commit()
            except SystemExit:
                return "there was an issue adding the playlist"

        elif name_input == "Add Track":
            track_content = request.form["content"]
            new_track = TrackEntry(relative_path=track_content)

            try:
                db.session.add(new_track)
                db.session.commit()
            except SystemExit:
                return "there was an issue adding the track"
        else:
            return "there was an issue adding the object."

        return redirect("/")

    else:
        # tasks = TrackEntry.query.order_by(TrackEntry.id).all()
        tracks = TrackEntry.query.all()
        playlists = PlayListEntry.query.all()
        return render_template("index.html", tracks=tracks, playlists=playlists)


@reporting.route("/delete/<int:id>")
def delete(id):
    track_to_delete = TrackEntry.query.get_or_404(id)

    try:
        db.session.delete(track_to_delete)
        db.session.commit()
        return redirect("/")
    except SystemExit:
        return "there was an issue with delete operation "


@reporting.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):

    track = TrackEntry.query.get_or_404(id)

    if request.method == "POST":
        track.relative_path = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except SystemExit:
            return "there was an issue updating the track information"

    else:
        return render_template("update.html", track=track)


@reporting.route("/playlist/<int:id>", methods=["GET"])
def getPlaylistContents(id):

    if request.method == "GET":
        return render_template("update.html", track=1)


@socketio.on("update")
def update(data):
    print("Current Value", data["value"])

