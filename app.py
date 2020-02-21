# Import modules
from flask import Flask, jsonify
import datetime as dt 
import numpy as np  
import pandas as pd 
import sqlalchemy  
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Setup SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect database into a new model
Base = automap_base()

# Reflect tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station



# Create a Flask app
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    """List all available api routes."""
    return(
        "Welcome to Hawaii Climate Analysis API!<br/>"
        "Available routes:<br/>"
        "<a href='/api/v1.0/precipitation'>Precipitation<a/><br/>"
        "<a href='/api/v1.0/stations'>Stations<a/><br/>"
        "<a href='/api/v1.0/tobs'>Tobs<a/><br/>"
        "<a href='/api/v1.0/<start>/<end>'>Stats<a/>"
    )

# Define what to do when a user hits the 'Precipiation' route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return dictionary using date as the key and prcp as the value."""
   
    # Create our session (link) from Python to the database
    session = Session(engine)

    # Query all prcp and dates
    results = session.query(Measurement.prcp, Measurement.date).all()

    # Close out our link
    session.close()

    # Create an empty dictionary to hold our prcp and date data
    prcp_dict = {}
    
    # Define query results as we want in the dictionary
    for prcp, date in results:
        # Want date as key and prcp as value
        prcp_dict[date] = prcp
    
    # Return results in json format
    return jsonify(prcp_dict)
    
    
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
    sel = [Measurement.date, Measurement.tobs]
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
@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date = None, end_date = None):

    # sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # if not end_date:
    #     results = session.query(*sel).filter(Measurement.date >= start_date).all()
    #     temps = list(np.ravel(results))
    #     return jsonify(temps)

    # results = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    # temps = list(np.ravel(results))
    # return jsonify(temps)
    return "Hello World!!!"


    # session = Session(engine)
    # stats = session.query(func.min(Measurement.tobs),\
    #                          func.avg(Measurement.tobs),\
    #                          func.max(Measurement.tobs)).\
    #             filter(Measurement.date >= start_date).\
    #             filter(Measurement.date <= end_date).all()            
    # session.close()
    # return jsonify(stats)
    




if __name__ == "__main__":
    app.run(debug=True)