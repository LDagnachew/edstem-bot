from flask import Flask, request
from dotenv import load_dotenv
from services import services_bp
import asyncio
from listener import main


app = Flask(__name__)
app.register_blueprint(services_bp)

if __name__ == "__main__":
	asyncio.run(main())