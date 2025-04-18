from config import API_KEY, BASE_URL, COURSE_ID
from models.threads import Thread
import requests

# File Used For All Basic Access to Ed (Decline Post)
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def decline_thread(thread=Thread):
	post_decline_comment(thread=thread)
	block_thread(thread=thread)

def mark_duplicate(thread=Thread, dup_thread=Thread):
	post_decline_comment(thread=thread)
	mark_thread_duplicate(thread=thread, dup_thread=dup_thread)

	
def block_thread(thread=Thread):
	url = f"{BASE_URL}/threads/{thread.id}/reject"

	response = requests.post(url, headers=HEADERS)
	if response.status_code == 201:
		print(f"✅ Rejection comment posted for thread {thread.id}")
	else:
		print(f"❌ Failed to post rejection comment: {response.status_code}, {response.text}")

def mark_thread_duplicate(thread=Thread, dup_thread=Thread):
	url = f"{BASE_URL}/threads/{thread.id}/mark_duplicate"

	data = {
		"duplicate_id": dup_thread.id
	}
	response = requests.post(url, json=data, headers=HEADERS)
	if response.status_code == 201:
		print(f"✅ Successfully Marked Thread {thread.id} as Duplicate!")
	else:
		print(f"❌ Failed to Mark Thread as Duplicate: {response.status_code}, {response.text}")
	

def post_decline_comment(thread=Thread):
	url = f"{BASE_URL}/threads/{thread.id}/comments"
	
	message = "This is a duplicate question. Please search for your question before making a post."
	data = {
        "comment": {
			"type": "comment",
			"kind": "thread_rejection",
			"content": f"<document version=\"2.0\"><paragraph>{message}</paragraph></document>",
			"is_private": False,
			"is_anonymous": True
    	}  # Marks this as an official rejection message
    }

	response = requests.post(url, json=data, headers=HEADERS)
	if response.status_code == 201:
		print(f"✅ Rejection comment posted for thread {thread.id}")
	else:
		print(f"❌ Failed to post rejection comment: {response.status_code}, {response.text}")

def post_mark_review_comment(thread=Thread):
	url = f"{BASE_URL}/threads/{thread.id}/comments"

	message = "<mention id=\"950432\">Leul Dagnachew</mention> Please Review This Post!"
	data = {
        "comment": {
			"type": "comment",
			"kind": "comment",
			"content": f"<document version=\"2.0\"><paragraph>{message}</paragraph></document>",
			"is_private": False,
			"is_anonymous": True
    	}  
    }

	response = requests.post(url, json=data, headers=HEADERS)
	if response.status_code == 201:
		print(f"✅ Review comment posted for thread {thread.id}")
	else:
		print(f"❌ Failed to post review comment: {response.status_code}, {response.text}")