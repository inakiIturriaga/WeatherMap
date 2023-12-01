import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import requests

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///weathermap.db")

lctnlat = 0
lctnlon = 0

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/marker", methods=["POST"])
def marker():
    data = request.json
    lat = data["lat"]
    lng = data["lng"]
    global lctnlat
    lctnlat = lat
    global lctnlon
    lctnlon = lng
    api_key = "8c31d1438b7154e8534461d3558c25d0"
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}"
    )
    weather = response.json()
    temperature = weather["main"]["temp"]
    temperature_celsius = temperature - 273.15
    city = weather["name"]
    humidity = weather["main"]["humidity"]
    deg = weather["wind"]["deg"]
    speed = weather["wind"]["speed"] * 3.6
    return jsonify(
        temp=temperature_celsius,
        city=city,
        humidity=humidity,
        deg=deg,
        speed=speed,
    )


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")


@app.route("/places", methods=["GET", "POST"])
def places():
    if request.method == "GET":
        sav = db.execute("SELECT * FROM savedplaces WHERE user_id = ?", session["user_id"])
        print(sav)
        return render_template("places.html", sav=sav)
    if request.method == "POST":
        lat, lon = request.form.get('placebutton').split(',')
        session['lat'] = lat
        session['lon'] = lon
        pmarker()
        return redirect("/")

@app.route("/addplace", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        global lctnlat
        global lctnlon
        nickname = request.form["nickname"]
        db.execute("INSERT INTO savedplaces(user_id, nickname, latitude, longitude) VALUES(?, ?, ?, ?)", session["user_id"], nickname, lctnlat, lctnlon)
        return redirect("/")

@app.route("/pmarker", methods=["GET", "POST"])
def pmarker():
    lat = session['lat']
    lon = session['lon']
    print(lat, lon)
    return jsonify({"lat": lat, "lon": lon})

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        print("hello")

        if not request.form.get("username"):
            return render_template(
                "apology.html", message="Must provide username", code=403
            )

        elif not request.form.get("password"):
            return render_template(
                "apology.html", message="Must provide password", code=403
            )

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return render_template(
                "apology.html", message="Invalid user information", code=403
            )

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form["username"]

        if not name:
            return render_template(
                "apology.html", message="Must provide username", code=403
            )

        elif db.execute("SELECT * FROM users WHERE username = ?", name):
            return render_template("apology.html", message="Username in use", code=403)

        password = request.form["password"]
        if not password:
            return render_template(
                "apology.html", message="Must provide password", code=403
            )

        elif request.form["confirmation"] != password:
            return render_template(
                "apology.html", message="Passwords do not match", code=403
            )

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, password) VALUES(?, ?)", name, hash)
        return redirect("/")

    else:
        return render_template("register.html")
