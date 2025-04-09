from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import logging
import sys
import os
import datetime

def botreply(messagein, db_location="database.db"):
    # Check if the database file exists
    if not os.path.exists(db_location):
        error = "ERROR IN REPLYING \n"
        error = error + "Model does not exist at " + db_location + "\n"
        error = str(datetime.datetime.now()) + "\n" + error + "\n"
        print(error)
        return "Sorry! I am resting right now. Please come back later"
    
    # Set the logging level for ChatterBot to suppress unnecessary logs
    logging.getLogger('chatterbot').setLevel(logging.WARNING)

    # Initialize the chatbot with logic adapters
    chatbot = ChatBot(
        'Chatting Bot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.MathematicalEvaluation'
            },
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'input_text': 'Help me!',
                'output_text': 'mail your query here'
            }
        ],
        database_uri=f'sqlite:///{db_location}',
        response_selection_method=get_random_response,
        read_only=True
    )

    # Handle special exit keywords (e.g., goodbye, thanks)
    exit_keywords = ['goodbye', 'thanks', 'thank you', 'bye', 'see you']
    if any(keyword in messagein.lower() for keyword in exit_keywords):
        response = "Goodbye! It was nice talking to you. See you next time!"
        print("\n")
        print('YOU (Input):', messagein)
        print('Virtual Tutoring BOT:', response)
        print("\n")
        return response
    
    # Get a response from the chatbot
    message = messagein
    reply = chatbot.get_response(message)
    response = str(reply)

    print("\n")
    print('YOU (Input):', message)
    print('Virtual Tutoring BOT:', response)
    print("\n")
    return response
