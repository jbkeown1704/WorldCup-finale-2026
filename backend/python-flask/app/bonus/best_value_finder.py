from datetime import datetime
from typing import TypedDict, Optional


class BestValueResult(TypedDict):
    """Response for best value finder."""
    withinBudget: bool
    matches: list
    route: Optional[dict]
    costBreakdown: dict
    countriesVisited: list
    matchCount: int
    message: str


class BestValueFinder:
    """
    BestValueFinder — BONUS CHALLENGE #1
    """

    REQUIRED_COUNTRIES = ['USA', 'Mexico', 'Canada']

    def find_best_value(
        self,
        all_matches: list,
        budget: float,
        origin_city_id: str,
        flight_prices: list
    ) -> BestValueResult:
        """
        Find the best value combination of matches within budget.
        Uses a simple greedy approach.
        """
        
        # Group matches by country
        matches_by_country = self.get_matches_by_country(all_matches)
        
        # Step 1: Pick the cheapest match from each required country
        selected_matches = []
        for country in self.REQUIRED_COUNTRIES:
            if country not in matches_by_country or not matches_by_country[country]:
                return {
                    "withinBudget": False,
                    "matches": [],
                    "route": None,
                    "costBreakdown": {},
                    "countriesVisited": [],
                    "matchCount": 0,
                    "message": f"No matches available in {country}"
                }
            # Pick cheapest match in this country
            cheapest = min(matches_by_country[country], key=lambda m: m['ticketPrice'])
            selected_matches.append(cheapest)
        
        # Remove selected matches from available pool
        remaining_matches = [m for m in all_matches if m not in selected_matches]
        
        # Sort remaining by ticket price (cheapest first)
        remaining_matches.sort(key=lambda m: m['ticketPrice'])
        
        # Step 2: Greedily add cheapest matches while staying within budget
        for match in remaining_matches:
            # Test adding this match
            test_matches = selected_matches + [match]
            test_matches.sort(key=lambda m: m['kickoff'])
            test_cost = self.calculate_trip_cost(test_matches, origin_city_id, flight_prices)
            
            if test_cost <= budget:
                selected_matches = test_matches
            else:
                # Can't add this match or any more (since sorted by price)
                break
        
        # Step 3: Check minimum matches requirement
        if len(selected_matches) < 5:
            return {
                "withinBudget": False,
                "matches": selected_matches,
                "route": None,
                "costBreakdown": self._get_cost_breakdown(selected_matches, origin_city_id, flight_prices),
                "countriesVisited": self.REQUIRED_COUNTRIES,
                "matchCount": len(selected_matches),
                "message": f"Only {len(selected_matches)} matches, need at least 5"
            }
        
        # Step 4: Build the optimised route
        from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy
        strategy = NearestNeighbourStrategy()
        route = strategy.optimise(selected_matches)
        
        # Add country info to route
        countries_visited = set()
        for stop in route.get('stops', []):
            if 'city' in stop and 'country' in stop['city']:
                countries_visited.add(stop['city']['country'])
        
        route['countriesVisited'] = list(countries_visited)
        route['feasible'] = len(countries_visited) == 3 and len(route.get('stops', [])) >= 5
        
        missing = [c for c in self.REQUIRED_COUNTRIES if c not in countries_visited]
        route['missingCountries'] = missing
        
        # Step 5: Return success result
        return {
            "withinBudget": True,
            "matches": selected_matches,
            "route": route,
            "costBreakdown": self._get_cost_breakdown(selected_matches, origin_city_id, flight_prices),
            "countriesVisited": list(countries_visited),
            "matchCount": len(selected_matches),
            "message": f"Found {len(selected_matches)} matches within ${budget:,.2f} budget"
        }
    
    def _get_cost_breakdown(self, matches, origin_city_id, flight_prices):
        """Get detailed cost breakdown for a set of matches."""
        if not matches:
            return {"ticketCost": 0, "flightCost": 0, "accommodationCost": 0, "totalCost": 0}
        
        sorted_matches = sorted(matches, key=lambda m: m['kickoff'])
        
        ticket_cost = sum(m['ticketPrice'] for m in sorted_matches)
        
        flight_cost = self.get_flight_price(
            origin_city_id,
            sorted_matches[0]['city']['id'],
            flight_prices
        )
        for i in range(1, len(sorted_matches)):
            flight_cost += self.get_flight_price(
                sorted_matches[i-1]['city']['id'],
                sorted_matches[i]['city']['id'],
                flight_prices
            )
        
        accommodation_cost = 0.0
        for i, match in enumerate(sorted_matches):
            nights = 1
            if i < len(sorted_matches) - 1:
                d1 = datetime.fromisoformat(match['kickoff'].split('T')[0])
                d2 = datetime.fromisoformat(sorted_matches[i+1]['kickoff'].split('T')[0])
                nights = max(1, (d2 - d1).days)
            accommodation_cost += nights * match['city']['accommodationPerNight']
        
        return {
            "ticketCost": round(ticket_cost, 2),
            "flightCost": round(flight_cost, 2),
            "accommodationCost": round(accommodation_cost, 2),
            "totalCost": round(ticket_cost + flight_cost + accommodation_cost, 2)
        }

    # ============================================================
    # HELPER METHODS (Already implemented for you)
    # ============================================================

    def get_matches_by_country(self, matches: list) -> dict:
        """Group matches by their country."""
        by_country = {}
        for match in matches:
            country = match['city']['country']
            if country not in by_country:
                by_country[country] = []
            by_country[country].append(match)
        return by_country

    def get_flight_price(
        self,
        from_city_id: str,
        to_city_id: str,
        flight_prices: list
    ) -> float:
        """Look up the flight price between two cities."""
        if from_city_id == to_city_id:
            return 0

        for fp in flight_prices:
            if fp['from_city_id'] == from_city_id and fp['to_city_id'] == to_city_id:
                return fp['price']

        if flight_prices:
            avg_price = sum(fp['price'] for fp in flight_prices) / len(flight_prices)
            return avg_price * 1.2
        return 300 * 1.2

    def calculate_trip_cost(
        self,
        matches: list,
        origin_city_id: str,
        flight_prices: list
    ) -> float:
        """Calculate the total cost for a set of matches."""
        if not matches:
            return 0

        sorted_matches = sorted(matches, key=lambda m: m['kickoff'])

        # Ticket costs
        ticket_cost = sum(m['ticketPrice'] for m in matches)

        # Flight costs
        flight_cost = self.get_flight_price(
            origin_city_id,
            sorted_matches[0]['city']['id'],
            flight_prices
        )
        for i in range(1, len(sorted_matches)):
            flight_cost += self.get_flight_price(
                sorted_matches[i - 1]['city']['id'],
                sorted_matches[i]['city']['id'],
                flight_prices
            )

        # Accommodation costs (simplified)
        accommodation_cost = 0.0
        for i, match in enumerate(sorted_matches):
            nights = 1  # At least one night per match
            if i < len(sorted_matches) - 1:
                d1 = datetime.fromisoformat(match['kickoff'].split('T')[0])
                d2 = datetime.fromisoformat(sorted_matches[i + 1]['kickoff'].split('T')[0])
                nights = max(1, (d2 - d1).days)
            accommodation_cost += nights * match['city']['accommodationPerNight']

        return ticket_cost + flight_cost + accommodation_cost