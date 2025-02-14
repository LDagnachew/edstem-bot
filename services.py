from config import API_KEY, BASE_URL, COURSE_ID
from models.threads import Thread
import requests
# File Used For All Basic Access to Ed (Decline Post)

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def decline_thread(thread=Thread):
	post_decline_comment(thread=thread)
	block_thread(thread=thread)
	
def block_thread(thread=Thread):
	url = f"{BASE_URL}/courses/{COURSE_ID}/threads/{thread.id}"

	data = {
		"approved_status": "rejected",
		"is_locked": True
	}

	response = requests.patch(url, json=data, headers=HEADERS)
	if response.status_code == 201:
		print(f"✅ Rejection comment posted for thread {thread.id}")
	else:
		print(f"❌ Failed to post rejection comment: {response.status_code}, {response.text}")



def post_decline_comment(thread=Thread):
	url = f"{BASE_URL}/courses/{COURSE_ID}/threads/{thread.id}/comments"
	
	message = "This is a duplicate question. Please search for your question before making a post."
	data = {
        "content": message,
        "kind": "thread_rejection"  # Marks this as an official rejection message
    }

	response = requests.post(url, json=data, headers=HEADERS)
	if response.status_code == 201:
		print(f"✅ Rejection comment posted for thread {thread.id}")
	else:
		print(f"❌ Failed to post rejection comment: {response.status_code}, {response.text}")
