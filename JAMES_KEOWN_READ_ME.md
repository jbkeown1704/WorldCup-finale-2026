# 🏆 World Cup 2026 Travel Route Planner

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-red.svg)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://typescriptlang.org)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9-green.svg)](https://leafletjs.com)

A full-stack web application that helps FIFA World Cup fans plan optimal travel routes across 16 host cities in USA, Mexico, and Canada.

## 📋 Overview

This application solves the challenge of planning a multi-city trip to attend World Cup matches. It uses a **Nearest Neighbour algorithm** to optimize travel routes, ensuring fans can watch at least 5 matches across all 3 countries while staying within budget.

### The Problem
Fans attending the 2026 World Cup face a complex logistical challenge:
- 48 teams, 16 cities, 3 countries
- Need to attend at least 5 matches
- Must visit USA, Mexico, AND Canada
- Have a fixed budget for flights, accommodation, and tickets

### The Solution
This app automatically:
1. Finds the optimal order to visit selected matches
2. Validates country coverage and minimum match requirements
3. Calculates total trip costs
4. Suggests the best value matches within budget

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Backend | Python 3.14 + Flask | Fast development, easy to run |
| Database | SQLAlchemy + SQLite | Zero config, perfect for this scale |
| Frontend | React 18 + TypeScript | Type safety, great UI libraries |
| Maps | Leaflet + react-leaflet | Free, no API key required |
| Testing | pytest (backend), Jest (frontend) | Industry standard |

## ✨ Features

### Backend APIs
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/cities` | GET | Returns all 16 host cities |
| `/api/matches` | GET | Returns 48 matches (with city/date filters) |
| `/api/matches/:id` | GET | Returns single match details |
| `/api/route/optimise` | POST | Nearest Neighbour route optimisation |
| `/api/route/budget` | POST | Calculates flights + accommodation + tickets |
| `/api/route/best-value` | POST | Finds optimal matches within budget (Bonus) |

### Frontend Features
- **Match Browser** - Filter by city or date, click to select matches
- **Interactive Map** - Leaflet map with numbered markers and popups
- **Route Validation** - Visual indicators for countries and match count
- **Cost Calculator** - Detailed breakdown of all expenses
- **Best Value Dialog** - One-click budget optimisation

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 20+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/jbkeown1704/WorldCup-finale-2026.git
cd WorldCup-finale-2026


///////////////////////////////////////////////////////////////////////

cd backend/python-flask

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install flask flask-cors flask-sqlalchemy pytest

# Seed the database (16 cities, 48 matches, 240 flight prices)
python -m app.seed

# Start the server
flask run --port 3008


///////////////////////////////////////////////////////////////////////

cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev