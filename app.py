###dependencies
from flask import Flask, jsonify

import datetime as dt
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

#save tables as variables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

##### Set up Flask
app = Flask(__name__)

#home route
@app.route("/")
def home():
    return ("Hawaii Weather Data API<br/>"
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/yyyy-mm-dd/<br/>"
    "/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/")

@app.route("/api/v1.0/precipitation")
def precipitation():
	#Query for the dates and temperature observations from the last year.
	results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()

	year_prcp = list(np.ravel(results))

	return jsonify(year_prcp)


@app.route("/api/v1.0/stations")
def stations():
	#return a json list of stations from the dataset.
	results = session.query(Station.station, Station.name, Station.latitude, Station.longitude).all()

	all_stations = list(np.ravel(results))

	return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
	#Return a json list of Temperature Observations (tobs) for the previous year
	year_tobs = []
	results = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()

	year_tobs = list(np.ravel(results))

	return jsonify(year_tobs)


@app.route("/api/v1.0/<start_date>/")
def temp_stats(start_date):
    #query using start date
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).first()
    #create dictionary from result
    temps_dictionary1 = {"minimum temperuture": temps[0], "maximum temperature": temps[1], "average temperature": temps[2]}
    return jsonify(temps_dictionary1)



@app.route("/api/v1.0/<start_date>/<end_date>/")
def temp_range(start_date, end_date):
    #query
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).first()
    #create dictionary from result
    temps_dictionary1 = {"TMIN": temps[0], "TMAX": temps[1], "TAVG": temps[2]}
    return jsonify(temps_dictionary1)


if __name__ == '__main__':
    app.run(debug=True)