# dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create and instance of flask
app = Flask(__name__)

# establish connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# render index.html
@app.route("/")
def index():
    mars_one = mongo.db.collection.find_one()
    return render_template("index.html", mars = mars_one)

@app.route("/scrape")
def scraper():
    #mars_dict = mongo.db.mars_one 
    mars_dict = scrape_mars.scrape()
    mars.update({}, mars_dict, upsert=True)
    
    #redirect to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
