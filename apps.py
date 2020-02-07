
from flask import Flask, render_template, redirect
import pymongo
import scrape

##Mongo Connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
dbName = "MarsDB"

if dbName in client.list_database_names():
    print("Mars DB Exists")
    db = client[dbName]
    print("Mars DB Connected")
else:
    print("Mars DB not existing -> New Created")
    db = client[dbName]
        

####Call Scrapping Function
##scrape.Mars_scrape(db)
#### Scrapping completed


app = Flask(__name__)

# Set route
@app.route("/")
def index():
    scrape.Mars_scrape(db)
    Articles = list(db.Mars_Articles.find())
    DayImage = list(db.Mars_Image.find())
    Weather = list(db.Mars_Weather.find())
    Hemi = list(db.Mars_Hemispheres.find())
    Data = list(db.Mars_Data.find())
    return render_template("index.html", Articles=Articles , DayImage=DayImage, Weather=Weather, Data=Data, Hemi=Hemi)


if __name__ == "__main__":
    app.run(debug=True)

    