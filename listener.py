import asyncio
import json
import aiohttp
import websockets
import requests
from config import BASE_URL, API_KEY, COURSE_ID

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WS_URL = "wss://us.edstem.org/api/stream"

async def fetch_latest_thread(thread_id):
    res_url = f"{BASE_URL}/threads/{thread_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(res_url, headers=HEADERS) as response:
            if response.status == 200:
                thread = await response.json()
                print(f"New Post! {thread.get('thread', {}).get('title', 'Untitled')} (ID: {thread_id})")
            else:
                print(f"Failed to fetch thread {thread_id}, status: {response.status}")


async def listen_for_threads():
    attempt = 0
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                """ Establish the WS Connection using AIOHTTP (WebSocket library
					does not do a good job with appending the headers)
                """
                async with session.ws_connect(WS_URL, headers=HEADERS, heartbeat=60) as ws:
                    
                    print("Connected to EdStem WebSocket!")
                    
                    subscribe_msg = json.dumps({
                        "type": "course.subscribe",
                        "oid": COURSE_ID,
                    })
                    await ws.send_str(subscribe_msg)
                    print(f"Subscribed to course {COURSE_ID}, listening for updates...")
                    async for message in ws:
                        if message.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(message.data)
                            if data.get("type") == "thread.new":
                                thread_id = data["data"]["thread"]["id"]
                                print(f"New Thread! Thread ID: {thread_id}")
                                await fetch_latest_thread(thread_id)
                        elif message.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED):
                            print("WebSocket closed, attempting to reconnect...")
                            break
                    
        except aiohttp.ClientError as e:
            print(f"WebSocket error: {e}. Retrying in {2 ** attempt} seconds...")
            await asyncio.sleep(2 ** attempt)
            attempt = min(attempt + 1, 6)  # Exponential backoff with max delay
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying...")
            await asyncio.sleep(1000)    
