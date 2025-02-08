from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from config import BASE_URL, API_KEY, COURSE_ID
import requests
import os

# Create a Blueprint for the routes
services_bp = Blueprint("services", __name__)
load_dotenv()

# Initialize Constants

# Used for Testing Purposes, ensures that Bot is running.
@services_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "Bot is running"})


# Fetch Posts (limited to fixed size, TODO: need to expand on this)
@services_bp.route("/fetch_posts", methods=["POST"])
def fetch_posts():
    if not COURSE_ID:
        return jsonify({"error": "Missing course_id"}), 400

    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{BASE_URL}/courses/{COURSE_ID}/threads"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@services_bp.route("/fetch_top", methods=["POST"])
def fetch_top():
    params = {
        "sort_key": request.args.get("sort_key", "id"),  # Default: id
        "order": request.args.get("order", "desc"),  # Default: descending
        "limit": request.args.get("limit", 50)  # Optional: Limit results
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{BASE_URL}/courses/{COURSE_ID}/threads"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return jsonify(response.json())
