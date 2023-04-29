from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, firestore, initialize_app
from urllib.parse import unquote
import pygeohash as pgh

# Initialize Firebase app
cred = credentials.Certificate("./service_account.json")
initialize_app(cred)
db = firestore.client()

app = FastAPI()


def get_venues_handler(resp):
    if len(resp) == 0:
        raise HTTPException(status_code=404, detail="No venues found")
    else:
        return {'venues': resp}


def search_name(name):
    name = unquote(name)
    venues = db.collection('venues').get()

    resp = [venue.to_dict() for venue in venues if name.lower()
            in venue.to_dict()['name'].lower()]

    # sort the venues by name in ascending order
    resp.sort(key=lambda x: x['name'])

    return get_venues_handler(resp)


def search_rating(rating):
    venues_ref = db.collection('venues')
    venues = venues_ref.where('rating', '>', rating).order_by(
        'rating', direction=firestore.Query.DESCENDING).stream()

    resp = [venue.to_dict() for venue in venues]

    return get_venues_handler(resp)


def search_price_type(price_type):
    venues_ref = db.collection('venues')
    venues = venues_ref.where('price_type', '==', unquote(price_type)).order_by(
        'name', direction=firestore.Query.ASCENDING).stream()

    resp = [venue.to_dict() for venue in venues]

    # sort the venues by name in ascending order
    resp.sort(key=lambda x: x['name'])

    return get_venues_handler(resp)


def get_geohash(lat, lon):
    return pgh.encode(lat, lon, precision=12)


def search_location(latitude, longitude):
    venues_ref = db.collection('venues')
    venues = venues_ref.stream()

    resp = []
    for venue in venues:
        venue_dict = venue.to_dict()

        # calculate the great-circle distance between two coordinates
        distance = pgh.geohash_haversine_distance(
            venue_dict['geohash'], get_geohash(latitude, longitude))

        if distance <= 5000:
            print(venue_dict['name'], distance)
            venue_dict['distance'] = distance
            resp.append(venue_dict)

    # sort the venues by distance in ascending order
    resp.sort(key=lambda x: x['distance'])
    print(len(resp))
    return get_venues_handler(resp)


@app.get("/")
async def root():
    return {"message": "Hello Venues!"}


@app.get("/search")
async def search_venues(name: str = None, rating: float = None, price_type: str = None, latitude: float = None, longitude: float = None):
    # allow you to pass 'Hunter & Barrel' instead of 'Hunter%20%26%20Barrel' in the localhost:8000/docs api
    if name is not None:
        return search_name(name)
    if rating is not None:
        return search_rating(rating)
    if price_type is not None:
        return search_price_type(price_type)
    if latitude is not None and longitude is not None:
        return search_location(latitude, longitude)
    raise HTTPException(
        status_code=400, detail="At least one parameter is required")
