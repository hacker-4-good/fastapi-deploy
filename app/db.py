from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client["gps_tracker"]

users = db["users"]

# index for performance
users.create_index("device_id", unique=True)