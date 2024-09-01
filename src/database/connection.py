import logging
import os
from dotenv import load_dotenv
from pymongo import ASCENDING
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv(".env")

# Retrieve the MongoDB Atlas components from environment variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB_PARAMS = os.getenv("MONGO_DB_PARAMS")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Construct the MongoDB Atlas URI
MONGO_ATLAS_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{MONGO_DB_PARAMS}"

# Create a new client and connect to the MongoDB Atlas server
client = MongoClient(MONGO_ATLAS_URI, server_api=ServerApi('1'))

# Attempt to ping the MongoDB Atlas cluster to confirm a successful connection
try:
    client.admin.command('ping')
    logger.info("Pinged your deployment. You successfully connected to MongoDB Atlas!")
except Exception as e:
    logger.error(f"An error occurred: {e}")

# Access the specified database and collection
db = client[DATABASE_NAME]

# Configure some database essentials
db["user"].create_index([("id", ASCENDING)], unique=True)
db["user"].create_index([("email", ASCENDING)], unique=True)

# Function to ensure the connection and availability of the database and collection
def ensure_db_and_collection():
    if client is not None:
        logger.info("Connected to MongoDB Atlas")
    else:
        logger.warning("Could not connect to MongoDB Atlas")

ensure_db_and_collection()
