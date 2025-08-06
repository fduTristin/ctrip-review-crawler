import requests
import json
from datetime import datetime, timedelta

hotels = {}

def _fetchHotels(pageIndex, cityId=2):
 
    url = "https://m.ctrip.com/restapi/soa2/34951/fetchHotelList"
    headers = {
        'Content-type': 'application/json',
        'Origin': 'https://hotels.ctrip.com',
        'Referer': 'https://hotels.ctrip.com',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    
    formData = {
    "date": {
        "dateType": 1,
        "dateInfo": {
            "checkInDate": (datetime.now() + timedelta(days=1)).strftime("%Y%m%d"),
            "checkOutDate": (datetime.now() + timedelta(days=2)).strftime("%Y%m%d")
        }
    },
    "destination": {
        "type": 1,
        "geo": {
            "cityId": cityId,
            "countryId": 1
        },
        "keyword": {
            "word": ""
        }
    },
    "paging": {
        "pageIndex": pageIndex,
        "pageSize": 10,
        "pageCode": "10650171192"
    },
    "head": {
        "platform": "PC",
        "cver": "0",
        "bu": "HBU",
        "group": "ctrip",
        "locale": "zh-CN",
        "timezone": "8",
        "currency": "CNY",
        "pageId": "10650171192",
        "guid": "",
        "isSSR": False,
        "extension": [
            {
                "name": "cityId",
                "value": "2"
            },
            {
                "name": "checkIn",
                "value": "2025/08/06"
            },
            {
                "name": "checkOut",
                "value": "2025/08/07"
            },
            {
                "name": "region",
                "value": "CN"
            }
        ]
    }
}
    
    r = requests.post(url, json=formData, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding

    if not r.text.strip():
        print("Error: Empty response from server.")
        return []

    try:
        data = json.loads(r.text)["data"]["hotelList"]
        
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response.")
        return []
    
    for item in data:
        hotelInfo = item["hotelInfo"]
        hotelId = hotelInfo["summary"]["hotelId"]
        hotelName = hotelInfo["nameInfo"]["name"]
        hotelImages = hotelInfo["hotelImages"]["multiImgs"]
        hotelImgURLs = [img["url"] for img in hotelImages]
        hotelStar = hotelInfo["hotelStar"]["star"]
        hotels[hotelId] = {
            "hotelName": hotelName,
            "hotelImages": hotelImgURLs,
            "hotelStar": hotelStar
        }
    
    return hotels

def fetchHotels(cityId, numPages=10, savePath="hotels.json"):
    allHotels = {}
    for pageIndex in range(1, numPages + 1):
        hotels = _fetchHotels(pageIndex, cityId=cityId)
        allHotels.update(hotels)
    
    with open(savePath, "w", encoding="utf-8") as f:
        json.dump(allHotels, f, ensure_ascii=False, indent=4)
    
    return allHotels


# just for testing
if __name__ == "__main__":
    fetchHotels(cityId=2, numPages=10, savePath="hotels.json")