import json
from models.threads import Thread
from datetime import datetime
from models.user import User

def test_json_load(file):
    try:
        with open(file, 'r') as f:
            json_data = json.load(f)
        return json_data
    except FileNotFoundError:
        print(f"File {file} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {file}.")
        return None

def attempt_thread_obj(thread_data):
    if thread_data.get("created_at"):
        thread_data["created_at"] = datetime.fromisoformat(thread_data["created_at"])
    if thread_data.get("updated_at"):
        thread_data["updated_at"] = datetime.fromisoformat(thread_data["updated_at"])
    threadobj = Thread(**thread_data)
    return threadobj
        

if __name__ == "__main__":
    data = test_json_load("out.json")
    if data:
        threadobj = attempt_thread_obj(data)
        print(json.dumps(threadobj, default=str, indent=4))
        