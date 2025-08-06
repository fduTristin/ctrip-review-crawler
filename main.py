from fetchComments import *
from fetchHotels import *
import json
from tqdm import tqdm  # Import tqdm for progress bar
import os  # Import os module for directory operations
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor for multithreading

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


# Function to process a single hotel
def process_hotel(hotel_id, hotel_data, numCommentPages):
    comments = fetchHotelComments(hotel_id, numCommentPages)
    hotel_data['comments'] = comments
    with open(f'outputs/hotel_{hotel_id}.json', 'w', encoding='utf-8') as hotel_file:
        json.dump(hotel_data, hotel_file, ensure_ascii=False, indent=4)

# read hotels from json and process each hotel
print("Fetching comments for each hotel...")
with open('hotels.json', 'r', encoding='utf-8') as f:
    hotels_dict = json.load(f)  # Load the entire JSON object

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(process_hotel, hotel_id, hotel_data, numCommentPages)
            for hotel_id, hotel_data in hotels_dict.items()
        ]
        for future in tqdm(futures, desc="Processing hotels", unit="hotel"):
            future.result()  # Wait for each thread to complete