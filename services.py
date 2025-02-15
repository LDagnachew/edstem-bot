from config import API_KEY, BASE_URL, COURSE_ID
from models.threads import Thread
import requests
# File Used For All Basic Access to Ed (Decline Post)

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def decline_thread(thread=Thread):
	post_decline_comment(thread=thread)
	block_thread(thread=thread)

	
def block_thread(thread=Thread):
	url = f"{BASE_URL}/threads/{thread.id}/reject"

	print(f"THE URL WE ARAE USING IS: {url}")
	response = requests.post(url, headers=HEADERS)
	if response.status_code == 201:
		print(f"✅ Rejection comment posted for thread {thread.id}")
	else:
		print(f"❌ Failed to post rejection comment: {response.status_code}, {response.text}")



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
