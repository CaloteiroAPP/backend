import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
load_dotenv(".env")

# Retrieve the MongoDB Atlas components from environment variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB_PARAMS = os.getenv("MONGO_DB_PARAMS")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Construct the MongoDB Atlas URI
MONGO_ATLAS_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{MONGO_DB_PARAMS}"

# Create a new client and connect to the MongoDB Atlas server
client = MongoClient(MONGO_ATLAS_URI, server_api=ServerApi('1'))

# Attempt to ping the MongoDB Atlas cluster to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"An error occurred: {e}")

# Access the specified database and collection
db = client[DATABASE_NAME]


# Function to ensure the connection and availability of the database and collection
def ensure_db_and_collection():
    if client is not None:
        print("Connected to MongoDB Atlas")
    else:
        print("Could not connect to MongoDB Atlas")
