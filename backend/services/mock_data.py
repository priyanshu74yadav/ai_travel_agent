"""
Mock data service for fallback when API keys are missing or API calls fail.
Provides sample hotel and activity data for testing.
"""


def get_mock_hotels(destination, limit=5):
    """
    Returns mock hotel data for a given destination.
    
    Args:
        destination (str): Destination name
        limit (int): Maximum number of hotels to return
    
    Returns:
        list: List of hotel dictionaries
    """
    mock_hotels = [
        {
            "name": "Paradise Beach Resort",
            "rating": 4.5,
            "price": "₹6,000",
            "currency": "INR",
            "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "coordinates": {"lat": 15.2993, "lng": 74.1240},
            "address": "Beach Road, North Goa"
        },
        {
            "name": "Sunset Luxury Hotel",
            "rating": 4.8,
            "price": "₹8,500",
            "currency": "INR",
            "image": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800",
            "coordinates": {"lat": 15.4909, "lng": 73.8278},
            "address": "Calangute, Goa"
        },
        {
            "name": "Ocean View Boutique",
            "rating": 4.3,
            "price": "₹5,200",
            "currency": "INR",
            "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
            "coordinates": {"lat": 15.5519, "lng": 73.7554},
            "address": "Baga Beach, Goa"
        },
        {
            "name": "Tropical Garden Resort",
            "rating": 4.2,
            "price": "₹4,800",
            "currency": "INR",
            "image": "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800",
            "coordinates": {"lat": 15.5832, "lng": 73.7414},
            "address": "Anjuna, Goa"
        },
        {
            "name": "Grand Heritage Palace",
            "rating": 4.7,
            "price": "₹12,000",
            "currency": "INR",
            "image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800",
            "coordinates": {"lat": 15.4989, "lng": 73.9128},
            "address": "Panaji, Goa"
        }
    ]
    
    return mock_hotels[:limit]


def get_mock_activities(destination, limit=5):
    """
    Returns mock activity data for a given destination.
    
    Args:
        destination (str): Destination name
        limit (int): Maximum number of activities to return
    
    Returns:
        list: List of activity dictionaries
    """
    mock_activities = [
        {
            "name": "Scuba Diving Adventure",
            "rating": 4.6,
            "category": "Water Sports",
            "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
            "coordinates": {"lat": 15.2993, "lng": 74.1240},
            "price": "₹3,500"
        },
        {
            "name": "Sunset Cruise",
            "rating": 4.8,
            "category": "Boat Tour",
            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
            "coordinates": {"lat": 15.4909, "lng": 73.8278},
            "price": "₹2,000"
        },
        {
            "name": "Spice Plantation Tour",
            "rating": 4.4,
            "category": "Cultural Experience",
            "image": "https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=800",
            "coordinates": {"lat": 15.5519, "lng": 73.7554},
            "price": "₹1,500"
        },
        {
            "name": "Parasailing Experience",
            "rating": 4.7,
            "category": "Adventure Sports",
            "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
            "coordinates": {"lat": 15.5832, "lng": 73.7414},
            "price": "₹2,500"
        },
        {
            "name": "Dolphin Watching Tour",
            "rating": 4.5,
            "category": "Wildlife",
            "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",
            "coordinates": {"lat": 15.4989, "lng": 73.9128},
            "price": "₹1,800"
        }
    ]
    
    return mock_activities[:limit]

