import requests
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, after_this_request, make_response
from helpers import error

app = Flask(__name__)

# Development, after - False
app.config["TEMPLATES_AUTO_RELOAD"] = True

api_key = os.environ['API_KEY']

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

api_query_url = "https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}".format(api_key = api_key)

# export API_KEY="1de24e617ade4a9c8cea38ee0d75b3c8"

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
        return render_template("search.html", active1="active")


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
        return render_template("result.html", ids=ids, titles=titles, descriptions=descriptions, images=images)

    return render_template("result.html", ids=ids, titles=titles, descriptions=descriptions, images=images)


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
        return render_template("recipe.html", recipe_title=recipe_title, recipe_summary=recipe_summary, recipe_image=recipe_image)
    
    return render_template("recipe.html", recipe_title=recipe_title, recipe_summary=recipe_summary, recipe_image=recipe_image)


@app.route('/recommendation')
def recommendation():
    return render_template("recommendation.html", active2="active")


@app.route('/plans')
def plans():
    return render_template("plans.html", active3="active")


@app.route('/history')
def history():
    return render_template("history.html", active4="active")

if __name__ == '__main__':
    app.run()