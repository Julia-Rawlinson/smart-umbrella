import serial # type: ignore
import requests # type: ignore
import time

api_key = "c3d8dec77b73f237a0b61db1382a6ebc"
city = "toronto"
weather_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
arduino = serial.Serial(port='/dev/tty.usbmodem142401', baudrate=9600, timeout=1)


def fetch_weather():
    try:
        print("Fetching weather data...")
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            weather_description = data["current"]["weather_descriptions"][0]
            print(f"Weather: {weather_description}")
            return weather_description
        else:
            print(f"Failed to fetch weather data. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
    
def test_mode():
    print("Test mode enabled. Type 'Clear', 'Rain', 'Snow', or 'Exit' to test servo movement.")
    while True:
        command = input("Enter weather description: ").strip()
        if command.lower() == "exit":
            print("Exiting test mode.")
            break
        send_to_arduino(command)    
    
def send_to_arduino(weather_description):
    arduino.write(weather_description.encode('utf-8') + b'\n')
    print(f"Sent to Arduino: {weather_description}")

def main():
    mode = input("Enter 'test' for test mode or 'run' to fetch weather data: ").strip().lower()
    if mode == "test":
        test_mode()
    elif mode == "run":
        while True:
            weather_description = fetch_weather()
            if weather_description:
                send_to_arduino(weather_description)
            time.sleep(600)  # Wait 10 minutes before fetching again
    else:
        print("Invalid mode. Exiting.")

if __name__ == "__main__":
    main()