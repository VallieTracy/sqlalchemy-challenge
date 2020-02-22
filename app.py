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

session = Session(engine)



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
        "<a href='/api/v1.0/<start>/<end>'>calc_temps<a/>"
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
    
    
# 'Stations' route
@app.route("/api/v1.0/stations")
def stations():
    """Retunrs JSON list of all stations"""
    
    # Create session from Python to DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()
    
    #close session
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    
    #return results as JSON
    return jsonify(all_stations)

# Define what to do when a user hits 'Tobs' route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the data's most recent 12 months,
    looking at the most active Station, USC00519281"""
    
    # Create session between Python and DB
    session = Session(engine)

    # Create start_date variable in order to filter the data
    start_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    
    # Query, filtering by start_date and station
    sel = [Measurement.date, Measurement.tobs]
    tobs_data = session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519281').all()
    
    # Close session
    session.close()

    # Return jsonified data to user
    return jsonify(tobs_data)

# Define 'calc_temps' route
@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date = None, end_date = None):
    
    
    
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end_date:
        
        results = session.query(*sel).filter(Measurement.date >= start_date).all()
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)

    results = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    temps = list(np.ravel(results))

    # Close session
    session.close()

    return jsonify(temps)
    
   



    




if __name__ == "__main__":
    app.run(debug=True)