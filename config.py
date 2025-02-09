import os
from dotenv import load_dotenv

# Load URLs
BASE_URL = "https://us.edstem.org/api"


# Load Dotenv Constants
load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")
COURSE_ID = int(os.getenv("COURSE_ID"))
