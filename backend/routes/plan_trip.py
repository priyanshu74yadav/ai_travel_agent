"""
Plan trip route handler.
Combines hotels, activities, and AI-generated summary for a complete trip plan.
"""

from flask import Blueprint, jsonify, request
from services.tripadvisor_service import get_hotels, get_activities
from services.openai_service import generate_ai_summary
from utils.helpers import log_request

bp = Blueprint("plan_trip", __name__)


@bp.route("/plan_trip", methods=["POST"])
def plan_trip():
    """
    POST /plan_trip endpoint.
    Creates a complete trip plan with hotels, activities, and AI-generated summary.
    
    Request Body (JSON):
        {
            "destination": "Goa",
            "budget": 20000,
            "limit": 5  # Optional, default: 5
        }
    
    Returns:
        JSON response with destination, budget, hotels, activities, and AI summary.
    """
    log_request(request)
    
    # Get request data
    data = request.get_json()
    
    # Validate required parameters
    if not data:
        return jsonify({"error": "Missing request body"}), 400
    
    destination = data.get("destination")
    budget = data.get("budget")
    limit = data.get("limit", 5)
    
    if not destination:
        return jsonify({"error": "Missing destination parameter"}), 400
    
    if budget is None:
        return jsonify({"error": "Missing budget parameter"}), 400
    
    try:
        # Fetch hotels and activities
        hotels_data = get_hotels(destination, limit=limit)
        activities_data = get_activities(destination, limit=limit)
        
        # Generate AI summary
        summary = generate_ai_summary(
            destination=destination,
            budget=budget,
            hotels=hotels_data,
            activities=activities_data
        )
        
        # Return complete trip plan
        return jsonify({
            "destination": destination,
            "budget": budget,
            "hotels": hotels_data,
            "activities": activities_data,
            "summary": summary
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to plan trip: {str(e)}"}), 500


# Example curl commands:
# curl -X POST http://127.0.0.1:5000/plan_trip \
#   -H "Content-Type: application/json" \
#   -d '{"destination": "Goa", "budget": 20000}'
#
# curl -X POST http://127.0.0.1:5000/plan_trip \
#   -H "Content-Type: application/json" \
#   -d '{"destination": "Goa", "budget": 20000, "limit": 5}'

