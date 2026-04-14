from app.strategies.route_strategy import RouteStrategy, build_route
from app.utils.haversine import calculate_distance


class NearestNeighbourStrategy(RouteStrategy):
    """
    NearestNeighbourStrategy — YOUR TASK #3

    Implement a smarter route optimisation using the nearest-neighbour heuristic.
    The idea: when you have multiple matches on the same day (or close dates),
    choose the one that's geographically closest to where you currently are.

    This should produce shorter total distances than DateOnlyStrategy.
    """

    def optimise(self, matches: list) -> dict:
        # TODO: Implement nearest-neighbour optimisation (YOUR TASK #3)
        
        #First part is a error handling if no matches are available, this will return an error message
        if not matches:
            return build_route([], 'nearest-neighbour')



        # Pseudocode:
        # 1. Sort all matches by kickoff date
        sorted_matches = sorted(matches, key=lambda m: m['kickoff'])


        grouped_by_date = {}
        
        # Loop through each match in date order
        for match in sorted_matches:
            # Extract just the date part (YYYY-MM-DD) from the full timestamp
            # Example: "2026-06-11T17:00:00Z" becomes "2026-06-11"
            date = match['kickoff'].split('T')[0]
            
            # If this date isn't a key in our dictionary yet, create it with an empty list
            if date not in grouped_by_date:
                grouped_by_date[date] = []
            
            # Add the current match to the list for this date
            grouped_by_date[date].append(match)
        
        # Build the route using nearest-neighbour logic
        # ordered_matches will store matches in the order we plan to attend them
        ordered_matches = []
        
        # current_city tracks where we are after each match
        # Starts as None because we haven't attended any matches yet
        current_city = None
        
        # Sort the dates chronologically and process each day group
        # sorted() on dictionary keys puts earliest dates first
        for date in sorted(grouped_by_date.keys()):
            # Get all matches happening on this specific date
            matches_on_day = grouped_by_date[date]
            
            # Case A: Only one match on this day
            if len(matches_on_day) == 1:
                # No choice to make - we must attend this match
                chosen_match = matches_on_day[0]
            
            # Case B: Multiple matches on the same day (e.g., 2pm and 8pm)
            else:
                # If we have a current location (not the first day)
                if current_city:
                    # Find the match closest to where we currently are
                    closest_distance = float('inf')  # Start with "infinity"
                    chosen_match = None
                    
                    # Check each match happening on this day
                    for match in matches_on_day:
                        # Get the city where this match is played
                        match_city = match['city']
                        
                        # Calculate distance from our current city to this match's city
                        # Uses latitude and longitude coordinates
                        distance = calculate_distance(
                            current_city['latitude'], current_city['longitude'],
                            match_city['latitude'], match_city['longitude']
                        )
                        
                        # If this match is closer than any we've seen so far
                        if distance < closest_distance:
                            closest_distance = distance   # Update the closest distance
                            chosen_match = match          # Remember this as the best choice
                else:
                    # First day with multiple matches (we have no current location yet)
                    # Just pick the first match in the list
                    chosen_match = matches_on_day[0]
            
            # Add the chosen match to our route in order
            ordered_matches.append(chosen_match)
            
            # Update our current location to the city of the match we just attended
            # This affects which city is "closest" for the next day's choice
            current_city = chosen_match['city']
        
        # Return the result in the format expected by the API
        # build_route calculates:
        #   - stop numbers (1, 2, 3...)
        #   - distance from previous stop
        #   - total distance of entire route
        # It returns: { "stops": [...], "strategy": "nearest-neighbour", "totalDistance": 1234.56 }
        return build_route(ordered_matches, 'nearest-neighbour')
