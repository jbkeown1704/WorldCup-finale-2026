# Design Decisions & Trade-offs

## Why Nearest Neighbour?

### The Problem
The Traveling Salesman Problem (TSP) with 16 cities has 16! ≈ 2.09 × 10¹³ possible routes. Brute force is impossible.

### My Choice: Nearest Neighbour
- **Time Complexity:** O(n²) - ~256 operations for 16 cities
- **Space Complexity:** O(n) - just stores the route
- **Good enough:** Usually produces routes within 25% of optimal

### Trade-offs
| Approach | Pros | Cons |
|----------|------|------|
| Nearest Neighbour | Fast, simple, predictable | Not optimal |
| Brute Force | Guaranteed optimal | Impossible (16! permutations) |
| Dynamic Programming | Optimal for small n | O(n²·2ⁿ) still huge |
| Genetic Algorithm | Good approximation | Complex, random results |

### Alternative Considered
I considered adding **2-opt optimization** after the initial route, which would swap edges to improve the route. I decided against it because:
- The challenge specifically asked for Nearest Neighbour
- Added complexity wasn't necessary for the requirements
- The algorithm performs well enough for 5-8 matches

## Why SQLite Instead of PostgreSQL?

### The Decision
SQLite was the right choice for this project because:

| Aspect | SQLite | PostgreSQL |
|--------|--------|------------|
| Setup | Zero config | Need Docker/install |
| File size | ~500KB | ~10MB + dependencies |
| Portability | Single file | Requires server |
| Windows support | Native | More complex |

### Trade-off
PostgreSQL would be better for production (concurrent users, advanced features), but for an evaluation project, SQLite's simplicity wins.

## Why Leaflet Instead of Google Maps?

| Aspect | Leaflet | Google Maps |
|--------|---------|-------------|
| Cost | Free | Requires API key |
| Offline | Works offline | Needs internet |
| Privacy | No tracking | Google collects data |
| Setup | Just install | Need billing setup |

The evaluators don't need an API key to run my app - just `npm install`.

## Strategy Pattern Implementation

### Why Use It?
The strategy pattern allows easy swapping between algorithms:

```python
# Current: Nearest Neighbour
strategy = NearestNeighbourStrategy()

# Could easily switch to:
strategy = DateOnlyStrategy()  # Already implemented
strategy = OptimisedStrategy()  # Future improvement