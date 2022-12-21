import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    transactions = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions where user_id= ? GROUP BY symbol", user_id)
    for stock in transactions:
        stock_total = stock["shares"] * stock["price"]
        stock_total = "${:.2f}".format(stock_total)
        stock["total"] = stock_total
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    cash = "{:.2f}".format(cash)
    return render_template("index.html", database=transactions, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")
    stock = lookup(symbol.upper())

    if not symbol:
        return apology("Input a Ticker!")

    if stock == None:
        return apology("Symbol Does Not Exist")

    if not shares.isdigit():
        return apology("Can Only Buy Whole Shares")

    shares = int(shares)

    if shares < 0:
        return apology("Can Only Input Positive Amount of Shares!")

    transaction = stock["price"] * shares
    user_id = session["user_id"]
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    if user_cash < transaction:
        return apology("Please Add More to Balance!")

    updated_cash = user_cash - transaction
    db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
    date = datetime.datetime.now()
    db.execute("INSERT INTO transactions(user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
               user_id, stock["symbol"], shares, stock["price"], date)

    flash("Bought")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    database = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", database=database)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    symbol = request.form.get("symbol")
    stock = lookup(symbol.upper())

    if not symbol:
        return apology("Input a Ticker!")
    if not stock:
        return apology("Symbol Does Not Exist")

    return render_template("quoted.html", name=stock["name"], price=usd(stock["price"]), symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Username
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]
    confirmation = request.form["confirmation"]
    existing_users = db.execute("SELECT username FROM users")

    if not username:
        return apology("Enter a Username!")

    if not password:
        return apology("Enter a Password!")

    if not confirmation:
        return apology("Please Confirm Your Password!")

    if password != confirmation:
        return apology("Passwords Do not Match!")

    hash = generate_password_hash(password)

    for existing_user in existing_users:
        if username == existing_user["username"]:
            return apology("Username Taken!")

    # All above works, and registering user
    new_user = db.execute("""INSERT INTO users (username, hash) VALUES (?, ?)""", username, hash)

    session["user_id"] = new_user
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        users_symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM (shares) > 0", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in users_symbols])

    symbol = request.form["symbol"]
    shares = int(request.form["shares"])
    stock = lookup(symbol)

    if shares < 0:
        return apology("Can Only Input Positive Amount of Shares!")

    user_id = session["user_id"]
    user_shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)[
        0]["shares"]

    if shares > user_shares:
        return apology(f"YOU DON'T HAVE ENOUGH SHARES!")

    transaction = stock["price"] * shares
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    updated_cash = user_cash + transaction
    db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
    date = datetime.datetime.now()

    db.execute("INSERT INTO transactions(user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
               user_id, stock["symbol"], (-1)*shares, stock["price"], date)

    flash("Sold")
    return redirect("/")