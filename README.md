# 🛣️ Optimal Fuel Route API (Django)

This Django-based API calculates the most **fuel cost-efficient** route from a `start` location to a `finish` location in the USA. It takes into account:

- Vehicle range: 500 miles  
- Fuel efficiency: 10 miles per gallon  
- Fuel prices: from a CSV data file  
- Fuel stops: selected to minimize total fuel cost  

---

## 🚀 Features

- Uses OpenStreetMap's **Nominatim API** for geocoding addresses  
- Builds a route graph using **NetworkX** and **BallTree**  
- Returns the **total fuel cost** and a **link to the route** on OpenStreetMap  

---

## 🏗️ Setup Instructions

### 1. Clone the project and create virtual environment

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
python -m venv venv
2. Activate the virtual environment
On Linux/macOS:

bash
Копировать
Редактировать
source venv/bin/activate
On Windows (PowerShell):

powershell
Копировать
Редактировать
.\venv\Scripts\activate
3. Install dependencies
bash
Копировать
Редактировать
pip install -r requirements.txt
📡 API Usage
🔹 Endpoint:
bash
Копировать
Редактировать
POST /api/route/
🔹 Request body (JSON):
json
Копировать
Редактировать
{
  "start": "New York, NY",
  "finish": "Chicago, IL"
}
🔹 Response (JSON):
json
Копировать
Редактировать
{
  "total_fuel_cost": 198.53,
  "route_url": "https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=40.7128,-74.0060;41.093,-87.1254;41.8781,-87.6298"
}
📍 How It Works
Geocoding: Converts start and finish addresses to geographic coordinates using Nominatim API.

Data loading: Reads fuel station data with prices and coordinates from CSV.

Graph building: Constructs a weighted directed graph using NetworkX and BallTree where nodes are stations and edges represent reachable distances within 500 miles.

Pathfinding: Uses Dijkstra's algorithm to find the route minimizing total fuel cost based on vehicle consumption (10 miles/gallon) and fuel prices.

Response: Returns total fuel cost and a link to visualize the route on OpenStreetMap.

🛠️ Example with curl
bash
Копировать
Редактировать
curl -X POST http://127.0.0.1:8000/api/route/ \
  -H "Content-Type: application/json" \
  -d '{"start": "Los Angeles, CA", "finish": "Las Vegas, NV"}'
📦 Notes
Max fuel range: 500 miles

Consumption: 10 miles/gallon

No API keys required (uses public geocoding and routing)

You can visualize the route using the returned OpenStreetMap URL

🧑‍💻 Author
Built by Mels as part of a backend challenge for a Django Developer position.
