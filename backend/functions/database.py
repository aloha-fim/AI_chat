import os
import json
import random

# save messages for retrieval later on
def store_messages(request_message, response_message):

    # define the file name
    file_name = "stored_data.json"

    # get recent messages
    messages = get_recent_messages()[1:]

    # add messages to data
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # sae the updated file
    with open(file_name, "w") as f:
        json.dump(messages, f)


# save messages to json file
def reset_messages():

    file_name = "stored_data.json"

    # write an empty file
    open(file_name, "w")