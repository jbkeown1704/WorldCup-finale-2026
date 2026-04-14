from flask import Blueprint, jsonify, request
from app.models.match import Match

matches_bp = Blueprint('matches', __name__)

# ============================================================
#  Matches Routes — YOUR TASK #2
#
#  Implement the REST endpoints for matches.
# ============================================================


# ============================================================
#  GET /api/matches — Return matches with optional filters
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #2)
#
# Query parameters (both optional):
#   ?city=city-atlanta    → filter by city ID
#   ?date=2026-06-14      → filter by date (YYYY-MM-DD)
#
# Hint: Use request.args.get() to extract optional query parameters.
# Use Match.query with filter_by() or filter() to apply filters.
# Order results by kickoff and convert to dicts using match.to_dict()
#
# ============================================================

@matches_bp.route('', methods=['GET'])
def get_matches():
    # TODO: Replace with your implementation (YOUR TASK #2)

    #Starting with grabbing all of the matches from the database
    query = Match.query

    #Get the optional filters for the URLS parameters
    city_id = request.args.get('city')
    date = request.args.get('date')

    #Apply city filter when/if it is provided
    if city_id:
        query = query.filter_by(city_id=city_id)

    #Apply date filter if provided (matches date part only, ignores time)
    if date:
        query = query.filter(Match.kickoff.like(f'{date}%'))

    #Order by kickoff date
    query = query.order_by(Match.kickoff)

    #Get all matches
    matches = query.all()

    #Convert to list of dictionaries and return as JSON
    return jsonify([match.to_dict() for match in matches])


# ============================================================
#  GET /api/matches/<id> — Return a single match by ID
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #2)
#
# Hint: Use Match.query.get(id) — returns None if not found.
# Return 404 with an error message if not found.
#
# ============================================================

@matches_bp.route('/<id>', methods=['GET'])
def get_match_by_id(id):
    # TODO: Replace with your implementation (YOUR TASK #2)

    #Match the match using the ID 
    match = Match.query.get(id)

    # If not found, return 404 error
    if not match:
        return jsonify({"error": f"Match with id '{id}' not found"}), 404


    # Return the match as JSON
    return jsonify(match.to_dict())
