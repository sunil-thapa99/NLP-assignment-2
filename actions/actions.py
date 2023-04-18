from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
# from rasa_sdk.forms import FormAction
from datetime import datetime
from .scrap import get_context, get_links, get_original_url
import pandas as pd
import json 
import re
import os

df = pd.DataFrame(columns=["title", "price", "description", "date_posted", "address", "url"])
idx = 0
new_df = df.copy()

# Extract title and url from dataframe for chatbot to show
def get_ad_info(df, index: int=5) -> List[Dict[Text, Any]]:
    ad_info = []
    global idx
    # global df
    print(idx, df.shape)
    if idx < df.shape[0]:
        for i in range(idx, index):
            ad_info.append({"title": df.iloc[i]["title"], "url": df.iloc[i]["url"]})
            idx += 1
    else:
        ad_info.append({"title": "No more listings", "url": None})
    return ad_info

# Define function to extract numeric value from price string
def extract_numeric_value(price_str):
    price_regex = r'^\$?([\d,]+)(?:\.(\d{2}))?$'
    match = re.match(price_regex, price_str)
    if match:
        return float(match.group(1).replace(',', '') + '.' + (match.group(2) if match.group(2) else '00'))
    else:
        return None

# Scrap through kijiji
# class ActionSearchProperties(Action):

#     def name(self) -> Text:
#         return "action_search_properties"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         location = tracker.get_slot("location")
#         try:
#             sorting = tracker.get_slot('sorting')
#         except:
#             sorting = None
#         global df
#         df = df.iloc[0:0]
#         if location is None:
#             dispatcher.utter_message(text="Please enter a location to search for properties.")
#             return []
#         elif not location.strip():
#             dispatcher.utter_message(text="Please enter a valid location to search for properties.")
#             return [SlotSet("entity_name", None)]
#         else:
#             url = get_original_url(location, sorting)
#             demo_links = get_links(url=url)
#             for link in demo_links[:20]:
#                 result = get_context(link)
#                 df = df.append(result, ignore_index=True)
#             df.to_csv('kijiji_toronto_apartments.csv', index=False)
#             ad_info = get_ad_info(df)
#             # Loop through each ad and show through listing
#             text = f"Here are some properties available in {location}: \n"
#             buttons = []
#             # Loop through each ad, payload on title and show url
#             for i in range(len(ad_info)):
#                 buttons.append(
#                     {"title": f"{i+1} - {ad_info[i]['title']}", "payload": '/property_details{\"idx\":\"' + str(i) + '\"}', 
#                      'url': ad_info[i]['url']}
#                 )
#             dispatcher.utter_message(text=text, buttons=buttons)
#             return []

# Filter through CSV 
class ActionSearchProperties(Action):

    def name(self) -> Text:
        return "action_search_properties"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        try:
            sorting = tracker.get_slot('sorting')
        except:
            sorting = None
        global df
        df = df.iloc[0:0]
        if location is None:
            dispatcher.utter_message(text="Please enter a location to search for properties.")
            return []
        elif not location.strip():
            dispatcher.utter_message(text="Please enter a valid location to search for properties.")
            return [SlotSet("entity_name", None)]
        else:
            data_path = os.path.join(os.getcwd(), 'actions/final_data.csv')
            df = pd.read_csv(data_path)
            df.drop_duplicates(subset='url', inplace=True)
            df['price'] = df['price'].astype(str)
            df['price'] = df['price'].apply(extract_numeric_value)
            if sorting:
                sorting = sorting.lower()
                if sorting in ['lowest', 'ascending']:
                    df = df['price'].sort_values(by='price', ascending=True)
                else:
                    df = df['price'].sort_values(by='price', ascending=False)
            ad_info = get_ad_info(df)
            # Loop through each ad and show through listing
            text = f"Here are some properties available in {location}: \n"
            buttons = []
            # Loop through each ad, payload on title and show url
            for i in range(len(ad_info)):
                buttons.append(
                    {"title": f"{i+1} - {ad_info[i]['title']}", "payload": '/property_details{\"idx\":\"' + str(i) + '\"}', 
                     'url': ad_info[i]['url']}
                )
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

# action for show more
class ActionShowMore(Action):
    def name(self) -> Text:
        return "action_show_more"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global idx, df
        id = idx
        ad_info = get_ad_info(df, idx+5)
        # Loop through each ad and show through listing
        text = f"Here are some more properties: \n"
        buttons = []
        # Loop through each ad, payload on title and show url
        for i in range(len(ad_info)):
            buttons.append(
                {"title": f"{id+1} - {ad_info[i]['title']}", "payload": '/property_details{\"idx\":\"' + str(i) + '\"}', 
                    'url': ad_info[i]['url']}
            )
            id += 1
        dispatcher.utter_message(text=text, buttons=buttons)
        return []

