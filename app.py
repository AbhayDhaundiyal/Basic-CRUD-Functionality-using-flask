import flask
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from flask import render_template, request
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    name = db.Column(db.String(10))
    username = db.Column(db.String(20), unique = True, primary_key = True)
    password = db.Column(db.String(20), unique = True, nullable = False)
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
db.create_all()
@app.route("/<n>")
def home(n):
    return f"Hello, {escape(n)}!"


@app.route("/<n>/<b>")
def full(n, b):
    return f"Hello, {escape(n)} {escape(b)}!"


@app.route("/info")
def info():
    return render_template("/index/index.html")


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        n_data = json.loads(request.data)
        new_user = User(n_data["name"], n_data["username"], n_data["password"])
        db.session.add(new_user)
        db.session.commit()
        return f"{escape(new_user.name)} created sucessfully!"

@app.route("/delete", methods = ["GET", "POST"])
def delete():
    if request.method == "POST":
        n_data = json.loads(request.data)
        delx = User.query.filter_by(username=n_data["username"]).first()
        print(delx)
        if delx is None:
            return "Incorrect Username"
        if delx.password != n_data["password"]:
            return "Password is Incorrect"
        db.session.delete(delx)
        db.session.commit()
        return f"{escape(n_data['username'])} deleted sucessfully"


@app.route("/update", methods = ["GET", "POST"])
def update():
    if request.method == "POST":
        n_data = json.loads(request.data)
        delx = User.query.filter_by(username=n_data["username"]).first()
        print(delx)
        if delx is None:
            return "Username not found"
        if delx.password != n_data["password"]:
            return "Password is Incorrect"
        delx.password = n_data["newpass"]
        db.session.commit()
        return f"{escape(n_data['username'])}'s password updated sucessfully"

@app.route("/get_info", methods = ["GET", "POST"])
def read():
    if request.method == "POST":
        n_data = json.loads(request.data)
        delx = User.query.filter_by(username=n_data["username"]).first()
        print(delx)
        if delx is None:
            return "Username not found"
        if delx.password != n_data["password"]:
            return "Password is Incorrect"
        return f"Name : {escape(delx.name)}\n Username : {escape(delx.username)}\n Password : {escape(delx.password)}\n"
@app.route("/post", methods = ["POST"])
def pose():
	n_data = json.loads(request.data)
	print(n_data['Name'])
	return "Sucess!"
db.session.commit()
if __name__=='__main__': 
    app.run()
