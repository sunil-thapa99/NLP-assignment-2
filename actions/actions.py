from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
# from rasa_sdk.forms import FormAction
from datetime import datetime
from .scrap import get_context, get_links, get_original_url
import pandas as pd

# Extract title and url from dataframe for chatbot to show
def get_ad_info(df: pd.DataFrame) -> List[Dict[Text, Any]]:
    ad_info = []
    for i in range(len(df)):
        ad_info.append({"title": df.iloc[i]["title"], "url": df.iloc[i]["url"]})
    return ad_info

class ActionSearchProperties(Action):

    def name(self) -> Text:
        return "action_search_properties"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        if location is None:
            dispatcher.utter_message(text="Please enter a location to search for properties.")
            return []
        elif not location.strip():
            dispatcher.utter_message(text="Please enter a valid location to search for properties.")
            return [SlotSet("entity_name", None)]
        else:
            df = pd.DataFrame(columns=["title", "price", "description", "date_posted", "address", "url"])
            url = get_original_url(location)
            demo_links = get_links(url=url)
            for link in demo_links[:5]:
                result = get_context(link)
                df = df.append(result, ignore_index=True)
            df.to_csv('kijiji_toronto_apartments.csv', index=False)
            ad_info = get_ad_info(df)
            # Loop through each ad and show through listing
            text = f"Here are some properties available in {location}: \n"
            buttons = []
            # Loop through each ad and show through listing with buttons
            for i in range(len(ad_info)):
                buttons.append(
                    {"title": f"{i+1} - {ad_info[i]['title']}", "payload": f"/inform{{\"url\": \"{ad_info[i]['url']}\"}}"}
                )
            # for i in range(len(ad_info)):
            #     text += f"{i+1} - {ad_info[i]['title']}: {ad_info[i]['url']} \n"
            # print(text)
            # dispatcher.utter_message(text=f"Here are some properties available in {location}: \n"+
            dispatcher.utter_message(text=text, buttons=buttons)
            return []

# action_search_properties_no_location
class ActionSearchPropertiesNoLocation(Action):
        def name(self) -> Text:
            return "action_search_properties_no_location"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
            dispatcher.utter_message(text="Please enter a location to search for properties.")
            return []

class ActionProvideLeaseDetails(Action):

    def name(self) -> Text:
        return "action_provide_lease_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Perform logic to retrieve and format lease details
        # ...
        # Example response:
        dispatcher.utter_message(text="The lease is for 12 months, and the rent is $2000 per month.")
        return []
    
class ActionProvidePropertyDetails(Action):

    def name(self) -> Text:
        return "action_provide_property_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Perform logic to retrieve and format lease details
        # ...
        # Example response:
        dispatcher.utter_message(text="This is the property details function")
        return []

class ActionAvailabilityPricing(Action):

    def name(self) -> Text:
        return "action_availability_pricing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Perform logic to retrieve and format lease details
        # ...
        # Example response:
        dispatcher.utter_message(text="This is the pricing function")
        return []

class ActionScheduleTour(Action):
    def name(self) -> Text:
        return "action_schedule_tour"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Use an API to schedule a virtual tour based on the user's availability
        # ...

        date_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        dispatcher.utter_message(response="utter_schedule_tour", date=date_time)
        
        return []

class ActionCancelTour(Action):

    def name(self) -> Text:
        return "action_cancel_tour"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Perform logic to cancel the scheduled tour
        # ...
        # Example response:
        dispatcher.utter_message(text="Your virtual tour has been cancelled.")
        return []

class ActionProvideParkingInfo(Action):

    def name(self) -> Text:
        return "action_provide_parking_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Perform logic to retrieve and format parking information
        # ...
        # Example response:
        dispatcher.utter_message(text="The parking info is as follows.")
        return []

class ActionProvidePetPolicy(Action):

    def name(self) -> Text:
        return "action_provide_pet_policy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Perform logic to retrieve and format parking information
        # ...
        # Example response:
        dispatcher.utter_message(text="This is pet policy section")
        return []
