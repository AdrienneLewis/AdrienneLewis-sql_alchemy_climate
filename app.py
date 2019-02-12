 #1. import Flask
from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
session = Session(engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

#Routes
@app.route("/")
def Welcome():
    """List Available Routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>")


@app.route("/api/v1.0/precipitation")
def prcp():
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    all_prcp =[]
    for date in results:
        prcp_dict = {}
        prcp_dict["date"] = date.date
        prcp_dict["prcp"] = date.prcp
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station():

    station= session.query(Measurement.station).\
        group_by(Measurement.station).all()

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-23').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= '2017-08-23').all() 
    return jsonify(tobs)

@app.route("/api/v1.0/<start_date>")
def calc_temps1(start_date):
    calc_temps1 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    return jsonify(calc_temps1)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps2(start_date, end_date):
    calc_temps2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    return jsonify(calc_temps2)
    

if __name__ == "__main__":
    app.run(debug=True)

