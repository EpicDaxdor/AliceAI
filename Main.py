import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests
import logging
from time import sleep

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

API_KEY = '45e2c57f1323f92e4797827cb3dadf70'  # Added my your OpenWeatherMap API key

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

# Configure logging
logging.basicConfig(level=logging.INFO)

def handle_error(e: Exception) -> None:
    """Handles errors by logging them."""
    if isinstance(e, requests.exceptions.HTTPError):
        logging.error(f"HTTP error occurred: {e}")
    elif isinstance(e, requests.exceptions.RequestException):
        logging.error(f"Request error occurred: {e}")
    elif isinstance(e, ValueError):
        logging.error(f"JSON decode error: {e}")

def tell_joke(retries: int = 3) -> str:
    url = "https://official-joke-api.appspot.com/random_joke"
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            joke_data = response.json()
            joke = f"{joke_data['setup']} {joke_data['punchline']}"
            return f"{joke} 1"  # Adding the number 1 to the joke
        except Exception as e:
            handle_error(e)  # Call the modular error handling function
        
        sleep(1)  # Wait before retrying

    return "I couldn't fetch a joke at the moment."

def get_weather(location):
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric")
        weather_data = response.json()
        if weather_data['cod'] == 200:
            main = weather_data['main']
            weather_description = weather_data['weather'][0]['description']
            temperature = main['temp']
            return f"The temperature in {location} is {temperature} degrees Celsius with {weather_description}."
        else:
            return "I couldn't find the weather for that location."
    except Exception as e:
        return "I couldn't fetch the weather at the moment."

def execute_command(command):
    command = command.lower()

    if "open browser" in command:
        webbrowser.open("http://www.google.com")
        speak("Opening the web browser.")
    elif "what time is it" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    elif "search for" in command:
        search_query = command.split("search for", 1)[1].strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching for {search_query}.")
    elif "tell me a joke" in command:
        joke = tell_joke()
        speak(joke)
    elif "weather in" in command:
        location = command.split("weather in", 1)[1].strip()
        weather_info = get_weather(location)
        speak(weather_info)
    elif "exit" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I am not sure how to help with that.")

    return True

def main():
    speak("Hello! I am your assistant.")
    while True:
        command = listen()
        if command:
            if not execute_command(command):
                break

if __name__ == "__main__":
    main()
