import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

def fetchComments(hotelId, pageIndex):
 
    url = "https://m.ctrip.com/restapi/soa2/33278/getHotelCommentList"
    headers = {
        'Content-type': 'application/json',
        'Origin': 'https://hotels.ctrip.com',
        'Referer': 'https://hotels.ctrip.com',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    
    formData = {
    "hotelId": hotelId,
    "pageIndex": pageIndex,
    "pageSize": 10,
    "repeatComment": 1,
    "needStaticInfo": False,
    "functionOptions": [
        "integratedTopComment",
        "ctripIntegratedExpediaTaList"
    ],
    "filterInfo": [
        {
            "id": 4,
            "filterType": 1
        }
    ],
    "orderBy": 1, # 1: by time
    "head": {
        "platform": "PC",
        "cver": "0",
        "cid": "",
        "bu": "HBU",
        "group": "ctrip",
        "aid": "",
        "sid": "",
        "ouid": "",
        "locale": "zh-CN",
        "timezone": "8",
        "currency": "CNY",
        "pageId": "102003",
        "vid": "",
        "guid": "",
        "isSSR": False
    }
}
    
    # 发起网络请求
    r = requests.post(url, json=formData, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding

    if not r.text.strip():
        print("Error: Empty response from server.")
        return []

    try:
        data = json.loads(r.text)["data"]["commentList"]

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response.")
        return []
    
    commentList = []
    for item in data:
        content = item["content"]
        rating = item["rating"]
        if "imageList" not in item:
            continue
        imageURLs = item["imageList"]
        createDate = item["createDate"]
        commentList.append({
            "content": content,
            "rating": rating,
            "imageURLs": imageURLs,
            "createDate": createDate
        })
    
    
    return commentList

def fetchHotelComments(hotelId, numPages=10):
    allComments = []

    def fetch_page(pageIndex):
        return fetchComments(hotelId, pageIndex)

    with ThreadPoolExecutor(max_workers=2) as executor: 
        results = executor.map(fetch_page, range(1, numPages + 1))
        for comments in results:
            allComments.extend(comments)

    return allComments

# just for testing
if __name__ == "__main__":
    allComments = fetchHotelComments(5545568, numPages=50)

    with open("comments.json", "w", encoding="utf-8") as f:
        json.dump(allComments, f, ensure_ascii=False, indent=4)