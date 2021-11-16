from flask import Flask
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
db.create_all()

# class representing the track #
class TrackEntry(db.Model):

    __tablename__ = "track_entry"
    id = db.Column(db.Integer, primary_key=True)
    relative_path = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Track %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    # return render_template("../webfiles/index.html")

    if request.method == "POST":
        track_content = request.form["content"]
        new_track = TrackEntry(relative_path=track_content)

        try:
            db.session.add(new_track)
            db.session.commit()
            return redirect("/")
        except:
            return "there was an issue adding the track"

    else:
        # tasks = TrackEntry.query.order_by(TrackEntry.id).all()
        tracks = TrackEntry.query.all()
        return render_template("index.html", tracks=tracks)
        # return render_template("index.html")


@app.route("/delete/<int:id>")
def delete(id):
    track_to_delete = TrackEntry.query.get_or_404(id)

    try:
        db.session.delete(track_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "there was an issue with delete operation "


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):

    track = TrackEntry.query.get_or_404(id)

    if request.method == "POST":
        track.relative_path = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "there was an issue updating the track information"

    else:
        return render_template("update.html", track=track)


# the basic command to being the flask server #
def run_flask_server(recreate=True):

    # create a dummy entry #

    app.run(debug=True)