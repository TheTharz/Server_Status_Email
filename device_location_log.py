import requests
import json
from datetime import datetime

def log_device_location():
    try:
        # Fetch location data from the external API
        response = requests.get("https://ipinfo.io")
        data = response.json()

        # Extract necessary information
        ip = data.get('ip', 'N/A')
        city = data.get('city', 'N/A')
        region = data.get('region', 'N/A')
        country = data.get('country', 'N/A')
        loc = data.get('loc', 'N/A')
        org = data.get('org', 'N/A')
        timezone = data.get('timezone', 'N/A')

        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Log data to a file
        log_data = {
            'timestamp': timestamp,
            'ip': ip,
            'city': city,
            'region': region,
            'country': country,
            'loc': loc,
            'org': org,
            'timezone': timezone
        }

        with open('device_location_log.json', 'a') as log_file:
            log_file.write(json.dumps(log_data) + '\n')

        print("Location logged successfully")

    except Exception as e:
        print(f"Error logging location: {e}")

if __name__ == "__main__":
    log_device_location()
