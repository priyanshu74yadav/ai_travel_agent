"""
OpenAI service for generating AI-powered travel summaries and itineraries.
"""

from openai import OpenAI
from config.settings import Config


def generate_ai_summary(destination, budget, hotels, activities):
    """
    Generates an AI-powered travel summary and itinerary using OpenAI GPT.
    
    Args:
        destination (str): Destination name
        budget (int): Travel budget in local currency
        hotels (list): List of hotel dictionaries
        activities (list): List of activity dictionaries
    
    Returns:
        str: AI-generated travel summary and itinerary
    """
    # Check if OpenAI API key is available
    if not Config.OPENAI_API_KEY:
        print("[WARNING] OpenAI API key not found, returning default summary")
        return _get_default_summary(destination, budget, hotels, activities)
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Format hotels and activities for the prompt
        hotels_text = "\n".join([
            f"- {h.get('name', 'Unknown')} (Rating: {h.get('rating', 0)}/5, Price: {h.get('price', 'N/A')})"
            for h in hotels[:3]
        ])
        
        activities_text = "\n".join([
            f"- {a.get('name', 'Unknown')} (Rating: {a.get('rating', 0)}/5, Category: {a.get('category', 'Adventure')})"
            for a in activities[:3]
        ])
        
        # Create the prompt
        prompt = f"""You are a helpful travel planner AI.
Based on this data, create a short travel summary for {destination} under a budget of ₹{budget}.
Mention 2-3 top hotels and 2-3 interesting activities.
Then suggest a 3-day itinerary in bullet points.
Keep the response under 150 words.

Hotels:
{hotels_text}

Activities:
{activities_text}

Provide a concise, engaging summary with a 3-day itinerary."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert travel planner AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"[ERROR] Failed to generate AI summary: {str(e)}")
        print("[INFO] Returning default summary")
        return _get_default_summary(destination, budget, hotels, activities)


def _get_default_summary(destination, budget, hotels, activities):
    """
    Returns a default summary when OpenAI API is unavailable.
    
    Args:
        destination (str): Destination name
        budget (int): Travel budget
        hotels (list): List of hotels
        activities (list): List of activities
    
    Returns:
        str: Default travel summary
    """
    top_hotels = hotels[:2] if hotels else []
    top_activities = activities[:2] if activities else []
    
    summary = f"Welcome to {destination}! With a budget of ₹{budget}, you can enjoy a wonderful trip. "
    
    if top_hotels:
        summary += f"Top hotel recommendations include {top_hotels[0].get('name', 'various accommodations')}"
        if len(top_hotels) > 1:
            summary += f" and {top_hotels[1].get('name', 'others')}. "
        else:
            summary += ". "
    
    if top_activities:
        summary += f"Don't miss exciting activities like {top_activities[0].get('name', 'local adventures')}"
        if len(top_activities) > 1:
            summary += f" and {top_activities[1].get('name', 'more experiences')}. "
        else:
            summary += ". "
    
    summary += "\n\n3-Day Itinerary:\n"
    summary += "• Day 1: Arrival, check-in, and explore local markets\n"
    summary += "• Day 2: Visit top attractions and enjoy water activities\n"
    summary += "• Day 3: Cultural experiences and departure\n"
    summary += "\nTravel Tip: Book accommodations in advance during peak season for better rates!"
    
    return summary

