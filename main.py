from flask import Flask, request
from dotenv import load_dotenv
from services import services_bp
import asyncio
from listener import listen_for_threads


app = Flask(__name__)
app.register_blueprint(services_bp)

if __name__ == "__main__":
	asyncio.run(listen_for_threads())