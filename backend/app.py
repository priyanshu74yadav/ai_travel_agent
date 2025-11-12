"""
Main Flask application entry point for AI Travel Agent Backend.
Initializes Flask app, enables CORS, and registers all routes.
"""

import os
from flask import Flask
from flask_cors import CORS
from config.settings import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for Next.js frontend
CORS(app)

# Import and register routes
from routes import health, hotels, activities, plan_trip

# Register blueprints
app.register_blueprint(health.bp)
app.register_blueprint(hotels.bp)
app.register_blueprint(activities.bp)
app.register_blueprint(plan_trip.bp)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

