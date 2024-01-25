import os
import json
import random


# save messages to json file
def reset_messages():

    file_name = "stored_data.json"

    # write an empty file
    open(file_name, "w")