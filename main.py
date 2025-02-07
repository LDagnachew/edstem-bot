from flask import Flask, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

@app.route("/ping", methods=["GET"])
def ping():
	return {"status": "Bot is running!"}

@app.route("/fetch_posts",methods=["POST"])
def fetch_posts():
	course_id = os.getenv("COURSE_ID")
	response = requests.get(f"https://us.edstem.org/api/courses/{course_id}/threads", headers={"Authorization": f"Bearer {API_KEY}"})
	return response.json()

if __name__ == "__main__":
	app.run(debug=True)
