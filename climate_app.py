
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"  
        f"/api/v1.0/precipitation<br/>"   
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Find the most recent date in the data set.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set.
    date_one_year_ago =  dt.datetime.strptime(recent_date, '%Y-%m-%d')  - dt.timedelta(365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_scores = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= date_one_year_ago).all()

    prcp_dict = dict(prcp_scores)

    session.close()

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations_list = session.query(Station.station).order_by(Station.station).all()

    # Convert list of tuples into normal list
    stations_ls = list(np.ravel(stations_list))

    session.close()

    return jsonify(stations_ls)


if __name__ == '__main__':
    app.run(debug=True)
