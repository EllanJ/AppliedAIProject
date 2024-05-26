import os
import google.generativeai as genai
import speech_recognition as sr
import datetime
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import requests
from bs4 import BeautifulSoup

# Set the API key for Google Generative AI
GENAI_API_KEY = 'AIzaSyDme7NsAOlmWPbwsZdOv9zsuZ-AgnWnVI0'
# hi sir, as you can see naa mi na exposed api key sa google gemini. mi salig mi nimo sir hihi
os.environ['GOOGLE_API_KEY'] = GENAI_API_KEY
genai.configure(api_key=GENAI_API_KEY)

# Generation configuration
generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
}

# Initialize speech recognizer
recognizer = sr.Recognizer()


def get_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("Recognized:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def talk(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def commands():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'arthur' in command:
                command = command.replace('arthur', '').strip()
                return command
    except Exception as e:
        print(f"Error: {e}")
        return ""
    return ""


def weather(command):
    try:
        city = command.split("in", 1)[-1].strip()  # Extract city from the command
        soup = BeautifulSoup(requests.get(f"https://www.google.com/search?q=weather+in+{city}").text, "html.parser")
        region = soup.find("span", class_="BNeawe tAd8D AP7Wnd").text
        temp = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
        string = soup.find("div", class_="BNeawe tAd8D AP7Wnd").text
        data = string.split('\n')
        time = data[0]
        sky = data[1]
        talk(f"It is currently {temp} and {sky} in {region}")
        print(f"It is currently {temp} and {sky} in {region}")
    except Exception as e:
        print(f"Error: {e}")
        talk("Sorry, I couldn't fetch the weather information.")


def gemini_response(prompt):
    try:
        response = genai.generate_text(
            model="models/gemini-1.5-flash",  # Corrected model name format
            prompt={"text": prompt},  # Specify the prompt text
            temperature=0.7
        )
        return response.result.strip()
    except Exception as e:
        print(f"Google Gemini Error: {e}")
        return "Sorry, there was an error generating the response."


def run_arthur():
    voice_input = get_voice_input()
    if voice_input:
        command = voice_input.lower()
        print(command)
        if 'play' in command:
            song = command.replace('play', '').strip()
            talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            talk('Time Check, it is ' + time_now)
        elif 'what' in command:
            info = command.replace('what', '').strip()
            result = wikipedia.summary(info, sentences=1)
            print(result)
            talk(result)
        elif 'who' in command:
            info = command.replace('who', '').strip()
            result = wikipedia.summary(info, sentences=1)
            print(result)
            talk(result)
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'weather' in command:
            weather(command)
        else:
            response = gemini_response(command)
            talk(response)


if __name__ == "__main__":
    run_arthur()
