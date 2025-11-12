"""
Helper utility functions for the application.
"""


def log_request(request):
    """
    Logs incoming request details to the console.
    
    Args:
        request: Flask request object
    """
    print(f"[REQUEST] {request.method} {request.path}")
    if request.args:
        print(f"[QUERY PARAMS] {dict(request.args)}")
    if request.is_json and request.get_json():
        print(f"[BODY] {request.get_json()}")


def format_json_response(data, status_code=200):
    """
    Helper function to format JSON responses consistently.
    
    Args:
        data: Data to be returned in JSON format
        status_code (int): HTTP status code
    
    Returns:
        tuple: (JSON response, status code)
    """
    from flask import jsonify
    return jsonify(data), status_code

