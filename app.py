from flask import Flask, jsonify
import date as dt 
import numpy as np  
import pandas as pd 
import sqlalchemy  
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    return(
        "Welcome to Hawaii Climate Analysis API!<br/>"
        "available routes:<br/>"
        "<a href='/api/v1.0/precipitation'>Precipitation<a/>"
        "<a href='/api/v1.0/stations'>Stations<a/>"
        "<a href='/api/v1.0/tobs'>Tobs<a/>"
        "<a href='/api/v1.0/<start>/<end>'>Start_End<a/>"
    )

    # Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    return()
    
# Define what to do when a user hits the index route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

# Define what to do when a user hits the index route
@app.route("/api/v1.0/tobs")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

# Define what to do when a user hits the index route
@app.route("/api/v1.0/<start>/<end>")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"




if __name__ == "__main__":
    app.run(debug=True)