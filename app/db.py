from pymongo import MongoClient
from app.config import MONGO_URI
import certifi 
import ssl

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=True,
    ssl_cert_reqs=ssl.CERT_NONE
)

db = client["gps_tracker"]

users = db["users"]

# index for performance
users.create_index("device_id", unique=True)