# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from scripts import zomatoApi


class ActionFindRestaurants(Action):
    """
    Find the restaurants using location & cuisine.
    Required Parameters: Location, Cuisine
    """

    def name(self) -> Text:
        return "action_find_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        print("====Inside ActionSearchRestaurants====")
        print()

        ## extract the required slots
        if tracker.get_slot("user_location"):
            location = tracker.get_slot("user_location")
            locationEntities = zomatoApi.getLocationDetailsbyName(location)
            if locationEntities["restaurants_available"] == "no":
                dispatcher.utter_message("Sorry I couldn't find any restaurants  😓")
                return []
            entity_id = locationEntities["entity_id"]
            entity_type = locationEntities["entity_type"]
            city_id = locationEntities["city_id"]
            SlotSet("user_location", locationEntities["title"])

        else:
            dispatcher.utter_message(
                "Sorry, I couldn't find your location.")
            return [UserUtteranceReverted()]

        cuisine = tracker.get_slot("cuisine")

        ##get the cuisine id for the cuisine name user provided
        cuisine_id = zomatoApi.getCuisineId(cuisine, city_id)

        print("Entities:  ", entity_id, " ", entity_type, " ", cuisine_id, " ", location, " ", cuisine)
        print()

        ## if we didn't find the restaurant for which user has provided the cuisine name
        if (cuisine_id == None):
            dispatcher.utter_message(
                "Sorry we couldn't find any restaurants that serves {} cuisine in {}".format(cuisine, location))
            return [UserUtteranceReverted()]
        else:
            ## search the restaurants by calling zomatoApi api
            restaurants = zomatoApi.searchRestaurants(entity_id, entity_type, cuisine_id, "")
            print("Here are the few restaurants that matches your preferences 😋")
            respose_message = ""

            if len(restaurants) > 0:
                for index, restaurant in enumerate(restaurants):
                    respose_message += (f"\n" \
                                        f"Restaurant {index + 1}: {restaurant['name']}" \
                                        f"\n" \
                                        f"\t Timings: {restaurant['timings']}" \
                                        f"\n" \
                                        f"\t Cuisines: {restaurant['cuisines']}" \
                                        f"\n" \
                                        f"\t Ratings: {restaurant['ratings']}/5" \
                                        f"\n" \
                                        f"\t Address: {restaurant['address']}" \
                                        f"\n" \
                                        f"\t Photos URL: {restaurant['photos']}" \
                                        f"\n")

            dispatcher.utter_message(respose_message)

