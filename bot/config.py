import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

if API_KEY is None:
    raise ValueError('Please set API_KEY in .env file')
elif API_SECRET is None:
    raise ValueError('Please set API_SECRET in .env file')
else:
    print('env variables loaded successfully')