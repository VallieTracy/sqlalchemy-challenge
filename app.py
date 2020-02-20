from flask import Flask, jsonify
import datetime as dt 
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
        "<a href='/api/v1.0/precipitation'>Precipitation<a/><br/>"
        "<a href='/api/v1.0/stations'>Stations<a/><br/>"
        "<a href='/api/v1.0/tobs'>Tobs<a/><br/>"
        "<a href='/api/v1.0/<start>/<end>'>Start_End<a/>"
    )

    # Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.prcp, Measurement.date).all()

    session.close()

    prcp_list = []
    for prcp, date in results:
        prcp_dict = {}
        prcp_dict["prcp"] = prcp
        prcp_dict["date"] = date
        prcp_list.append(prcp_dict)        

    return jsonify(prcp_list)
    
# Define what to do when a user hits the index route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

# Define what to do when a user hits the index route
@app.route("/api/v1.0/tobs")
def tobs():
    return "What do I want tobs to return?"

# Define what to do when a user hits the index route
@app.route("/api/v1.0/<start>/<end>")
def hmmm():
    return "And this one doesn't work"




if __name__ == "__main__":
    app.run(debug=True)