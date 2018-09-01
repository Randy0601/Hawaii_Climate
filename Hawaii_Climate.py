
import matplotlib.pyplot as plt
import seaborn

import numpy as np
import pandas as pd

import datetime as dt

# Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

measurement = session.query(Measurement).first()
measurement.__dict__


station = session.query(Station).first()
station.__dict__

# Exploratory Climate Analysis

# Design a query to retrieve the last 12 months from 08-23-2017 of precipitation data.
precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
       group_by(Measurement.date).all()
precipitation

# Save the query results as a Pandas DataFrame and set the index to the date column
df = pd.DataFrame(precipitation)
df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d')
prcp_df = df.set_index("date")
prcp_df.head()


# Use Pandas Plotting with Matplotlib to plot the data
prcp_df.plot(figsize = (10,6), rot = 45)
plt.title("12 Months Precipitation")
plt.ylim(0,7)
plt.savefig("Images/12 Months Precipitation")
plt.show()




# Use Pandas to calcualte the summary statistics for the precipitation data
prcp_df.describe()

# How many stations are available in this dataset?
station_count = session.query(Station.station).count()
station_count

# List the stations and the counts in descending order.
active_station = session.query(Station.station, Station.name, Measurement.station, func.count(Measurement.tobs)).filter(Station.station == Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()
active_station

# What are the most active stations?
most_active = active_station[0][0:2]
most_active

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
activity = session.query(Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == most_active[0]).order_by(Measurement.station).all()
activity

# Choose the station with the highest number of temperature observations.
max_temp = session.query(Measurement.station, Measurement.tobs).filter(Measurement.station == most_active[0], Measurement.date >= "2016-08-23").all()
len(max_temp)

# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
temps = [x[1] for x in max_temp]
plt.hist(temps, bins=12)
plt.xlabel("Temperature (F)")
plt.ylabel("Frequency")
plt.title("Temperature Frequency")
plt.savefig("Images/Temperature Frequency")
plt.show()

# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
print(calc_temps('2016-08-23', '2017-08-23'))

# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
temp_values = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()
temp_values_list = [x for (x,) in temp_values]
avg_temp = np.mean(temp_values_list)
max_temp = max(temp_values_list)
min_temp = min(temp_values_list)

print(min_temp,avg_temp, max_temp)

# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)
plt.figure(figsize=(2,5))
plt.title("Trip Average Temp")
plt.ylabel("Temperature (F)")
plt.bar(1, avg_temp, yerr = (max_temp - min_temp), tick_label = "")
plt.savefig("Images/Trip Average Temp")
plt.show()
