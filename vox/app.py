from flask import Flask
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


# class representing the track #
class TrackEntry(db.Model):

    __tablename__ = "track_entry"

    id = db.Column(db.Integer, primary_key=True)
    relative_path = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self, id, relative_path, date_created):
    #     self.id = id
    #     self.relative_path = relative_path
    #     self.date_create = date_created

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
    task_to_delete = TrackEntry.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "there was an issue with delete operation "


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    
    track = TrackEntry.query.get_or_404(id)
    
    if request.method == "POST":
        track.content = request.form["content"]
        
        try: 
            db.session.commit()
            return redirect('/')
        
        except:
            return 'there was an issue updating the track information'
        
    else:
        return render_template("update.html")


# the basic command to being the flask server #
def run_flask_server(recreate=True):

    db.create_all()
    # create a dummy entry #
    first_entry = TrackEntry(relative_path="/")
    db.session.add(first_entry)
    db.session.commit()

    app.run(debug=True)
