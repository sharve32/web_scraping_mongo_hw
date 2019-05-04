#Create route
import sys
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

sys.setrecursionlimit(2000)
app = Flask(__name__)
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data

#Create route that will query Mongo database and pass the mars data into an HTML template to display data

@app.route('/scrape')
def scrape():
    mars = scrape_mars.scrape()
    db.mars_data.insert_one(mars)

    return "Some scrapped data"

@app.route('/')
def home():
    mars = list(db.mars_data.find())
    return render_template("index.html", mars=mars)

if __name__ == "__main__":
    app.run(debug=True)