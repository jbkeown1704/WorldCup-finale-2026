import pytest
from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy


class TestNearestNeighbourStrategy:
    """
    NearestNeighbourStrategyTest — YOUR TASK #4

    Unit tests for the NearestNeighbourStrategy.
    """

    def setup_method(self):
        self.strategy = NearestNeighbourStrategy()

    def test_happy_path_returns_valid_route(self):
        """Should return a valid route for multiple matches (happy path)"""
        # Arrange: Create an array of matches across different cities and dates
        matches = [
            {
                "id": "match-1",
                "kickoff": "2026-06-11T17:00:00Z",
                "city": {
                    "id": "city-new-york",
                    "name": "New York",
                    "latitude": 40.7128,
                    "longitude": -74.0060
                }
            },
            {
                "id": "match-2",
                "kickoff": "2026-06-12T19:00:00Z",
                "city": {
                    "id": "city-boston",
                    "name": "Boston",
                    "latitude": 42.3601,
                    "longitude": -71.0589
                }
            },
            {
                "id": "match-3",
                "kickoff": "2026-06-13T21:00:00Z",
                "city": {
                    "id": "city-philadelphia",
                    "name": "Philadelphia",
                    "latitude": 39.9526,
                    "longitude": -75.1652
                }
            }
        ]
        
        # Act: Call self.strategy.optimise(matches)
        result = self.strategy.optimise(matches)
        
        # Assert: Verify the result has stops, totalDistance > 0, and strategy = 'nearest-neighbour'
        assert result is not None
        assert "stops" in result
        assert "totalDistance" in result
        assert "strategy" in result
        assert result["strategy"] == "nearest-neighbour"
        assert len(result["stops"]) == 3
        assert result["totalDistance"] > 0

    def test_empty_matches_returns_empty_route(self):
        """Should return an empty route for empty matches"""
        # Arrange: Create an empty array of matches
        matches = []
        
        # Act: Call self.strategy.optimise([])
        result = self.strategy.optimise(matches)
        
        # Assert: Verify the result has empty stops and totalDistance = 0
        assert result is not None
        assert result["stops"] == []
        assert result["totalDistance"] == 0
        assert result["strategy"] == "nearest-neighbour"

    def test_single_match_returns_zero_distance(self):
        """Should return zero distance for a single match"""
        # Arrange: Create an array with a single match
        matches = [
            {
                "id": "match-1",
                "kickoff": "2026-06-11T17:00:00Z",
                "city": {
                    "id": "city-new-york",
                    "name": "New York",
                    "latitude": 40.7128,
                    "longitude": -74.0060
                }
            }
        ]
        
        # Act: Call self.strategy.optimise(matches)
        result = self.strategy.optimise(matches)
        
        # Assert: Verify totalDistance = 0 and len(stops) = 1
        assert result is not None
        assert len(result["stops"]) == 1
        assert result["totalDistance"] == 0
        assert result["stops"][0]["distanceFromPrevious"] == 0