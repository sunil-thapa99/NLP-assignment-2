# NLP-assignment-2

### Steps:
  - Step 1: pip install rasa
  - Step 2: rasa train [To train model]
  - Step 3: rasa run actions [To run all the action and create an endpoint: view endpoints.yml]
  - Step 4: rasa shell [To use command line to interact with chatbot]
  - Step 5: rasa run -m models --enable-api --cors "*" --debug

> Step 3 & 5 should be run in two different terminals as our project contains action to perform as per intent classification