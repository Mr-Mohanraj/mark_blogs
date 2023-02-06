import random
from django.conf import settings
import json
import jwt


def get_random_quote():
    with open(settings.BASE_DIR/'static/sample.json', 'r') as file:
        file_data = json.load(file)
        quote = {"quote": "", "author": ""}
        if not(random.randint(1, 99) == 41):
            quote = file_data[f"quote {random.randint(1,99)}"]
    return quote['quote'], quote['author']
