from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('TOMTOM_API_KEY')

if api_key:
    print(f"API Key loaded: {api_key[:10]}...{api_key[-4:]}")
    print(" .env file is working!")
else:
    print("API Key NOT found! Check your .env file")