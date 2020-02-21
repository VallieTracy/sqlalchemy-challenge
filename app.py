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
        "Available routes:<br/>"
        "<a href='/api/v1.0/precipitation'>Precipitation<a/><br/>"
        "<a href='/api/v1.0/stations'>Stations<a/><br/>"
        "<a href='/api/v1.0/tobs'>Tobs<a/><br/>"
        "<a href='/api/v1.0/<start>/<end>'>Stats<a/>"
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
        prcp_dict["Precipitation"] = prcp
        prcp_dict["Date"] = date
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
    session = Session(engine)
    sel = [Measurement.station, Measurement.date, Measurement.tobs]
    tobs_data = session.query(*sel).\
        filter(Measurement.date >= '2016-08-24').all()
    session.close()
    return jsonify(tobs_data)

    # Lines 71-76 retunrs one giant list of dates and tobs
    #session = Session(engine)
    #results = session.query(Measurement.date, Measurement.tobs).\
       #filter(Measurement.date >= '2016-08-24').all()
    #session.close()
    #tobs_data = list(np.ravel(results))
    #return jsonify(tobs_data)

# Define what to do when a user hits the index route
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start_date, end_date):
    session = Session(engine)
    stats = session.query(func.min(Measurement.tobs),\
                             func.avg(Measurement.tobs),\
                             func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).\
                filter(Measurement.date <= end_date).all()            
    session.close()
    return jsonify(stats)
    




if __name__ == "__main__":
    app.run(debug=True)