import asyncio
import json
import aiohttp
from services import decline_thread, mark_duplicate, post_mark_review_comment
from models.threads import Thread, find_duplicate_thread, declined_threads_id
from datetime import datetime
from models.user import User
from config import BASE_URL, API_KEY, COURSE_ID, WS_URL

# Include `_token` in WebSocket URL if required

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


async def listen_for_events():
    """Test WebSocket connection, verify subscription, and print ALL events."""
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(WS_URL, headers=HEADERS, heartbeat=60) as ws:
                    
                    print("✅ Connected to EdStem WebSocket!")

                    # Ensure WebSocket is open before subscribing
                    if ws.closed:
                        print("❌ WebSocket closed unexpectedly. Reconnecting...")
                        continue  

                    # Send subscription message (ensure it matches Chrome's)
                    subscribe_msg = json.dumps({"type": "course.subscribe", "oid": COURSE_ID})
                    print(f"📌 Sending Subscription Request: {subscribe_msg}")
                    await ws.send_str(subscribe_msg)
                    print(f"✅ Subscription message sent successfully!")

                    # Wait for subscription confirmation
                    subscription_verified = False
                    async for message in ws:
                        if message.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(message.data)

                            # Log every received event
                            print(f"📩 WebSocket Event: {json.dumps(data, indent=4)}")

                            # Verify subscription response
                            if data.get("type") == "course.subscribe":
                                print("✅ Subscription Confirmed!")
                                subscription_verified = True
                                break  # Stop checking once verified

                    if not subscription_verified:
                        print("⚠️ Subscription not confirmed. Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                        continue  # Restart loop to retry subscription

                    # Listen for all messages
                    async for message in ws:
                        if message.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(message.data)
                            print(f"📩 WebSocket Event: {json.dumps(data, indent=4)}")

                            # Log detected event type
                            event_type = data.get("type")
                            print(f"🔍 Detected Event Type: {event_type}")
                            # TODO: Pass JSON into event_handler
                            await event_handler(data)

                        elif message.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED):
                            print("🔄 WebSocket closed. Reconnecting...")
                            break  # Exit loop to trigger reconnect

        except aiohttp.WSServerHandshakeError as e:
            if e.status == 401:
                print("❌ Authentication failed. Check your API token.")
                return
            elif e.status == 403:
                print("❌ Missing permissions. You may need instructor/TA access.")
                return
            else:
                print(f"⚠️ WebSocket handshake failed with status {e.status}. Retrying...")
            await asyncio.sleep(5)

        except aiohttp.ClientError as e:
            print(f"⚠️ WebSocket error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)


# Handles All Events At Once
async def event_handler(data):
    type = data.get("type")
    if(type == "thread.new"):
        thread_data = data["data"]["thread"]
        # Convert datetime fields
        if thread_data.get("created_at"):
            thread_data["created_at"] = datetime.fromisoformat(thread_data["created_at"])
        if thread_data.get("updated_at"):
            thread_data["updated_at"] = datetime.fromisoformat(thread_data["updated_at"])
        # Convert user field if necessary
        if "user" in thread_data and thread_data["user"]:
            thread_data["user"] = User(**thread_data["user"])
        thread = Thread(**thread_data)

        # With this, now we check for correct formatting. (For Now Restrict to Exam Questions)
        # TODO: DO NOT DECLINE PROFESSORS/INSTRUCTOR POSTS LOL (will add after testing)
        if thread.category == "Exams" and thread.id not in declined_threads_id:
            dup_thread = find_duplicate_thread(thread)
            if isinstance(dup_thread, dict) and dup_thread.get("requires_review"):
                post_mark_review_comment(dup_thread["thread"])
            if dup_thread is not None and isinstance(dup_thread, Thread) and not dup_thread.is_private:
                mark_duplicate(thread=thread, dup_thread=dup_thread)
                declined_threads_id.insert(thread.id)
                print("✅ Successfully Declined Duplicate Thead!")
        
    
async def main():
    await listen_for_events()  # Start WebSocket listener
    
