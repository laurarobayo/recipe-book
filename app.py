from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["recipedb"]
recipes = db["recipes"]


@app.route("/")
def index():
    all_recipes = list(recipes.find())
    return render_template("index.html", recipes=all_recipes)


@app.route("/recipe/<recipe_id>")
def view_recipe(recipe_id):
    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=recipe)


@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        name = request.form.get("name")
        instructions = request.form.get("instructions")

        items = request.form.getlist("ingredient_item")
        amounts = request.form.getlist("ingredient_amount")
        ingredients = [
            {"item": item, "amount": amount}
            for item, amount in zip(items, amounts)
            if item.strip()
        ]

        recipes.insert_one({
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions
        })
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    recipes.delete_one({"_id": ObjectId(recipe_id)})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
