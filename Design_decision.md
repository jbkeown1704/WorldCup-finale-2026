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


📁 WorldCup-finale-2026/
│
├── 📁 backend/
│   └── 📁 python-flask/
│       │
│       ├── 📁 app/
│       │   │
│       │   ├── 📁 bonus/
│       │   │   └── 📄 best_value_finder.py     ← Bonus: finds best matches within budget
│       │   │
│       │   ├── 📁 models/
│       │   │   ├── 📄 city.py                  ← City database model
│       │   │   ├── 📄 match.py                 ← Match database model
│       │   │   ├── 📄 team.py                  ← Team database model
│       │   │   └── 📄 flight_price.py          ← Flight prices model
│       │   │
│       │   ├── 📁 routes/
│       │   │   ├── 📄 cities.py                ← GET /api/cities (Task #1)
│       │   │   ├── 📄 matches.py               ← GET /api/matches (Task #2)
│       │   │   ├── 📄 optimise.py              ← POST /optimise, /budget, /best-value (Tasks #3, #5, Bonus)
│       │   │   └── 📄 itineraries.py           ← Pre-built (save/load trips)
│       │   │
│       │   ├── 📁 strategies/
│       │   │   ├── 📄 route_strategy.py        ← Strategy interface
│       │   │   ├── 📄 date_only_strategy.py    ← Naive example (working)
│       │   │   └── 📄 nearest_neighbour_strategy.py  ← YOUR algorithm (Task #3)
│       │   │
│       │   ├── 📁 utils/
│       │   │   ├── 📄 haversine.py             ← Distance calculator (pre-built)
│       │   │   └── 📄 cost_calculator.py       ← Budget calculator (Task #5)
│       │   │
│       │   ├── 📄 __init__.py                  ← Flask app factory
│       │   ├── 📄 db.py                        ← Database setup
│       │   └── 📄 seed.py                      ← Seeds SQLite database
│       │
│       ├── 📁 tests/
│       │   └── 📄 test_nearest_neighbour_strategy.py  ← 3 unit tests (Task #4)
│       │
│       ├── 📁 venv/                            ← Python virtual environment
│       ├── 📄 worldcup.db                      ← SQLite database (auto-created)
│       └── 📄 requirements.txt                 ← Python dependencies
│
├── 📁 frontend/
│   │
│   ├── 📁 src/
│   │   │
│   │   ├── 📁 components/
│   │   │   ├── 📄 RouteMap.tsx                 ← Map with markers (Frontend Task)
│   │   │   ├── 📄 ItineraryPanel.tsx           ← Route validation display
│   │   │   ├── 📄 CostBreakdownPanel.tsx       ← Budget breakdown display
│   │   │   ├── 📄 BestValueDialog.tsx          ← Bonus dialog
│   │   │   ├── 📄 MatchBrowser.tsx             ← Match list/filters
│   │   │   └── 📄 MatchCard.tsx                ← Individual match card
│   │   │
│   │   ├── 📁 types/
│   │   │   └── 📄 index.ts                     ← TypeScript interfaces
│   │   │
│   │   ├── 📁 api/
│   │   │   └── 📄 client.ts                    ← API calls to backend
│   │   │
│   │   ├── 📄 App.tsx                          ← Main app component
│   │   └── 📄 main.tsx                         ← Entry point
│   │
│   ├── 📁 __tests__/                           ← Frontend tests (nice-to-have)
│   ├── 📄 package.json                         ← Node dependencies
│   └── 📄 index.html                           ← HTML entry point
│
├── 📁 seed-data/
│   ├── 📄 cities.json                          ← 16 cities with coordinates
│   ├── 📄 matches.json                         ← 48 matches with teams
│   └── 📄 teams.json                           ← 48 teams data
│
├── 📁 postman/
│   └── 📄 WorldCup2026_API.postman_collection.json  ← API test collection
│
├── 📄 README.md                                ← Setup instructions (you write)
├── 📄 DECISIONS.md                             ← Design decisions (you write)
└── 📄 .gitignore                               ← Git ignore rules




┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER BROWSER                                    │
│                           http://localhost:5173                              │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           REACT FRONTEND                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ MatchBrowser │  │RouteMap     │  │ItineraryPanel│ │CostBreakdown│        │
│  │ (select     │  │(Leaflet map │  │(validation) │  │Panel        │        │
│  │  matches)   │  │ with popups)│  │             │  │             │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                    │                                        │
│                                    │ API calls via /api/*                   │
│                                    ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ http://localhost:3008
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FLASK BACKEND                                     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                         ROUTES (Blueprints)                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │    │
│  │  │ /api/cities  │  │ /api/matches │  │ /api/route/optimise       │  │    │
│  │  │ (Task #1)    │  │ (Task #2)    │  │ (Task #3)                 │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────┐  ┌──────────────────────────────┐    │    │
│  │  │ /api/route/budget        │  │ /api/route/best-value        │    │    │
│  │  │ (Task #5)                │  │ (Bonus)                      │    │    │
│  │  └──────────────────────────┘  └──────────────────────────────┘    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                      STRATEGY PATTERN                               │    │
│  │  ┌─────────────────────────┐    ┌─────────────────────────────┐   │    │
│  │  │ DateOnlyStrategy        │    │ NearestNeighbourStrategy    │   │    │
│  │  │ (naive - sort by date)  │    │ (YOUR algorithm)            │   │    │
│  │  └─────────────────────────┘    └─────────────────────────────┘   │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    SQLAlchemy ORM                                   │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────────┐    │    │
│  │  │ City     │ │ Match    │ │ Team     │ │ FlightPrice        │    │    │
│  │  │ model    │ │ model    │ │ model    │ │ model              │    │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────────────────┘    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                         SQLite Database                              │    │
│  │                         (worldcup.db)                               │    │
│  │                                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │    │
│  │  │ cities      │  │ matches     │  │ teams       │                 │    │
│  │  │ (16 rows)   │  │ (48 rows)   │  │ (48 rows)   │                 │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                 │    │
│  │  ┌─────────────────────────────────────────────────────┐           │    │
│  │  │ flight_prices (240 rows)                            │           │    │
│  │  └─────────────────────────────────────────────────────┘           │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