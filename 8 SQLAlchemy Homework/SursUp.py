import numpy as np
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

########################
# Database Setup
########################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
#reflect the tables 
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations

#######################
# Flask Setup
#######################
app = Flask(__name__)

#######################
#Flask Routes
#######################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        #Create our session (link) from Python to the DB
        session = Session(engine)

        """Return a list of search queries"""
        results = session.query(Measurements.date, Measurements.prcp).all()

        session.close()

        #Convert list of tuples into normal list
        all_dates= list(np.ravel(results))

        return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def stations(): 
        #Create a session (link) from Python to the DB
        session = Session(engine)

        """Return a list of Stations"""
        station_query= session.query(Stations.station).all()

        session.close()

        #all_stations= list(np.ravel(station_query))

        #return jsonify(all_stations)

        #Create a dictionary from the row table and append to list
        stations_all = []
        for station in station_query:
            station_dict = {}
            station_dict["station"] = station
            stations_all.append(station_dict)
        return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():
        #Create a session 
        session = Session(engine)

        #Return a temp and dates results 
        temp_dates = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date.between('2016-08-23', '2017-08-23')).all()

        session.close() 

        #Convert list of tuples into normal list
        all_tempdates= list(np.ravel(temp_dates))

        return jsonify(all_tempdates)

@app.route("/api/v1.0/<start>/<end>")
def startstop(start_date, end_date): 

        #create a session 
        session = Session(engine)

        #Return the needed variables in search query
        startend = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
                   filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
        
        session.close()

        #create a dictionary of the results 
        startend_all = []
        for start_date in startend:
            startend_dict = {}
            startend_dict["Start Date"] = start_date
            startend_dict["End Date"] = end_date
            startend_dict["Min Temp"] = startend[0]
            startend_dict["Avg Temp"] = startend[1]
            startend_dict["Max Temp"] = startend[2]
            startend_all.append(startend_dict)
        return jsonify(startend_all)


if __name__ == '__main__':
    app.run(debug=True)
