from fetchComments import *
from fetchHotels import *
import json
from tqdm import tqdm  # Import tqdm for progress bar
import os  # Import os module for directory operations

# config
cityId = 2  # 1: Beijing, 2: Shanghai, 3: Guangzhou, 4: Shenzhen
numHotelPages = 10  # the number of hotels fetched is about numHotelPages * 10, unless there are not enough hotels
numCommentPages = 100  # the number of comments fetched is about numCommentPages * 10, unless there are not enough comments

# Ensure 'outputs' directory exists
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# fetch hotels
print(f"Fetching hotels for city {cityId}...")
fetchHotels(cityId, numHotelPages, savePath="hotels.json")
print("Hotels fetched and saved to hotels.json")


# read hotels from json and process each hotel
print("Fetching comments for each hotel...")
with open('hotels.json', 'r', encoding='utf-8') as f:
    hotels_dict = json.load(f)  # Load the entire JSON object
    for hotel_id, hotel_data in tqdm(hotels_dict.items(), desc="Processing hotels", unit="hotel"):
        # fetch comments for the hotel
        comments = fetchHotelComments(hotel_id, numCommentPages)
        hotel_data['comments'] = comments

        # save the complete hotel data to a file
        with open(f'outputs/hotel_{hotel_id}.json', 'w', encoding='utf-8') as hotel_file:
            json.dump(hotel_data, hotel_file, ensure_ascii=False, indent=4)