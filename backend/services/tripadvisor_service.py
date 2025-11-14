"""
TripAdvisor/RapidAPI service for fetching hotels and activities data.
Falls back to mock data if API keys are missing or API calls fail.
"""

import time
import math
import requests
from typing import Optional
from config.settings import Config
from services.mock_data import get_mock_hotels, get_mock_activities


# Constants
PLACEHOLDER_IMAGE = "https://via.placeholder.com/400x300?text=No+Image"
REQUEST_TIMEOUT = 8
MAX_RETRIES = 3
RETRY_BACKOFFS = [0.5, 1.0, 2.0]
HOTEL_MAX_DISTANCE_KM = 200
ACTIVITY_MAX_DISTANCE_KM = 100

# Hotel category keywords (case-insensitive matching)
HOTEL_CATEGORIES = ["hotel", "lodging", "resort", "motel", "guest_house", "inn", "hostel"]

# Activity category allowlist
ALLOWED_ACTIVITY_CATEGORIES = [
    "Attraction", "Tours", "Outdoor Activities", "Nature & Parks",
    "Sights & Landmarks", "Cultural", "Hiking Trails", "Adventure",
    "Wildlife", "Museums", "Historical Sites", "Monuments"
]

# Water activity keywords to exclude for mountain destinations
WATER_ACTIVITY_KEYWORDS = ["scuba", "diving", "surfing", "snorkeling", "water sports", "sailing", "kayaking"]

# Mountain destination keywords
MOUNTAIN_KEYWORDS = ["mount", "mountain", "hill", "himalaya", "himalayan", "annapurna", "nepal", "manali", "leh", "mustang", "trek", "peak"]

