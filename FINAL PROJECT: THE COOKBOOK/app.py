import requests
import os
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from cs50 import SQL
import random
import datetime
from helpers import error

#Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure flask_sqlalchemy library to use SQLite database
db = SQL("sqlite:///history.db")

#API KEY
""" export API_KEY=1de24e617ade4a9c8cea38ee0d75b3c """
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
search_history = []

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
            ids.clear(), titles.clear(), descriptions.clear(), images.clear(), search_history.clear()
            search_history.append(search)
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

            # Inserts recipes and search query to database
            value = session.get("user_id", None)
            if value == None: 
                return redirect('/recipe')
            else:
                username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]
                db.execute("INSERT INTO user_search (username, search_query, food_id, recipe_name, date) VALUES (?, ?, ?, ?, ?)", username, search_history[0], food_id, recipe_title[0], datetime.datetime.now())
                return redirect('/recipe')

        else: 
            return error("Try again later")

    if request.method == "GET":
        return render_template("recipe.html", recipe_title=recipe_title, recipe_summary=recipe_summary, recipe_image=recipe_image, session=session)
    
    return render_template("recipe.html", recipe_title=recipe_title, recipe_summary=recipe_summary, recipe_image=recipe_image, session=session)


recommendation_title = []
recommendation_time = []
recommendation_servings = []
recommendation_source = []
@app.route('/recommendation')
def recommendation():
    if request.method == "GET":
        recommendation_title.clear(), recommendation_time.clear(), recommendation_servings.clear(), recommendation_source.clear()
        value = session.get("user_id", None)
        if value == None:
            return render_template("recommendation.html", active2="active", session=session)
        
        else: 
            username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]
            possible_recommendation_id = db.execute("SELECT food_id FROM user_search WHERE username=?", username)
            # Returns list of dictionaries
            if len(possible_recommendation_id) >=  3:
                # Get random recommendation
                random_recommendation_id = random.choice(possible_recommendation_id) 
                random_recommendation_id = random_recommendation_id["food_id"]
                api_similar_recipe_url = "https://api.spoonacular.com/recipes/{id}/similar?apiKey={api_key}".format(id=random_recommendation_id, api_key=api_key)
                recommended_recipe = requests.get(api_similar_recipe_url, params={"number": 20}).json()
                for recipe in recommended_recipe:
                    if recommended_recipe.count(recipe["title"]) > 1:
                        recommended_recipe.remove(recipe["title"])
                recommended_recipe = random.sample(recommended_recipe, k=3)
                
                # Adding values returned to variables
                for recipe in recommended_recipe: 
                    recommendation_title.append(recipe["title"])
                    recommendation_time.append(recipe["readyInMinutes"])
                    recommendation_servings.append(recipe["servings"])
                    recommendation_source.append(recipe["sourceUrl"])   

            else:
                return error("Make at least 3 searches before you can use this feature!", code="We need to get to know you better")
        
        return render_template("recommendation.html", active2="active", session=session, recommendation_title=recommendation_title, recommendation_time=recommendation_time, recommendation_servings=recommendation_servings, recommendation_source=recommendation_source)
    
    return render_template("recommendation.html", active2="active", session=session, recommendation_title=recommendation_title, recommendation_time=recommendation_time, recommendation_servings=recommendation_servings, recommendation_source=recommendation_source)


@app.route('/history')
def history():
    if request.method == "GET":
        value = session.get("user_id", None)
        if value == None:
            return render_template("history.html", active4="active", session=session)
        
        else:
            username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]
            user_history = db.execute("SELECT DISTINCT recipe_name, search_query, date FROM user_search WHERE username=?", username)
            return render_template("history.html", active4="active", session=session, user_history=user_history)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    existing_users = db.execute("SELECT username FROM users")

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
    new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

    session["user_id"] = new_user
    return redirect("/")

    
@app.route('/login', methods=["GET", "POST"])
def login():
    
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username1"):
            return error("Must provide username")

        # Ensure password was submitted
        if not request.form.get("password1"):
            return error("Must provide password")

        # Query database for username
        row = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username1"))

        # Ensure username exists and password is correct
        if len(row) != 1 or not check_password_hash(row[0]["hash"], request.form.get("password1")):
            return error("Invalid username or password", 403)

        # Remember which user has logged in
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    if request.method == "GET":
        session.clear()
        return redirect("/")
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")