from flask import Blueprint, jsonify
from app.models.city import City

cities_bp = Blueprint('cities', __name__)

# ============================================================
#  City Routes — YOUR TASK #1
#
#  Implement the REST endpoint for cities.
# ============================================================


# ============================================================
#  GET /api/cities — Return all host cities
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #1)
#
# This should return all 16 host cities as a JSON array.
#
# Hint: Use City.query.all() to get all cities from the database,
# then convert each to a dict using city.to_dict()
#
# Expected response: [{ id, name, country, latitude, longitude, stadium }, ...]
#
# ============================================================

@cities_bp.route('/')
def get_all():
    # TODO: Replace with your implementation (YOUR TASK #1)

    #The is the line query the database for the 16 cities in a json file
    cities = City.query.all()

    #This will convert each object of "City" and then convert them into a dictionary and return this as json file
    return jsonify([city.to_dict() for city in cities])