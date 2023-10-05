import googlemaps
from twilio.rest import Client
import time

# Set your Google Maps API key and Twilio credentials
google_maps_api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
twilio_account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
twilio_auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'
your_phone_number = 'YOUR_PHONE_NUMBER'  # Replace with your phone number

# Initialize Google Maps client
gmaps = googlemaps.Client(key=google_maps_api_key)

def get_traffic_duration(origin, destination):
    try:
        # Get current traffic duration between origin and destination
        directions_result = gmaps.directions(origin, destination, mode="driving", departure_time="now")
        duration_in_traffic = directions_result[0]["legs"][0]["duration_in_traffic"]["text"]
        return duration_in_traffic
    except Exception as e:
        return str(e)

def send_sms_notification(message):
    client = Client(twilio_account_sid, twilio_auth_token)
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=your_phone_number
    )

def main():
    origin = "Boston, MA"
    destination = "Andover, MA"
    threshold_duration = "15 mins"  # Set your threshold duration

    while True:
        traffic_duration = get_traffic_duration(origin, destination)

        if traffic_duration > threshold_duration:
            alert_message = f"Traffic alert: Current duration from {origin} to {destination} is {traffic_duration}."
            send_sms_notification(alert_message)

        time.sleep(600)  # Check traffic every 10 minutes

if __name__ == '__main__':
    main()

