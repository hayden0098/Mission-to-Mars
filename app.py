from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scraping 

#set up flask
app = Flask(__name__)

#tell python to connect Mongo using PyMongo
#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set flask routes
@app.route("/")
def index():
    # PyMongo to find "mars" collection in DB
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

# set scraping route, this will be the "button" of web application
@app.route("/scrape")
def scrape():
    # variable that points to our Mongo database
    mars = mongo.db.mars
    # variable to hold the newly scraped data
    mars_data = scraping.scrape_all()
    # To update the database
    # Syntax: .update(query_parameter, data, options)
    mars.update({}, mars_data, upsert=True)  #indicates to create a new document if one doesn't already exist and save
    # navigate our page back to '/' page
    return redirect('/', code = 302) 

if __name__ == "__main__":
    app.run()