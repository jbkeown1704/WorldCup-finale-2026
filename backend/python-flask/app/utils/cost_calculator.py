from datetime import datetime
from typing import Optional
from app.strategies.route_strategy import BudgetResult, CostBreakdown


class CostCalculator:
    """
    CostCalculator — YOUR TASK #5

    ============================================================
    WHAT YOU NEED TO IMPLEMENT:
    ============================================================

    The calculate method should:
    1. Calculate ticket costs (sum of ticketPrice for all matches)
    2. Calculate flight costs (between consecutive cities + from origin)
    3. Calculate accommodation costs (nights × city's accommodationPerNight rate)
    4. Check feasibility (total ≤ budget AND visits USA, Mexico, Canada)
    5. Return suggestions if not feasible

    ============================================================
    HELPER METHODS PROVIDED:
    ============================================================

    The helper methods below are already implemented for you:
    - get_flight_price(): Look up flight price between two cities
    - calculate_nights_between(): Calculate nights between two dates
    - get_countries_visited(): Get list of unique countries from matches
    - get_missing_countries(): Check which required countries are missing
    - generate_suggestions(): Create cost-saving suggestions

    """

    REQUIRED_COUNTRIES = ['USA', 'Mexico', 'Canada']

    def calculate(
        self,
        matches: list,
        budget: float,
        origin_city_id: str,
        flight_prices: list
    ) -> BudgetResult:
        """
        Calculate the total cost of a trip and check if it's within budget.

        Args:
            matches: List of match dicts the user wants to attend (sorted by date)
            budget: The user's maximum budget in USD
            origin_city_id: The city where the user starts their trip
            flight_prices: All available flight prices between cities

        Returns:
            BudgetResult dict containing feasibility, costs, and suggestions
        """
        # Step 1: Calculate ticket costs
        ticket_cost = sum(match.get('ticketPrice', 100) for match in matches)
        
        # Step 2: Calculate flight costs
        flight_cost = 0
        current_city = origin_city_id
        
        for match in matches:
            match_city_id = match['city']['id']
            flight_price = self.get_flight_price(current_city, match_city_id, flight_prices)
            flight_cost += flight_price
            current_city = match_city_id
        
        # Step 3: Calculate accommodation costs
        accommodation_cost = 0
        current_date = None
        
        for i, match in enumerate(matches):
            match_date = match['kickoff'].split('T')[0]
            
            if current_date is not None and i > 0:
                nights = self.calculate_nights_between(current_date, match_date)
                if nights > 0:
                    # Use previous city's accommodation rate
                    prev_city = matches[i-1]['city']
                    rate = prev_city.get('accommodationPerNight', 150)
                    accommodation_cost += nights * rate
            
            current_date = match_date
        
        # Step 4: Build CostBreakdown
        total_cost = ticket_cost + flight_cost + accommodation_cost
        
        cost_breakdown = {
            "ticketCost": round(ticket_cost, 2),
            "flightCost": round(flight_cost, 2),
            "accommodationCost": round(accommodation_cost, 2),
            "totalCost": round(total_cost, 2)
        }
        
        # Step 5: Check country constraint
        countries_visited = self.get_countries_visited(matches)
        missing_countries = self.get_missing_countries(countries_visited)
        meets_countries = len(missing_countries) == 0
        
        # Step 6: Check budget constraint
        meets_budget = total_cost <= budget
        meets_min_matches = len(matches) >= 5
        
        is_feasible = meets_budget and meets_countries and meets_min_matches
        
        # Step 7: Generate suggestions if not feasible
        suggestions = []
        minimum_budget_required = None
        
        if not is_feasible:
            if not meets_budget:
                minimum_budget_required = round(total_cost, 2)
                suggestions = self.generate_suggestions(matches, total_cost, budget)
            elif not meets_countries:
                suggestions.append(f"Missing countries: {', '.join(missing_countries)}. You must attend at least one match in each of USA, Mexico, and Canada.")
            elif not meets_min_matches:
                suggestions.append(f"Only {len(matches)} matches selected. You need at least 5 matches.")
        
        # Step 8: Return BudgetResult
        return {
            "feasible": is_feasible,
            "budget": budget,
            "minimumBudgetRequired": minimum_budget_required,
            "costBreakdown": cost_breakdown,
            "countriesVisited": countries_visited,
            "missingCountries": missing_countries,
            "numberOfMatches": len(matches),
            "meetsBudget": meets_budget,
            "meetsCountries": meets_countries,
            "meetsMinimumMatches": meets_min_matches,
            "suggestions": suggestions
        }

    # ============================================================
    # HELPER METHODS (Already implemented for you)
    # ============================================================

    def get_flight_price(
        self,
        from_city_id: str,
        to_city_id: str,
        flight_prices: list
    ) -> float:
        """
        Look up the flight price between two cities.
        Returns an estimated price if no direct flight exists.
        """
        if from_city_id == to_city_id:
            return 0

        for fp in flight_prices:
            if fp['from_city_id'] == from_city_id and fp['to_city_id'] == to_city_id:
                return fp['price']

        # If no direct flight, estimate based on average
        if flight_prices:
            avg_price = sum(fp['price'] for fp in flight_prices) / len(flight_prices)
            return avg_price * 1.2  # 20% markup for indirect routes
        return 300 * 1.2

    def calculate_nights_between(self, date1: str, date2: str) -> int:
        """Calculate the number of nights between two dates."""
        d1 = datetime.fromisoformat(date1.split('T')[0])
        d2 = datetime.fromisoformat(date2.split('T')[0])
        return max(0, (d2 - d1).days)

    def get_countries_visited(self, matches: list) -> list:
        """Get list of unique countries visited from matches."""
        countries = set()
        for match in matches:
            countries.add(match['city']['country'])
        return list(countries)

    def get_missing_countries(self, countries_visited: list) -> list:
        """Check which required countries (USA, Mexico, Canada) are missing."""
        return [c for c in self.REQUIRED_COUNTRIES if c not in countries_visited]

    def generate_suggestions(
        self,
        matches: list,
        total: float,
        budget: float
    ) -> list:
        """Generate cost-saving suggestions when budget is exceeded."""
        suggestions = []
        overage = total - budget

        if len(matches) > 5:
            most_expensive = max(matches, key=lambda m: m['ticketPrice'])
            suggestions.append(
                f"Consider removing the {most_expensive['homeTeam']['name']} vs "
                f"{most_expensive['awayTeam']['name']} match to save ${most_expensive['ticketPrice']}"
            )

        suggestions.append(
            f"You are ${overage:.0f} over budget. Consider reducing the number of matches."
        )

        return suggestions
