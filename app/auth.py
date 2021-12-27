import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CMC_KEY = os.getenv('CMC_KEY')
WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")