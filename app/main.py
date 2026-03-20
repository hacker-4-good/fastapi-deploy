from fastapi import FastAPI
from datetime import datetime
from app.db import users
from app.geofence import is_inside
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/location")
def update_location(data: dict):
    device_id = data["device_id"]

    now = datetime.now()
    date = now.strftime("%d-%m-%Y")

    lat = data["lat"]
    lon = data["lon"]

    inside = is_inside(lat, lon)

    update = {
        "name": data["name"],
        "phone": data["phone"],
        "last_location": f"({lat:.5f},{lon:.5f})",
        "last_seen": now,
        "status": "INSIDE" if inside else "OUTSIDE"
    }

    if inside:
        users.update_one(
            {"device_id": device_id},
            {
                "$set": update,
                "$inc": {f"attendance.{date}": 1}
            },
            upsert=True
        )
    else:
        users.update_one(
            {"device_id": device_id},
            {"$set": update},
            upsert=True
        )

    return {"inside": inside}