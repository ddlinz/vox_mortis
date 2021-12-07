from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from vox.data_entry import db
from vox.data_entry import TrackEntry, PlayListEntry
from flask import Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room
from vox.session import BasicVoxSession

# from multiprocessing import Value
from multiprocessing import Process
from threading import Lock  # I would rather not use threads

# the basic global objects that the application uses #
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vox.db"
async_mode = None
socketio = SocketIO(async_mode=async_mode)
reporting = Blueprint("reporting", __name__)
central_session = BasicVoxSession()

# we are using threads for now, I guess #
thread = None
thread_lock = Lock()

# #
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        socketio.emit("my_response", {"data": "Server generated event", "count": count})


# #
def librarian_process():
    print("run librarian process")
    while 1:
        count = central_session.run_librarian_process()
        socketio.emit("my_response", {"data": "Server generated event", "count": count})
        print("doing random stuff")
        socketio.sleep(20)


# #
def create_background_process():
    bg_process = Process(target=librarian_process)
    return bg_process


# #
def run_app_as_process(app):
    fg_process = Process(target=app.run)
    return fg_process


# #
def create_flask_app(debug=False):

    # start the initial flask application #

    app.debug = debug
    app.register_blueprint(reporting)
    # app.config["SECRET_KEY"] = "secret!"
    # initiate the flask-socket-io application #

    central_session.initialize_database_archive(app)
    socketio.init_app(app)
    socketio.run(app)


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(librarian_process)
    emit("my_response", {"data": "Connected", "count": 0})


@socketio.event
def my_room_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": message["data"], "count": session["receive_count"]},
        to=message["room"],
    )


@socketio.event
def my_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit("my_response", {"data": message["data"], "count": session["receive_count"]})

    return redirect("/")


@socketio.event
def my_playlist_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit("my_response", {"data": message["data"], "count": session["receive_count"]})
    playlist_content = message["data"]
    # create a new playlist based on the entry #
    new_playlist = PlayListEntry(origin_uri=playlist_content)
    try:
        db.session.add(new_playlist)
        db.session.commit()
    except SystemExit:
        return "there was an issue adding the playlist"
    destination = "/index.html"
    emit("my_response", {"url": destination})


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


@reporting.route("/delete_track/<int:id>")
def delete_track(id):
    track_to_delete = TrackEntry.query.get_or_404(id)

    try:
        db.session.delete(track_to_delete)
        db.session.commit()
        return redirect("/")
    except SystemExit:
        return "there was an issue with delete track operation "


@reporting.route("/delete_playlist/<int:id>")
def delete_playlist(id):
    playlist_to_delete = PlayListEntry.query.get_or_404(id)

    try:
        db.session.delete(playlist_to_delete)
        db.session.commit()
        return redirect("/")
    except SystemExit:
        return "there was an issue with delete playlist operation "


@reporting.route("/delete/<int:id>")
def delete_general(id):
    return redirect("/")


# #
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
