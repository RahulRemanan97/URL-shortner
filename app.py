from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id = db.Column("id_",db.Integer, primary_key = True)
    long = db.Column("long",db.String())
    short = db.Column("short",db.String(4))

    def __init__(self,long,short):
        self.long = long
        self.short = short

@app.before_request
def create_table():
    db.create_all()

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        random_letters = random.choices(letters, k=4)
        random_letters = "".join(random_letters)
        short_url = Urls.query.filter_by(short=random_letters).first()
        if not short_url:
            return random_letters

@app.route('/', methods=["POST","GET"])
def main():
    if request.method == "POST":
        url_entered = request.form["nm"]
        # check if url already exists in db
        found_url = Urls.query.filter_by(long=url_entered).first()
        if found_url:
            # return its shorten url
            return redirect(url_for("display_short_url",url=found_url.short))
        else:
            # create a short url
            short_url = shorten_url()
            new_url = Urls(url_entered, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url",url=short_url))

    else:
        return render_template("main.html")
    
@app.route("/display/<url>")
def display_short_url(url):
    return render_template("short.html",short_url=url)

@app.route("/<short_url>")
def redirection(short_url):
    url = Urls.query.filter_by(short=short_url).first()
    if url:
        return redirect(url.long)
    else:
        return f"<h2>Url doesnt exist</h2>"



if __name__ == '__main__':
    app.run(port=5000, debug=True)