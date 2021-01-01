## functions to call zomato api for searching the restaurants
# get the API key from https://developers.zomato.com/documentation#/
import requests
import json

# headers = {'user-key': '{Put your Zomato API key here}',
#            'Accept': 'application/json'}


def getLocationDetailsbyName(location_name):
    data = {'query': location_name}
    url = 'https://developers.zomato.com/api/v2.1/locations'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    print("Came to getLocationDetailsbyName ")
    print()

    if (len(data["location_suggestions"]) > 0):
        entity_id = data["location_suggestions"][0]["entity_id"]
        entity_type = data["location_suggestions"][0]["entity_type"]
        title = data["location_suggestions"][0]["title"]
        city_id = data["location_suggestions"][0]["city_id"]
        city_name = data["location_suggestions"][0]["city_name"]
        city_name = data["location_suggestions"][0]["city_name"]
        latitude = data["location_suggestions"][0]["latitude"]
        longitude = data["location_suggestions"][0]["longitude"]
        details = {"restaurants_available": "yes", "entity_id": entity_id, "entity_type": entity_type, "title": title,
                   "city_id": city_id, "city_name": city_name, "latitude": latitude, "longitude": longitude}
        return details
    else:
        return {"restaurants_available": "no"}



def getCuisineId(cuisine_name, city_id):
    data = {'city_id': city_id}
    url = 'https://developers.zomato.com/api/v2.1/cuisines'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    #print("data from cuisine id api: ",data)
    cuisines = data["cuisines"]
    cuisineID = None
    for cuisine in cuisines:
        if (cuisine_name.lower() == cuisine["cuisine"]["cuisine_name"].lower()):
            cuisineID = cuisine["cuisine"]["cuisine_id"]
            print("cuisine id =", cuisineID)
            return cuisineID

    return cuisineID


def searchRestaurants(entity_id, entity_type, cuisine_id, search_query):
    url = 'https://developers.zomato.com/api/v2.1/search'
    data = {"entity_id": entity_id, "entity_type": entity_type,
            "cuisines": cuisine_id, "count": "10", "order": "asc"}
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    restaurants = []
    if (len(data["restaurants"]) < 10):
        restoDataLen = len(data["restaurants"])
    else:
        restoDataLen = 10

    for i in range(0, restoDataLen):
        item = {}
        photos = []
        item["id"] = data["restaurants"][i]["restaurant"]["id"]
        item["name"] = data["restaurants"][i]["restaurant"]["name"]
        item["url"] = data["restaurants"][i]["restaurant"]["url"]
        item["timings"] = data["restaurants"][i]["restaurant"]["timings"]
        item["votes"] = data["restaurants"][i]["restaurant"]["user_rating"]["votes"]
        item["image"] = data["restaurants"][i]["restaurant"]["featured_image"]
        item["cuisines"] = data["restaurants"][i]["restaurant"]["cuisines"]
        item["ratings"] = data["restaurants"][i]["restaurant"]["user_rating"]["aggregate_rating"]
        item["rating_color"] = data["restaurants"][i]["restaurant"]["user_rating"]["rating_color"]
        item["price_range"] = data["restaurants"][i]["restaurant"]["price_range"]
        item["cost"] = data["restaurants"][i]["restaurant"]["average_cost_for_two"]
        item["location"] = data["restaurants"][i]["restaurant"]["location"]["locality_verbose"]
        item["currency"] = data["restaurants"][i]["restaurant"]["currency"]
        item["user_rating_text"] = data["restaurants"][i]["restaurant"]["user_rating"]["rating_text"]
        item["address"] = data["restaurants"][i]["restaurant"]["location"]["address"]
        item["photos"] = data["restaurants"][i]["restaurant"]["photos_url"]
        # if "photos_url" in data["restaurants"][i]["restaurant"].keys():
        #     if (len(data["restaurants"][i]["restaurant"]["photos"]) < 5):
        #         photos_len = len(data["restaurants"][i]["restaurant"]["photos"])
        #     else:
        #         photos_len = 5
        #     for j in range(0, photos_len):
        #         photos.append(data["restaurants"][i]["restaurant"]["photos"][j]["photo"]["url"])
        #     item["photos"] = photos
        restaurants.append(item)

    return restaurants
