import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#or can use .format instead of placeholder values in dynamic insertion
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name_added = request.form["name"]
        month_added = request.form["month"]
        day_added = request.form["day"]
        db.execute("""
        INSERT INTO birthdays (name, month, day)
        VALUES (?, ?, ?)""",
        name_added, month_added, day_added)

        return redirect("/")

    else:
        data_all = db.execute("SELECT name,month,day FROM birthdays")
        for data in data_all:
            birthday = f"{data['month']}/{data['day']}"
            data["birthday"] = birthday
        return render_template("index.html", data_all=data_all)