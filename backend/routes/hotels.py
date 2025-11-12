"""
Hotels route handler.
Fetches hotel data for a given destination.
"""

from flask import Blueprint, jsonify, request
from services.tripadvisor_service import get_hotels
from utils.helpers import log_request

bp = Blueprint("hotels", __name__)


@bp.route("/hotels", methods=["GET"])
def hotels():
    """
    GET /hotels endpoint.
    Fetches hotels for a given destination.
    
    Query Parameters:
        destination (str): Required. The destination city/location.
        limit (int): Optional. Maximum number of hotels to return (default: 5).
    
    Returns:
        JSON response with list of hotels or error message.
    """
    log_request(request)
    
    # Get query parameters
    destination = request.args.get("destination")
    limit = request.args.get("limit", 5, type=int)
    
    # Validate required parameters
    if not destination:
        return jsonify({"error": "Missing destination parameter"}), 400
    
    try:
        # Fetch hotels from service
        hotels_data = get_hotels(destination, limit=limit)
        return jsonify(hotels_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch hotels: {str(e)}"}), 500


# Example curl command:
# curl "http://127.0.0.1:5000/hotels?destination=Goa&limit=5"

