
import requests
import matplotlib.pyplot as plt
import pandas as pd

# 定義API URL和参数
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-025?Authorization=CWA-530FA5B2-CD7C-4CB5-A92F-6A93D85D0EBA"
params = {
    "Authorization": "CWA-530FA5B2-CD7C-4CB5-A92F-6A93D85D0EBA",
    "limit": 5,
    "format": "JSON"
}

# 發送GET請求
response = requests.get(url, params=params)

# 確保請求成功
if response.status_code == 200:
    data = response.json()

    # 提取所需字段
    extracted_data = []
    for location in data.get('records', {}).get('locations', []):
        for loc in location.get('location', []):
            location_name = loc.get('locationName', 'N/A')
            if location_name == '斗六市':  # 限制地點為"斗六市"
                for weather_element in loc.get('weatherElement', []):
                   if weather_element.get('elementName') == 'PoP12h':  # 降雨機率
                        for time in weather_element.get('time', []):
                            start_time = time.get('startTime', 'N/A')
                            end_time = time.get('endTime', 'N/A')
                            element_value = time.get('elementValue', [{}])[0].get('value', 'N/A')
                            extracted_data.append({
                                'Location Name': location_name,
                                'Start Time': start_time,
                                'End Time': end_time,
                                'PoP12h': element_value
                                })

    # 打印提取出的數據
    for item in extracted_data:
        print(f"Location Name: {item['Location Name']}, Start Time: {item['Start Time']}, End Time: {item['End Time']}, PoP12h: {item['PoP12h']}")
else:
    print(f"Failed to retrieve data, status code: {response.status_code}")
    
    

   
df = pd.DataFrame(extracted_data)