import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from task1.scraper import scrape_yelp_data
import pygeohash as pgh

# Use a service account
cred = credentials.Certificate('./service_account.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

def get(venue_data, key):
    return venue_data[key] if key in venue_data.keys() else None

def calculate_geohash(lat, lon):
    return pgh.encode(lat, lon)

# Function to write venue data to Firestore
def write_to_firestore(venue_data):
    # Generate a unique identifier for the document
    doc_id = str(uuid.uuid4())

    # Create a dictionary to store the data
    venue_dict = {
        'name': get(venue_data, 'restaurant_name'),
        'rating': get(venue_data, 'restaurant_rating'),
        'url': get(venue_data, 'businessUrl'),
        'address': get(venue_data, 'restaurant_address'),
        'price_type': get(venue_data, 'price_type'),
        'review_highlights': get(venue_data, 'review_highlights'),
        'geohash': calculate_geohash(get(venue_data, 'latitude'), get(venue_data, 'longitude')),
        'latitude': get(venue_data, 'latitude'),
        'longitude': get(venue_data, 'longitude')
    }

    # Write the data to Firestore
    db.collection('venues').document(doc_id).set(venue_dict)

# Call the scraping function to get venue data
venue_data_list = scrape_yelp_data()

# Write the data to Firestore
for venue_data in venue_data_list:
    write_to_firestore(venue_data)
