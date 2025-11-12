"""
TripAdvisor/RapidAPI service for fetching hotels and activities data.
Falls back to mock data if API keys are missing or API calls fail.
"""

import requests
from config.settings import Config
from services.mock_data import get_mock_hotels, get_mock_activities


def get_hotels(destination, limit=5):
    """
    Fetches hotel data from RapidAPI Travel Advisor or returns mock data.
    
    Args:
        destination (str): Destination city/location name
        limit (int): Maximum number of hotels to return
    
    Returns:
        list: List of hotel dictionaries with name, rating, price, image, coordinates
    """
    # Check if we should use real API
    if not Config.USE_REAL_API or not Config.RAPIDAPI_KEY:
        print(f"[INFO] Using mock data for hotels in {destination}")
        return get_mock_hotels(destination, limit)
    
    try:
        # RapidAPI Travel Advisor endpoint for location search
        url = "https://travel-advisor.p.rapidapi.com/locations/search"
        
        headers = {
            "X-RapidAPI-Key": Config.RAPIDAPI_KEY,
            "X-RapidAPI-Host": Config.RAPIDAPI_HOST
        }
        
        params = {
            "query": destination,
            "limit": limit,
            "offset": "0",
            "units": "km",
            "currency": "INR",
            "sort": "relevance",
            "lang": "en_US"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            hotels = []
            
            # Parse the response (structure may vary based on API)
            locations = data.get("data", [])
            
            for location in locations[:limit]:
                # Extract hotel information
                hotel = {
                    "name": location.get("result_object", {}).get("name", "Unknown Hotel"),
                    "rating": float(location.get("result_object", {}).get("rating", 0)),
                    "price": f"₹{location.get('result_object', {}).get('price_level', 0) * 1000}",
                    "currency": "INR",
                    "image": location.get("result_object", {}).get("photo", {}).get("images", {}).get("medium", {}).get("url", ""),
                    "coordinates": {
                        "lat": float(location.get("result_object", {}).get("latitude", 0)),
                        "lng": float(location.get("result_object", {}).get("longitude", 0))
                    },
                    "address": location.get("result_object", {}).get("address", "")
                }
                
                if hotel["name"] != "Unknown Hotel":
                    hotels.append(hotel)
            
            if hotels:
                return hotels
            else:
                print(f"[WARNING] No hotels found from API, using mock data")
                return get_mock_hotels(destination, limit)
        else:
            print(f"[WARNING] API returned status {response.status_code}, using mock data")
            return get_mock_hotels(destination, limit)
            
    except Exception as e:
        print(f"[ERROR] Failed to fetch hotels from API: {str(e)}")
        print(f"[INFO] Falling back to mock data")
        return get_mock_hotels(destination, limit)


def get_activities(destination, limit=5):
    """
    Fetches activity/adventure data from RapidAPI Travel Advisor or returns mock data.
    
    Args:
        destination (str): Destination city/location name
        limit (int): Maximum number of activities to return
    
    Returns:
        list: List of activity dictionaries with name, rating, category, image, coordinates
    """
    # Check if we should use real API
    if not Config.USE_REAL_API or not Config.RAPIDAPI_KEY:
        print(f"[INFO] Using mock data for activities in {destination}")
        return get_mock_activities(destination, limit)
    
    try:
        # RapidAPI Travel Advisor endpoint for attractions search
        url = "https://travel-advisor.p.rapidapi.com/attractions/search"
        
        headers = {
            "X-RapidAPI-Key": Config.RAPIDAPI_KEY,
            "X-RapidAPI-Host": Config.RAPIDAPI_HOST
        }
        
        params = {
            "query": f"{destination} attractions",
            "limit": limit,
            "offset": "0",
            "units": "km",
            "currency": "INR",
            "sort": "relevance",
            "lang": "en_US"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            activities = []
            
            # Parse the response
            attractions = data.get("data", [])
            
            for attraction in attractions[:limit]:
                # Extract activity information
                activity = {
                    "name": attraction.get("name", "Unknown Activity"),
                    "rating": float(attraction.get("rating", 0)),
                    "category": attraction.get("category", {}).get("name", "Adventure"),
                    "image": attraction.get("photo", {}).get("images", {}).get("medium", {}).get("url", ""),
                    "coordinates": {
                        "lat": float(attraction.get("latitude", 0)),
                        "lng": float(attraction.get("longitude", 0))
                    },
                    "price": f"₹{attraction.get('price_level', 0) * 500}"
                }
                
                if activity["name"] != "Unknown Activity":
                    activities.append(activity)
            
            if activities:
                return activities
            else:
                print(f"[WARNING] No activities found from API, using mock data")
                return get_mock_activities(destination, limit)
        else:
            print(f"[WARNING] API returned status {response.status_code}, using mock data")
            return get_mock_activities(destination, limit)
            
    except Exception as e:
        print(f"[ERROR] Failed to fetch activities from API: {str(e)}")
        print(f"[INFO] Falling back to mock data")
        return get_mock_activities(destination, limit)

