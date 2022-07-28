import logging
import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get('DEBUG', 'False').lower() != 'False'.lower()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

SUPER_ADMIN_ID = int(os.environ.get('SUPER_ADMIN_ID', 0))
