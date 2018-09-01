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
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

#save tables as variables
Measurement = Base.classes.measurements
Station = Base.classes.stations

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
	#results.___dict___
	#Create a dictionary using 'date' as the key and 'prcp' as the value.
	"""year_prcp = []
	for result in results:
		row = {}
		row[Measurements.date] = row[Measurements.prcp]
		year_prcp.append(row)"""

	return jsonify(year_prcp)


@app.route("/api/v1.0/stations")
def stations():
	#return a json list of stations from the dataset.
	results = session.query(Stations.station).all()

	all_stations = list(np.ravel(results))

	return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
	#Return a json list of Temperature Observations (tobs) for the previous year
	year_tobs = []
	results = session.query(Measurements.tobs).filter(Measurements.date >= "2016-08-23").all()

	year_tobs = list(np.ravel(results))

	return jsonify(year_tobs)

@app.route("/api/v1.0/<start>")
def start_trip_temp(start_date):
	start_trip = []

	results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date == start_date).all()
	results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date == start_date).all()
	results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == start_date).all()

	start_trip = list(np.ravel(results_min,results_max, results_avg))

	return jsonify(start_trip)

def greater_start_date(start_date):

	start_trip_date_temps = []

	results_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).all()
	results_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date).all()
	results_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).all()

	start_trip_date_temps = list(np.ravel(results_min,results_max, results_avg))

	return jsonify(start_trip_date_temps)

@app.route("/api/v1.0/<start>/<end>")

def start_end_trip(start_date, end_date):

	start_end_trip_temps = []

	results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()
	results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()
	results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()

	start_end_trip_temps = list(np.ravel(results_min,results_max, results_avg))

	return jsonify(start_end_trip_temps)

def start_end_trip(start_date, end_date):

	round_trip_temps = []

	results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
	results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
	results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()

	round_trip_temps = list(np.ravel(results_min,results_max, results_avg))

	return jsonify(round_trip_temps)


if __name__ == '__main__':
    app.run(debug=True)