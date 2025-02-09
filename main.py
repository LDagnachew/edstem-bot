from flask import Flask, request
from dotenv import load_dotenv
import asyncio
from listener import main


if __name__ == "__main__":
	asyncio.run(main())