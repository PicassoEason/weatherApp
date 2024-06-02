import requests
import pandas as pd
import matplotlib.pyplot as plt

# API URL
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWA-1DD9390B-E18C-49A7-B850-511F98946DF2"
params = {
    "Authorization": "CWA-1DD9390B-E18C-49A7-B850-511F98946DF2",
    "limit": 5,
    "format": "JSON"
}

# Send GET request
response = requests.get(url, params=params)

# Ensure the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract required fields
    extracted_data = []
    for record in data.get('records', {}).get('Earthquake', []):
        earthquake_info = record.get('EarthquakeInfo', {})
        origin_time = earthquake_info.get('OriginTime', 'N/A')
        epicenter = earthquake_info.get('Epicenter', {}).get('Location', 'N/A')
        magnitude = earthquake_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', 'N/A')
        
        extracted_data.append({
            'Origin Time': origin_time,
            'Epicenter': epicenter,
            'Magnitude': magnitude
        })

    # Print the extracted data
    for item in extracted_data:
        print(f"Origin Time: {item['Origin Time']}, Epicenter: {item['Epicenter']}, Magnitude: {item['Magnitude']}")

    # Create a DataFrame
    df = pd.DataFrame(extracted_data)

    # Print the DataFrame
    print(df)

    # Convert Magnitude to float for plotting
    df['Magnitude'] = df['Magnitude'].astype(float)

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(df['Origin Time'], df['Magnitude'], marker='o', linestyle='-', color='b')
    plt.title('Earthquake Magnitudes Over Time')
    plt.xlabel('Origin Time')
    plt.ylabel('Magnitude')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print(f"Failed to retrieve data, status code: {response.status_code}")