# Beach destination keywords
BEACH_KEYWORDS = ["goa", "bali", "maldives", "boracay", "phuket", "beach", "coast", "island"]


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth (in km).
    
    Args:
        lat1, lon1: Latitude and longitude of first point in decimal degrees
        lat2, lon2: Latitude and longitude of second point in decimal degrees
    
    Returns:
        Distance in kilometers
    """
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def within_radius(lat1: float, lon1: float, lat2: float, lon2: float, km: float) -> bool:
    """
    Check if two coordinates are within the specified radius.
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
        km: Maximum distance in kilometers
    
    Returns:
        True if within radius, False otherwise
    """
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return distance <= km


def make_api_request(url: str, headers: dict, params: dict) -> Optional[dict]:
    """
    Make an API request with retry logic and exponential backoff.
    
    Args:
        url: API endpoint URL
        headers: Request headers
        params: Request parameters
    
    Returns:
        JSON response as dict, or None if all retries fail
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Rate limited - wait longer before retry
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_BACKOFFS[attempt] * 2
                    print(f"[WARNING] Rate limited, waiting {wait_time}s before retry {attempt + 1}/{MAX_RETRIES}")
                    time.sleep(wait_time)
                    continue
            else:
                print(f"[WARNING] API returned status {response.status_code}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_BACKOFFS[attempt])
                    continue
        except requests.exceptions.Timeout:
            print(f"[WARNING] Request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFFS[attempt])
                continue
        except requests.exceptions.RequestException as e:
            print(f"[WARNING] Request error: {str(e)} (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFFS[attempt])
                continue
        except Exception as e:
            print(f"[ERROR] Unexpected error: {str(e)}")
            break
    
    return None


def extract_image_url(result_obj: dict) -> str:
    """
    Extract image URL from result object, trying multiple paths.
    
    Args:
        result_obj: The result_object from API response
    
    Returns:
        Absolute image URL or placeholder
    """
    photo = result_obj.get("photo", {})
    if not photo:
        return PLACEHOLDER_IMAGE
    
    images = photo.get("images", {})
    if not images:
        return PLACEHOLDER_IMAGE
    
    # Try large -> medium -> original -> thumbnail
    for size in ["large", "medium", "original", "thumbnail"]:
        size_obj = images.get(size, {})
        if size_obj:
            url = size_obj.get("url", "")
            if url and url.startswith("http"):
                return url
    
    return PLACEHOLDER_IMAGE


def extract_price(result_obj: dict) -> tuple[str, Optional[str]]:
    """
    Extract price and currency from result object, trying multiple paths.
    
    Args:
        result_obj: The result_object from API response
    
    Returns:
        Tuple of (price_string, currency)
    """
    # Try result["price"]
    price = result_obj.get("price")
    if price:
        currency = result_obj.get("currency", {}).get("code") if isinstance(result_obj.get("currency"), dict) else result_obj.get("currency")
        return (str(price), currency)
    
    # Try result["price_range"]
    price_range = result_obj.get("price_range")
    if price_range:
        currency = result_obj.get("currency", {}).get("code") if isinstance(result_obj.get("currency"), dict) else result_obj.get("currency")
        return (str(price_range), currency)
    
    # Try result["price_level"]
    price_level = result_obj.get("price_level")
    if price_level:
        # Convert price level (1-4) to approximate price
        price_map = {1: "₹1,000-2,000", 2: "₹2,000-4,000", 3: "₹4,000-8,000", 4: "₹8,000+"}
        price_str = price_map.get(price_level, f"Level {price_level}")
        return (price_str, "INR")
    
    # Try result["offer_group"]["offers"][0]["price"]
    offer_group = result_obj.get("offer_group", {})
    if offer_group:
        offers = offer_group.get("offers", [])
        if offers and len(offers) > 0:
            offer = offers[0]
            price = offer.get("price")
            if price:
                currency = offer.get("currency", {}).get("code") if isinstance(offer.get("currency"), dict) else offer.get("currency")
                return (str(price), currency)
    
    return ("Price unavailable", None)


def is_hotel_category(result_obj: dict) -> bool:
    """
    Check if result object represents a hotel/lodging.
    
    Args:
        result_obj: The result_object from API response
    
    Returns:
        True if it's a hotel category, False otherwise
    """
    category = result_obj.get("category", {})
    category_key = category.get("key", "").lower() if isinstance(category, dict) else str(category).lower()
    category_name = category.get("name", "").lower() if isinstance(category, dict) else ""
    
    # Check category key
    for hotel_cat in HOTEL_CATEGORIES:
        if hotel_cat in category_key:
            return True
    
    # Check category name
    for hotel_cat in HOTEL_CATEGORIES:
        if hotel_cat in category_name:
            return True
    
    # Check name for hotel keywords
    name = result_obj.get("name", "").lower()
    for hotel_cat in HOTEL_CATEGORIES:
        if hotel_cat in name:
            return True
    
    return False


def is_mountain_destination(destination: str) -> bool:
    """
    Check if destination is a mountain region.
    
    Args:
        destination: Destination name
    
    Returns:
        True if mountain destination, False otherwise
    """
    dest_lower = destination.lower()
    return any(keyword in dest_lower for keyword in MOUNTAIN_KEYWORDS)


def is_beach_destination(destination: str) -> bool:
    """
    Check if destination is a beach/coastal region.
    
    Args:
        destination: Destination name
    
    Returns:
        True if beach destination, False otherwise
    """
    dest_lower = destination.lower()
    return any(keyword in dest_lower for keyword in BEACH_KEYWORDS)


def is_water_activity(activity_name: str, category: str) -> bool:
    """
    Check if activity is water-based.
    
    Args:
        activity_name: Activity name
        category: Activity category
    
    Returns:
        True if water activity, False otherwise
    """
    name_lower = activity_name.lower()
    category_lower = category.lower()
    
    for keyword in WATER_ACTIVITY_KEYWORDS:
        if keyword in name_lower or keyword in category_lower:
            return True
    
    return False


def is_allowed_activity_category(category: str) -> bool:
    """
    Check if activity category is in the allowlist.
    
    Args:
        category: Activity category name
    
    Returns:
        True if allowed, False otherwise
    """
    category_lower = category.lower()
    for allowed in ALLOWED_ACTIVITY_CATEGORIES:
        if allowed.lower() in category_lower:
            return True
    return False


def get_hotels(destination: str, limit: int = 5) -> list[dict]:
    """
    Fetch hotel data from RapidAPI Travel Advisor.
    
    Args:
        destination: Destination city/location name
        limit: Maximum number of hotels to return
    
    Returns:
        List of hotel dictionaries with name, rating, price, image, coordinates, address, ranking
    """
    # Check if we should use real API
    if not Config.USE_REAL_API or not Config.RAPIDAPI_KEY:
        print(f"[INFO] Using mock data for hotels in {destination}")
        return get_mock_hotels(destination, limit)
    
    url = "https://travel-advisor.p.rapidapi.com/locations/search"
    headers = {
        "X-RapidAPI-Key": Config.RAPIDAPI_KEY,
        "X-RapidAPI-Host": Config.RAPIDAPI_HOST
    }
    params = {
        "query": destination,
        "limit": 30,
        "offset": "0",
        "units": "km",
        "lang": "en_US"
    }
    
    print(f"[INFO] Fetching hotels for: {destination}")
    data = make_api_request(url, headers, params)
    
    if not data:
        print(f"[ERROR] API request failed for hotels, using mock data")
        return get_mock_hotels(destination, limit)
    
    # Parse response
    items = data.get("data", [])
    raw_count = len(items)
    print(f"[INFO] Received {raw_count} raw items from API")
    
    hotels = []
    center_lat = None
    center_lng = None
    
    # First pass: find center coordinates from first valid hotel
    for item in items:
        result_obj = item.get("result_object", {})
        if not result_obj:
            continue
        
        if not is_hotel_category(result_obj):
            continue
        
        lat = result_obj.get("latitude")
        lng = result_obj.get("longitude")
        
        if lat is not None and lng is not None:
            try:
                lat_float = float(lat)
                lng_float = float(lng)
                if -90 <= lat_float <= 90 and -180 <= lng_float <= 180:
                    center_lat = lat_float
                    center_lng = lng_float
                    break
            except (ValueError, TypeError):
                continue
    
    # Second pass: extract and filter hotels
    for item in items:
        result_obj = item.get("result_object", {})
        if not result_obj:
            continue
        
        # Filter by category
        if not is_hotel_category(result_obj):
            continue
        
        # Extract coordinates
        lat = result_obj.get("latitude")
        lng = result_obj.get("longitude")
        
        if lat is None or lng is None:
            continue
        
        try:
            lat_float = float(lat)
            lng_float = float(lng)
        except (ValueError, TypeError):
            continue
        
        # Validate coordinates
        if not (-90 <= lat_float <= 90 and -180 <= lng_float <= 180):
            continue
        
        # Geo-filtering: exclude hotels too far from center
        if center_lat is not None and center_lng is not None:
            if not within_radius(center_lat, center_lng, lat_float, lng_float, HOTEL_MAX_DISTANCE_KM):
                continue
        
        # Extract hotel data
        name = result_obj.get("name", "Unknown Hotel")
        if name == "Unknown Hotel":
            continue
        
        # Extract rating
        rating = result_obj.get("rating")
        if rating is not None:
            try:
                rating = float(rating)
            except (ValueError, TypeError):
                rating = "N/A"
        else:
            rating = "N/A"
        
        # Extract price and currency
        price, currency = extract_price(result_obj)
        
        # Extract image
        image = extract_image_url(result_obj)
        
        # Extract address
        address = result_obj.get("address", "Not available")
        if not address or address == "":
            address = "Not available"
        
        # Extract ranking
        ranking = result_obj.get("ranking_position")
        if ranking is not None:
            ranking = str(ranking)
        else:
            ranking = None
        
        hotel = {
            "name": name,
            "rating": rating,
            "price": price,
            "currency": currency,
            "image": image,
            "coordinates": {"lat": lat_float, "lng": lng_float},
            "address": address,
            "ranking": ranking
        }
        
        hotels.append(hotel)
        
        if len(hotels) >= limit:
            break
    
    print(f"[INFO] Returning {len(hotels)} hotels after filtering")
    return hotels if hotels else get_mock_hotels(destination, limit)


def get_activities(destination: str, limit: int = 5) -> list[dict]:
    """
    Fetch activity data from RapidAPI Travel Advisor.
    
    Args:
        destination: Destination city/location name
        limit: Maximum number of activities to return
    
    Returns:
        List of activity dictionaries with name, image, category, duration_minutes, price, currency, rating, coordinates, booking_link
    """
    # Check if we should use real API
    if not Config.USE_REAL_API or not Config.RAPIDAPI_KEY:
        print(f"[INFO] Using mock data for activities in {destination}")
        return get_mock_activities(destination, limit)
    
    url = "https://travel-advisor.p.rapidapi.com/locations/search"
    headers = {
        "X-RapidAPI-Key": Config.RAPIDAPI_KEY,
        "X-RapidAPI-Host": Config.RAPIDAPI_HOST
    }
    params = {
        "query": f"{destination} attractions",
        "limit": 30,
        "offset": "0",
        "units": "km",
        "lang": "en_US"
    }
    
    print(f"[INFO] Fetching activities for: {destination}")
    data = make_api_request(url, headers, params)
    
    if not data:
        print(f"[ERROR] API request failed for activities, using mock data")
        return get_mock_activities(destination, limit)
    
    # Parse response
    items = data.get("data", [])
    raw_count = len(items)
    print(f"[INFO] Received {raw_count} raw items from API")
    
    activities = []
    center_lat = None
    center_lng = None
    is_mountain = is_mountain_destination(destination)
    is_beach = is_beach_destination(destination)
    
    # First pass: find center coordinates from first valid activity
    for item in items:
        result_obj = item.get("result_object", {})
        if not result_obj:
            continue
        
        lat = result_obj.get("latitude")
        lng = result_obj.get("longitude")
        
        if lat is not None and lng is not None:
            try:
                lat_float = float(lat)
                lng_float = float(lng)
                if -90 <= lat_float <= 90 and -180 <= lng_float <= 180:
                    center_lat = lat_float
                    center_lng = lng_float
                    break
            except (ValueError, TypeError):
                continue
    
    # If no center from activities, try to get from hotels (fallback)
    if center_lat is None or center_lng is None:
        hotels = get_hotels(destination, 1)
        if hotels and hotels[0].get("coordinates"):
            coords = hotels[0]["coordinates"]
            center_lat = coords.get("lat")
            center_lng = coords.get("lng")
    
    # Second pass: extract and filter activities
    for item in items:
        result_obj = item.get("result_object", {})
        if not result_obj:
            continue
        
        # Extract coordinates
        lat = result_obj.get("latitude")
        lng = result_obj.get("longitude")
        
        if lat is None or lng is None:
            continue
        
        try:
            lat_float = float(lat)
            lng_float = float(lng)
        except (ValueError, TypeError):
            continue
        
        # Validate coordinates
        if not (-90 <= lat_float <= 90 and -180 <= lng_float <= 180):
            continue
        
        # Geo-filtering: exclude activities too far from center
        if center_lat is not None and center_lng is not None:
            if not within_radius(center_lat, center_lng, lat_float, lng_float, ACTIVITY_MAX_DISTANCE_KM):
                continue
        
        # Extract name
        name = result_obj.get("name", "Unknown Activity")
        if name == "Unknown Activity":
            continue
        
        # Extract category
        category_obj = result_obj.get("category", {})
        if isinstance(category_obj, dict):
            category = category_obj.get("name", "Attraction")
        else:
            category = str(category_obj) if category_obj else "Attraction"
        
        # Filter by category allowlist
        if not is_allowed_activity_category(category):
            continue
        
        # Destination-based filtering: exclude water activities for mountain destinations
        if is_mountain and is_water_activity(name, category):
            continue
        
        # Extract rating
        rating = result_obj.get("rating")
        if rating is not None:
            try:
                rating = float(rating)
            except (ValueError, TypeError):
                rating = "N/A"
        else:
            rating = "N/A"
        
        # Extract price and currency
        price, currency = extract_price(result_obj)
        if price == "Price unavailable":
            price = "Free"
        
        # Extract image
        image = extract_image_url(result_obj)
        
        # Extract duration (if available)
        duration_minutes = result_obj.get("duration_minutes")
        if duration_minutes is not None:
            try:
                duration_minutes = int(duration_minutes)
            except (ValueError, TypeError):
                duration_minutes = None
        else:
            duration_minutes = None
        
        # Extract booking link (if available)
        booking_link = result_obj.get("booking_link")
        if not booking_link:
            booking_link = result_obj.get("web_url")
        if not booking_link:
            booking_link = None
        
        activity = {
            "name": name,
            "image": image,
            "category": category,
            "duration_minutes": duration_minutes,
            "price": price,
            "currency": currency,
            "rating": rating,
            "coordinates": {"lat": lat_float, "lng": lng_float},
            "booking_link": booking_link
        }
        
        activities.append(activity)
        
        if len(activities) >= limit:
            break
    
    print(f"[INFO] Returning {len(activities)} activities after filtering")
    return activities if activities else get_mock_activities(destination, limit)


"""
Example Usage:

# In Python:
from services.tripadvisor_service import get_hotels, get_activities

# Get hotels
hotels = get_hotels("Goa", limit=5)
print(f"Found {len(hotels)} hotels")
for hotel in hotels:
    print(f"- {hotel['name']}: {hotel['rating']}, {hotel['price']}")

# Get activities
activities = get_activities("Goa", limit=5)
print(f"Found {len(activities)} activities")
for activity in activities:
    print(f"- {activity['name']}: {activity['category']}, {activity['price']}")

# Example output shape for hotels:
# [
#     {
#         "name": "Paradise Beach Resort",
#         "rating": 4.5,
#         "price": "₹6,000",
#         "currency": "INR",
#         "image": "https://...",
#         "coordinates": {"lat": 15.2993, "lng": 74.1240},
#         "address": "Beach Road, North Goa",
#         "ranking": "1"
#     },
#     ...
# ]

# Example output shape for activities:
# [
#     {
#         "name": "Scuba Diving Adventure",
#         "image": "https://...",
#         "category": "Water Sports",
#         "duration_minutes": 120,
#         "price": "₹3,500",
#         "currency": "INR",
#         "rating": 4.6,
#         "coordinates": {"lat": 15.2993, "lng": 74.1240},
#         "booking_link": "https://..."
#     },
#     ...
# ]


# Testing via curl (assuming Flask routes are set up):

# Get hotels:
# curl -X GET "http://localhost:5000/api/hotels?destination=Goa&limit=5"

# Get activities:
# curl -X GET "http://localhost:5000/api/activities?destination=Goa&limit=5"
"""
