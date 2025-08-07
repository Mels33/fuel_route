# 🛣️ Optimal Fuel Route API (Django)

This Django-based API calculates the most **fuel cost-efficient** route from a `start` location to a `finish` location in the USA. It takes into account:

- Vehicle range: 500 miles
- Fuel efficiency: 10 miles per gallon
- Fuel prices: from a CSV data file
- Fuel stops: selected to minimize total fuel cost

---

## 🚀 Features

- Uses OpenStreetMap's **Nominatim API** for geocoding addresses.
- Builds a route graph using **NetworkX** and **BallTree**.
- Returns the **total fuel cost** and a **link to the route** on OpenStreetMap.

---

## 🏗️ Setup Instructions

### 1. Clone the project and create virtual environment

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
