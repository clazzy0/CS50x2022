import requests
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, after_this_request, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from helpers import error

#Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
session["user_id"] = None

# Configure flask_sqlalchemy library to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
db = SQLAlchemy(app)

#API key 
""" export API_KEY="1de24e617ade4a9c8cea38ee0d75b3c8 """
api_key = os.environ['API_KEY']
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
api_query_url = "https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}".format(api_key = api_key)

#Development 
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    return redirect('/search')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        return render_template("search.html", active1="active", session=session)


ids = []
titles = []
descriptions = []
images = []

@app.route('/result', methods=["GET", "POST"])
def result():
    if request.method == "POST":
        search = request.form.get("search")

        if not search:
            return error("Must input into search bar!")
        
        query = {'query': search, 'number': 8}
        response = requests.get(api_query_url, params=query)
        
        if response.ok:
            response = response.json()
            i = 0
            ids.clear(), titles.clear(), descriptions.clear(), images.clear()
            for result in response["results"]:
                # food id
                ids.append(result['id'])

                # titles 
                i += 1
                titles.append(f"{search.title()} Recipe {i}")

                # descriptions 
                descriptions.append(result["title"])

                # images
                images.append(result["image"])

            if not ids:
                return error("That search does not exist!")
            
            return redirect('/result')

        else:
            return error("Try again later")

    if request.method == "GET":
        return render_template("result.html", ids=ids, titles=titles, descriptions=descriptions, images=images, session=session)

    return render_template("result.html", ids=ids, titles=titles, descriptions=descriptions, images=images, session=session)


recipe_title = []
recipe_summary = []
recipe_image = []

@app.route('/recipe', methods=["GET", "POST"])
def recipe():
    if request.method == "POST":
        food_id = request.form.get('get-recipe-button')
        api_recipe_url = "https://api.spoonacular.com/recipes/{id}/summary?apiKey={api_key}".format(id=food_id, api_key=api_key)
        recipe = requests.get(api_recipe_url)
        
        if recipe.ok: 
            recipe_title.clear(), recipe_summary.clear(), recipe_image.clear()
            recipe = recipe.json()
            recipe_title.append(recipe["title"])
            recipe_summary.append(recipe["summary"])
            image_index = ids.index(int(food_id))
            recipe_image.append(images[image_index])
            return redirect('/recipe')

        else: 
            return error("Try again later")

    if request.method == "GET":
        return render_template("recipe.html", recipe_title=recipe_title, recipe_summary=recipe_summary, recipe_image=recipe_image, session=session)
    
    return render_template("recipe.html", recipe_title=recipe_title, recipe_summary=recipe_summary, recipe_image=recipe_image, session=session)


@app.route('/recommendation')
def recommendation():
    if session.get("user_id") == None:
        return render_template("notloggedin.html")
    
    return render_template("recommendation.html", active2="active")


@app.route('/plans')
def plans():
    if session.get("user_id") == None:
        return render_template("notloggedin.html")
    
    return render_template("plans.html", active3="active")


@app.route('/history')
def history():
    if session.get("user_id") == None:
        return render_template("notloggedin.html")
    
    return render_template("history.html", active4="active")

@app.route('/register')
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    existing_users = db.execute(text("SELECT username FROM users"))

    if not username:
        return error("Enter a Username!")

    if not password:
        return error("Enter a Password!")

    if not confirmation:
        return error("Please Confirm Your Password!")

    if password != confirmation:
        return error("Passwords Do not Match!")
    
    hash = generate_password_hash(password)

    for existing_user in existing_users:
        if username == existing_user["username"]:
            return error("Username Taken!")
        
    # All above is valid, registering user...
    new_user = db.execute(text("INSERT INTO users (username, hash) VALUES (?, ?)"), username, hash)

    session["user_id"] = new_user.rowcount()
    return redirect("/")

    
@app.route('/login')
def login():
    
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Must provide password")

        # Query database for username
        rows = db.execute(text("SELECT * FROM users WHERE username = ?", request.form.get("username")))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route('/logout')
def logout():
    if request.method == "GET":
        session.clear()
        return render_template("/")
    
if __name__ == '__main__':
    app.run()
