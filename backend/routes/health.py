"""
Health check route for monitoring API status.
"""

from flask import Blueprint, jsonify

bp = Blueprint("health", __name__)


@bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    Returns API status for monitoring.
    
    Returns:
        JSON response with status "ok"
    """
    return jsonify({"status": "ok"}), 200

