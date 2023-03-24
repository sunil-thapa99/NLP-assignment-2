# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormAction
from datetime import datetime

# class ActionGreet(Action):
#     def name(self) -> Text:
#         return "action_greet"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         dispatcher.utter_message(response="utter_greet")
        
#         return []
    
# class ActionGoodbye(Action):
#     def name(self) -> Text:
#         return "action_goodbye"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         dispatcher.utter_message(response="utter_goodbye")
        
#         return []

class ActionSearchProperties(Action):

    def name(self) -> Text:
        return "action_search_properties"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        # Perform property search logic here based on user's location input
        
        dispatcher.utter_message(text=f"Here are some properties available in {location}: [Property 1], [Property 2], [Property 3]")
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
