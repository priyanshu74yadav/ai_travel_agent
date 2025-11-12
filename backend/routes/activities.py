"""
Activities route handler.
Fetches activity/adventure data for a given destination.
"""

from flask import Blueprint, jsonify, request
from services.tripadvisor_service import get_activities
from utils.helpers import log_request

bp = Blueprint("activities", __name__)


@bp.route("/activities", methods=["GET"])
def activities():
    """
    GET /activities endpoint.
    Fetches activities/adventures for a given destination.
    
    Query Parameters:
        destination (str): Required. The destination city/location.
        limit (int): Optional. Maximum number of activities to return (default: 5).
    
    Returns:
        JSON response with list of activities or error message.
    """
    log_request(request)
    
    # Get query parameters
    destination = request.args.get("destination")
    limit = request.args.get("limit", 5, type=int)
    
    # Validate required parameters
    if not destination:
        return jsonify({"error": "Missing destination parameter"}), 400
    
    try:
        # Fetch activities from service
        activities_data = get_activities(destination, limit=limit)
        return jsonify(activities_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch activities: {str(e)}"}), 500


# Example curl command:
# curl "http://127.0.0.1:5000/activities?destination=Goa&limit=5"

