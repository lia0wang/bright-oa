import re
import json
import requests
from bs4 import BeautifulSoup

def scrape_yelp_data():
    restaurant_list = []
    
    # scrape the data
    for i in range(10):
        print(f"Scraping page {i+1}")
        url = f"https://www.yelp.com/search?find_desc=Restaurants&find_loc=Sydney+New+South+Wales&start={i*10}"
        response = requests.get(url)
    
        soup = BeautifulSoup(response.text, "html.parser")
    
        # fetch the json script
        try:
            general_data = soup.find("script", {"type": "application/json", "data-hypernova-key": "yelpfrontend__5385__yelpfrontend__GondolaSearch__dynamic"})
        except IndexError:
            print("Script tag not found")
            continue
        general_text = general_data.text.strip()

        # format the json string
        general_json_str = re.sub(r"<!--|-->", "", general_text)
        # json string -> python dict
        general_json_data = json.loads(general_json_str)
    
        for restaurant in general_json_data['legacyProps']['searchAppProps']['searchPageProps']['mainContentComponentsListProps']:
            # if restaurant has key called bizId
            if 'bizId' in restaurant.keys():
                restaurant_name = restaurant['searchResultBusiness']['name'].replace('&amp;', '&').replace('\u2019', "'")
                restaurant_rating = restaurant['searchResultBusiness']['rating']
                price_type = restaurant['searchResultBusiness']['priceRange']
                businessUrl = restaurant['searchResultBusiness']['businessUrl']
    
                restaurant = {
                    "restaurant_name": restaurant_name,
                    "restaurant_rating": restaurant_rating,
                    "price_type": price_type,
                    "businessUrl": businessUrl
                }
                print(f'Scraping url from: {restaurant_name} done')
                restaurant_list.append(restaurant)
        
        # fetch longitude and latitude
        try:
            location_data = soup.find("script", {"type": "application/json", "data-hypernova-key": "yelpfrontend__5385__yelpfrontend__GondolaSearch__dynamic"})
        except IndexError:
            print("Script tag not found")
            continue
        
        location_text = location_data.text.strip()
        # format the json string
        location_json_str = re.sub(r"<!--|-->", "", location_text)
        # json string -> python dict
        location_json_data = json.loads(location_json_str)
        
        # for each restaurant, update the dict with longitude and latitude
        for restaurant in restaurant_list:
            for maker in location_json_data['legacyProps']['searchAppProps']['searchPageProps']['rightRailProps']['searchMapProps']['mapState']['markers']:
                if 'url' in maker.keys() and maker['url'] in restaurant['businessUrl']:
                    restaurant['latitude'] = maker['location']['latitude']
                    restaurant['longitude'] = maker['location']['longitude']
                    print(f"{restaurant['restaurant_name']} - {restaurant['latitude']}, {restaurant['longitude']}")
                    break

    # for restaurant in restaurant_list, access the businessUrl and scrape the data
    rank = 1
    for restaurant in restaurant_list:
        print(f"Scraping data from: {rank} - {restaurant['restaurant_name']} starts >>>")
    
        url = f"https://www.yelp.com{restaurant['businessUrl']}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # fetch the json script
        try :
            address_reviews_data = soup.find_all("script", {"type": "application/ld+json"})[1]
        except IndexError:
            print("Script tag not found")
            continue

        address_reviews_text = address_reviews_data.text.strip()
        # format the json string
        address_reviews_json_str = re.sub(r"<!--|-->", "", address_reviews_text)
        # json string -> python dict
        address_reviews_json_data = json.loads(address_reviews_json_str)
        
        # if it is not a restaurant page, e.g. FAQ page
        if address_reviews_json_data['@type'] != 'Restaurant':
            continue
    
        # fetch the address
        restaurant_address = f"{address_reviews_json_data['address']['streetAddress']}, {address_reviews_json_data['address']['addressLocality']}, {address_reviews_json_data['address']['addressRegion']} {address_reviews_json_data['address']['postalCode']}".replace('\n', ' ')
        # fetch the reviews
        reviews = address_reviews_json_data['review']
        
        # sort the reviews by rating, best 3 reviews
        reviews = sorted(reviews, key=lambda x: x['reviewRating']['ratingValue'], reverse=True)[:3]
        # fetch the review description and put it in a list
        reviews = [review['description'].replace('\n', ' ').replace('&apos;', "'").replace('&amp;', '&') for review in reviews]
    
        # store the address and reviews in the restaurant dictionary
        restaurant['restaurant_address'] = restaurant_address
        restaurant['review_highlights'] = reviews
    
        print(f"Scraping data from: {rank} - {restaurant['restaurant_name']} done   <<<")
        rank += 1

    # store the data in a JSON file
    with open("../data/restaurants.json", "w") as f:
        json.dump(restaurant_list, f, indent=4)
    
    return restaurant_list

if __name__ == '__main__':
    scrape_yelp_data()