# action for querying through df description if there is specific for gender
class ActionQueryGender(Action):
    def name(self) -> Text:
        return "action_query_gender"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global df, idx, new_df
        idx = 0
        pattern = re.compile(r'\b(male|female|m|f|man|woman)\b', flags=re.IGNORECASE)
        df['gender'] = df['description'].str.extract(pattern, expand=False)
        gender_map = {
            'male': 'male',
            'Male': 'male',
            'MALE': 'male',
            'm': 'male',
            'man': 'male',
            'female': 'female',
            'Female': 'female',
            'FEMALE': 'female',
            'f': 'female',
            'woman': 'female'
        }
        gender = tracker.get_slot("gender")
        df['gender'] = df['gender'].map(gender_map)
        new_df = df[df['gender'] == gender]
        # new_df = df[df['description'].str.contains(gender, case=False)]
        if new_df.shape[0] == 0:
            dispatcher.utter_message(text="Sorry, there are no properties that match your criteria.")
        else:
            ad_info = get_ad_info(new_df)
            print(ad_info, 'gender')
            # Loop through each ad and show through listing
            text = f"Here are some properties that match your criteria: \n"
            buttons = []
            # Loop through each ad, payload on title and show url
            for i in range(len(ad_info)):
                buttons.append(
                    {"title": f"{i+1} - {ad_info[i]['title']}", "payload": '/property_details{\"idx\":\"' + str(i) + '\"}', 
                        'url': ad_info[i]['url']}
                )
            dispatcher.utter_message(text=text, buttons=buttons)
        return []

# action for querying through df description if there is specific for basement or main floor
class ActionQueryBasement(Action):
    def name(self) -> Text:
        return "action_query_basement"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global df, idx, new_df
        idx = 0
        floor_type = tracker.get_slot("floor_type")
        new_df = df[df['description'].str.contains(floor_type, case=False) == True]
        if new_df.shape[0] == 0:
            dispatcher.utter_message(text="Sorry, there are no properties that match your criteria.")
        else:
            ad_info = get_ad_info(new_df)
            # Loop through each ad and show through listing
            text = f"Here are some properties that match your criteria: \n"
            buttons = []
            # Loop through each ad, payload on title and show url
            for i in range(len(ad_info)):
                buttons.append(
                    {"title": f"{i+1} - {ad_info[i]['title']}", "payload": '/property_details{\"idx\":\"' + str(i) + '\"}', 
                        'url': ad_info[i]['url']}
                )
            dispatcher.utter_message(text=text, buttons=buttons)
        return []

# action for querying through df description if there is specific for number of bedrooms
class ActionQueryBedrooms(Action):
    def name(self) -> Text:
        return "action_query_bedrooms"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global df, new_df
        bedrooms = tracker.get_slot("bedrooms")
        new_df = df['title'].str.extract('(\d+)\s*Bed', flags=re.IGNORECASE, expand=False).fillna(-1).astype(int)
        new_df = new_df[new_df == int(bedrooms)]
        if new_df.shape[0] == 0:
            dispatcher.utter_message(text="Sorry, there are no properties that match your criteria.")
        else:
            ad_info = get_ad_info(new_df)
            # Loop through each ad and show through listing
            text = f"Here are some properties that match your criteria: \n"
            buttons = []
            # Loop through each ad, payload on title and show url
            for i in range(len(ad_info)):
                buttons.append(
                    {"title": f"{i+1} - {ad_info[i]['title']}", "payload": '/property_details{\"idx\":\"' + str(i) + '\"}', 
                        'url': ad_info[i]['url']}
                )
            dispatcher.utter_message(text=text, buttons=buttons)
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
        
        message_text = tracker.latest_message['text']
        command, json_payload = message_text.split('property_details', 1)
        idx_value = int(json.loads(json_payload)['idx'])
        global new_df
        if new_df.empty:
            dispatcher.utter_message(text=f"Here are the details for the property: </hr></br>"
                                        f"<strong>Title</strong>: {df.iloc[idx_value]['title']} </hr></br>"
                                        f"<strong>Price</strong>: {df.iloc[idx_value]['price']} </hr></br>"
                                        f"<strong>Description</strong>: {df.iloc[idx_value]['description'][11:]} </hr></br>"
                                        # f"<strong>Date Posted</strong>: {df.iloc[idx_value]['date_posted']} </hr></br>"
                                        f"<strong>Address</strong>: {df.iloc[idx_value]['address']} </hr></br>"
                                        f"<strong>URL</strong>: <a href='{df.iloc[idx_value]['url']}'>{df.iloc[idx_value]['url']}</a> </hr></br>")
        else:
            dispatcher.utter_message(text=f"Here are the details for the property: </hr></br>"
                                        f"<strong>Title</strong>: {new_df.iloc[idx_value]['title']} </hr></br>"
                                        f"<strong>Price</strong>: {new_df.iloc[idx_value]['price']} </hr></br>"
                                        f"<strong>Description</strong>: {new_df.iloc[idx_value]['description'][11:]} </hr></br>"
                                        # f"<strong>Date Posted</strong>: {new_df.iloc[idx_value]['date_posted']} </hr></br>"
                                        f"<strong>Address</strong>: {new_df.iloc[idx_value]['address']} </hr></br>"
                                        f"<strong>URL</strong>: <a href='{new_df.iloc[idx_value]['url']}'>{new_df.iloc[idx_value]['url']}</a> </hr></br>")
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
