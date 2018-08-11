import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct
from sqlalchemy import desc

import datetime as dt
from datetime import date

from flask import Flask, jsonify


# from flask import jsonify

#Database setup
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Query for the dates and temperature observations from the last year
    #Convert the query results to a Dictionary using 'date' as the key and 'tobs' as the value
    #Return the JSON representation of your dictionary

    start_date= date(2017,8,23)
    year_ago= start_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    all_precip = []
    for precips in results:
        precip_dict={}
        precip_dict["date"]=precips.date
        precip_dict["prcp"]=precips.prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results1 = session.query(distinct(Measurement.station)).all()
    station = list(np.ravel(results1))
    return jsonify(station)

#Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    start_date= date(2017,8,23)
    year_ago= start_date - dt.timedelta(days=365)
    results2 = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_ago).\
        group_by(Measurement.date).all()
    tobs = list(np.ravel(results2))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
   sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
   
   if not end:
       results = session.query(*sel).filter(Measurement.date >= start).all()
       temps = list(np.ravel(results))
       return jsonify(temps)
   
   results = session.query(*sel).filter(Measurement.date >=start).filter(Measurement.date <= end).all()
   temps = list(np.ravel(results))
   return jsonify(temps)
   
if __name__ == '__main__':
    app.run(debug=True)