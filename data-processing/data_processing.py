import pandas as pd
import requests
import time
import json
from geopy.distance import geodesic

#  Foursquare Places API Key & Headers

FOURSQUARE_API_KEY = "TLG5B2RTGLRA4FE2A4VTMCKXCCMNRBZTPWXZOAIRDL1IOE2H"
HEADERS = {
    "Authorization": f"Bearer {FOURSQUARE_API_KEY}",
    "Accept": "application/json",
    "X-Places-Api-Version": "2025-06-17"
}

#  Load CSV files
try:
    neighborhoods = pd.read_csv("delhi_neighborhoods.csv")
    metro_stations = pd.read_csv("metro_stations.csv")
except FileNotFoundError as e:
    print(f"Error: {e}. Please make sure your CSV files are in the same directory.")
    exit()

#  Amenity query terms
amenities = [
    "cafe", "restaurant", "gym", "school", "hospital", "grocery", 
    "playground", "park", "day care", "bookstore", "coaching center"
]


#  Function to fetch total place count by paginating
def fetch_amenity_count(lat, lon, query_term, radius):
    """
    Fetches the total count by paginating through all results using the cursor.
    This is the correct method for the new Foursquare Places API.
    """
    url = "https://places-api.foursquare.com/places/search"
    total = 0
    cursor = None

    while True:
        params = {
            "ll": f"{lat},{lon}",
            "radius": int(radius),
            "query": query_term,
            "fields": "fsq_place_id", 
            "limit": 50
        }
        if cursor:
            params["cursor"] = cursor

        try:
            res = requests.get(url, headers=HEADERS, params=params)
            
            if res.status_code != 200:
                data = res.json()
                print(f"  API error ({query_term}):", data.get("message", "Unknown error"))
                return total 

            data = res.json()
            total += len(data.get("results", []))
            
           
            cursor = data.get("context", {}).get("next_cursor")
            if not cursor:
                break # Exit the loop if there are no more pages

            time.sleep(0.2) 

        except Exception as e:
            print(f"  Request failed for {query_term}: {e}")
            return total # Return what we have so far

    return total

# Distance to nearest metro station
def nearest_metro_distance(lat, lon):
    try:
        dists = metro_stations.apply(
            lambda row: geodesic((lat, lon), (row["Latitude"], row["Longitude"])).meters,
            axis=1
        )
        return round(dists.min(), 2)
    except Exception as e:
        print(f"Metro distance error: {e}")
        return None

# Function to normalize all collected data
def normalize_data(data):
    print("\n Normalizing data...")
    df = pd.DataFrame(data)

    # --- Stage 1: Normalize SIMPLE attributes ---
    simple_attributes = [
        'nearest_metro_m', 'cafe_count', 'restaurant_count', 'gym_count', 'hospital_count'
    ]
    for attr in simple_attributes:
        if attr not in df.columns: continue
        min_val, max_val = df[attr].min(), df[attr].max()
        norm_attr_name = f"norm_{attr.replace('_count', '').replace('_m', '')}"
        if max_val == min_val:
            df[norm_attr_name] = 1.0
            continue
        if 'metro' in attr: # Less is better
            df[norm_attr_name] = 1 - ((df[attr] - min_val) / (max_val - min_val))
        else: # More is better
            df[norm_attr_name] = (df[attr] - min_val) / (max_val - min_val)
        print(f"  Normalized simple attribute: '{attr}' -> '{norm_attr_name}'")

    # --- Stage 2: Create and Normalize COMPOSITE scores ---

    # 2a. Family-Friendly Score
    print("  Creating composite score: 'norm_family_friendly'")
    df['family_friendly_raw'] = df['school_count'] + df['playground_count'] + df['day care_count']
    min_ff, max_ff = df['family_friendly_raw'].min(), df['family_friendly_raw'].max()
    if max_ff == min_ff:
        df['norm_family_friendly'] = 1.0
    else:
        df['norm_family_friendly'] = (df['family_friendly_raw'] - min_ff) / (max_ff - min_ff)

    # 2b. Community Score
    print("  Creating composite score: 'norm_community'")
    # Using park and grocery counts as a proxy for community spaces and local markets
    df['community_raw'] = df['park_count'] + df['grocery_count']
    min_comm, max_comm = df['community_raw'].min(), df['community_raw'].max()
    if max_comm == min_comm:
        df['norm_community'] = 1.0
    else:
        df['norm_community'] = (df['community_raw'] - min_comm) / (max_comm - min_comm)

    
    # 2d. Student-Friendly Score
    print("  Creating composite score: 'norm_student_friendly'")
    # Combines access to bookstores and coaching centers
    df['student_friendly_raw'] = df['bookstore_count'] + df['coaching center_count']
    min_student, max_student = df['student_friendly_raw'].min(), df['student_friendly_raw'].max()
    if max_student == min_student:
        df['norm_student_friendly'] = 1.0
    else:
        df['norm_student_friendly'] = (df['student_friendly_raw'] - min_student) / (max_student - min_student)
        
    return df.to_dict('records')


# Process neighborhoods
processed_data = []
for _, hood in neighborhoods.iterrows():
    print(f"\n Processing {hood['name']}...")
    lat, lon, radius = hood["lat"], hood["lon"], hood["radius_km"] * 1000

    data = {
        "name": hood["name"],
        "lat": lat, "lon": lon,
        "radius_m": radius,
        "nearest_metro_m": nearest_metro_distance(lat, lon)
    }

    for amenity in amenities:
        count = fetch_amenity_count(lat, lon, amenity, radius)
        print(f"   {amenity:<10}: {count}")
        data[f"{amenity}_count"] = count
        time.sleep(0.3) 

    processed_data.append(data)

#  Normalize the final data
final_data = normalize_data(processed_data)

#  Save to JSON
with open("processed_delhi_data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4)

print("\n  Successfully processed and saved normalized data to 'processed_delhi_data.json'")