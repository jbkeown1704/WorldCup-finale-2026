from flask import Blueprint, jsonify, request
from app.models.match import Match
from app.models.flight_price import FlightPrice
from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy
# Tip: You can also import DateOnlyStrategy to compare results
# from app.strategies.date_only_strategy import DateOnlyStrategy

optimise_bp = Blueprint('optimise', __name__)

# ============================================================
#  Route Optimisation — YOUR TASK #3 and #5
#
#  Implement route optimisation and budget calculation endpoints.
# ============================================================


# ============================================================
#  POST /api/route/optimise — Optimise a travel route
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #3)
#
# Request body: { "matchIds": ["match-1", "match-5", "match-12", ...] }
#
# Steps:
#   1. Extract matchIds from the request JSON
#   2. Fetch full match data from the database
#   3. Convert matches to dicts (using match.to_dict())
#   4. Create a strategy instance: NearestNeighbourStrategy()
#      (or DateOnlyStrategy() to test with the working example first)
#   5. Call strategy.optimise(match_dicts)
#   6. Return the optimised route as JSON
#
# TIP: Start by using DateOnlyStrategy to verify your endpoint works,
# then switch to NearestNeighbourStrategy once you've implemented it.
#
# ============================================================

@optimise_bp.route('/optimise', methods=['POST'])
def optimise():
    #Debugging a 200 code 
    print("=== OPTIMISE ENDPOINT HIT ===")
    print(f"Request data: {request.get_json()}")

    # first we have to get the "matchIds" from the request
    data = request.get_json()
    match_ids = data.get('matchIds', [])

    #If the match id entered isnt available we add in this error handling
    if not match_ids:
        return jsonify({"error": "No matchIds provided"}), 400

    #Now we will fetch the matches from the database 
    matches = Match.query.filter(Match.id.in_(match_ids)).all()

    #Convert the database info into a dictionary for ease of searching
    match_dicts = [match.to_dict() for match in matches]

    #Use DateOnlyStrategy first (to test)
    from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy
    strategy = NearestNeighbourStrategy()
    
    #Optimise the route
    result = strategy.optimise(match_dicts)
    
    # Add country validation to the result
    countries_visited = set()
    for stop in result.get('stops', []):
        if 'city' in stop and 'country' in stop['city']:
            countries_visited.add(stop['city']['country'])
    
    result['countriesVisited'] = list(countries_visited)
    result['feasible'] = len(countries_visited) == 3 and len(result.get('stops', [])) >= 5
    
    missing = []
    required = {'USA', 'Mexico', 'Canada'}
    for country in required:
        if country not in countries_visited:
            missing.append(country)
    result['missingCountries'] = missing
    
    #Return as JSON
    return jsonify(result)


# ============================================================
#  POST /api/route/budget — Calculate trip costs and check budget
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #5)
#
# Request body:
# {
#   "budget": 5000.00,
#   "matchIds": ["match-1", "match-5", "match-12", ...],
#   "originCityId": "city-atlanta"
# }
#
# Steps:
#   1. Extract budget, matchIds, and originCityId from request JSON
#   2. Fetch matches by IDs from the database
#   3. Convert matches to dicts (using match.to_dict())
#   4. Fetch all flight prices from the database
#   5. Create a CostCalculator instance
#   6. Call calculator.calculate(match_dicts, budget, origin_city_id, flight_prices)
#   7. Return the BudgetResult as JSON
#
# IMPORTANT CONSTRAINTS:
#   - User MUST attend at least 1 match in each country (USA, Mexico, Canada)
#   - If the budget is insufficient, return feasible=False with:
#     - minimumBudgetRequired: the actual cost
#     - suggestions: ways to reduce cost
#   - If countries are missing, return feasible=False with:
#     - missingCountries: list of countries not covered
#
# ============================================================
@optimise_bp.route('/budget', methods=['POST'])
def budget_optimise():
    # Extract data from request
    data = request.get_json()
    budget = data.get('budget')
    match_ids = data.get('matchIds', [])
    origin_city_id = data.get('originCityId')
    
    # Validate required fields
    if budget is None:
        return jsonify({"error": "Missing required field: budget"}), 400
    if not match_ids:
        return jsonify({"error": "Missing required field: matchIds"}), 400
    if not origin_city_id:
        return jsonify({"error": "Missing required field: originCityId"}), 400
    
    # Fetch matches from database
    matches = Match.query.filter(Match.id.in_(match_ids)).all()
    
    if not matches:
        return jsonify({"error": "No valid matches found for the provided IDs"}), 404
    
    # Convert to dictionaries and sort by date
    match_dicts = [match.to_dict() for match in matches]
    match_dicts.sort(key=lambda m: m['kickoff'])

    # Fetch all flight prices
    flight_prices_db = FlightPrice.query.all()
    flight_prices = [
        {
            "from_city_id": fp.origin_city_id,      # Changed
            "to_city_id": fp.destination_city_id,   # Changed
            "price": fp.price_usd                    # Changed (if field is price_usd)
        }
        for fp in flight_prices_db
    ]
    
    # Create CostCalculator instance and calculate
    from app.utils.cost_calculator import CostCalculator
    calculator = CostCalculator()
    result = calculator.calculate(match_dicts, budget, origin_city_id, flight_prices)
    
    # Return result
    return jsonify(result)


# ============================================================
#  POST /api/route/best-value — Find best match combination within budget
# ============================================================
#
# TODO: Implement this endpoint (BONUS CHALLENGE #1)
#
# Request body:
# {
#   "budget": 5000.00,
#   "originCityId": "city-atlanta"
# }
#
# Steps:
#   1. Extract budget and originCityId from request JSON
#   2. Fetch all available matches from the database
#   3. Convert matches to dicts (using match.to_dict())
#   4. Fetch all flight prices from the database
#   5. Create a BestValueFinder instance
#   6. Call finder.find_best_value(match_dicts, budget, origin_city_id, flight_prices)
#   7. Return the BestValueResult as JSON
#
# Requirements:
#   - Find the maximum number of matches that fit within budget
#   - Must include at least 1 match in each country (USA, Mexico, Canada)
#   - Minimum 5 matches required
#   - Return optimised route with cost breakdown
#
# ============================================================
@optimise_bp.route('/best-value', methods=['POST'])
def best_value():
    try:
        data = request.get_json()
        budget = data.get('budget')
        origin_city_id = data.get('originCityId')
        
        print(f"Received budget: {budget}, origin: {origin_city_id}", flush=True)
        
        if budget is None:
            return jsonify({"error": "Missing required field: budget"}), 400
        if not origin_city_id:
            return jsonify({"error": "Missing required field: originCityId"}), 400
        
        # Fetch all matches
        all_matches_db = Match.query.all()
        all_matches = [match.to_dict() for match in all_matches_db]
        print(f"Fetched {len(all_matches)} matches", flush=True)
        
        # Fetch flight prices
        flight_prices_db = FlightPrice.query.all()
        flight_prices = [
            {"from_city_id": fp.origin_city_id, "to_city_id": fp.destination_city_id, "price": fp.price_usd}
            for fp in flight_prices_db
        ]
        print(f"Fetched {len(flight_prices)} flight prices", flush=True)
        
        from app.bonus.best_value_finder import BestValueFinder
        finder = BestValueFinder()
        result = finder.find_best_value(all_matches, budget, origin_city_id, flight_prices)
        
        print(f"Result: {result}", flush=True)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
