import streamlit as st
import speech_recognition as sr
import datetime
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import google.generativeai as genai


recognizer = sr.Recognizer()
os.environ['GOOGLE_API_KEY'] = 'AIzaSyDme7NsAOlmWPbwsZdOv9zsuZ-AgnWnVI0'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 80
}

def get_voice_input():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        st.write("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.write("Could not understand audio")
        return None
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def talk(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def weather(command):
    try:
        city = command.split("in", 1)[-1].strip()
        soup = BeautifulSoup(requests.get(f"https://www.google.com/search?q=weather+in+{city}").text, "html.parser")
        region = soup.find("span", class_="BNeawe tAd8D AP7Wnd").text
        temp = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
        string = soup.find("div", class_="BNeawe tAd8D AP7Wnd").text
        data = string.split('\n')
        time = data[0]
        sky = data[1]
        response = f"It is currently {temp} and {sky} in {region}"
        talk(response)
        st.write(f"Arthur's Response: {response}")
    except Exception as e:
        error_message = "Sorry, I couldn't fetch the weather information."
        st.write(f"Error: {e}")
        talk(error_message)
        st.write(f"Arthur's Response: {error_message}")

def open_application(command):
    app_opened = False
    if 'chrome' in command:
        talk("Opening Google Chrome")
        subprocess.Popen('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.exe')
        app_opened = True
    elif 'notepad' in command:
        talk("Opening Notepad")
        subprocess.Popen('notepad.exe')
        app_opened = True
    elif 'paint' in command:
        talk("Opening Paint")
        subprocess.Popen('mspaint.exe')
        app_opened = True
    elif 'word' in command:
        talk("Opening Microsoft Word")
        subprocess.Popen('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.exe')
        app_opened = True
    elif 'excel' in command:
        talk("Opening Microsoft Excel")
        subprocess.Popen('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel.exe')
        app_opened = True
    elif 'powerpoint' in command:
        talk("Opening Microsoft PowerPoint")
        subprocess.Popen('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint.exe')
        app_opened = True
    if not app_opened:
        response = "Sorry, I am not able to open that application."
        talk(response)
        st.write(f"Arthur's Response: {response}")

def process_user_input(user_input):
    command = user_input.lower()
    st.write(f"User Input: {command}")

    if 'play' in command:
        song = command.replace('play', '').strip()
        response = 'playing now'
        talk(response)
        pywhatkit.playonyt(song)
        st.write(f"Arthur's Response: {response}")
        st.write('Playing now...')

    elif 'time' in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        response = 'Time Check, it is ' + time_now
        talk(response)
        st.write(f"Arthur's Response: {response}")
    elif 'date' in command:
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        response = 'The date today is ' + current_date
        talk(response)
        st.write(f"Arthur's Response: {response}")
    elif 'what' in command:
        info = command.replace('what', '').strip()
        result = wikipedia.summary(info, sentences=1)
        talk(result)
        st.write(f"Arthur's Response: {result}")
    elif 'who' in command:
        info = command.replace('who', '').strip()
        result = wikipedia.summary(info, sentences=1)
        talk(result)
        st.write(f"Arthur's Response: {result}")
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        st.write(f"Arthur's Response: {joke}")
    elif 'open' in command:
        open_application(command)
    elif 'weather' in command:
        weather(command)
    else:
        model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
        response = model.generate_content([user_input])
        for chunk in response:
            st.write(f"Arthur's Response: {chunk.text}")
            talk(chunk.text)

def main():
    st.title("Arthur Voice Assistant")
    st.markdown("---")
    st.write("Press Activate Arthur to start.")

    if st.button("Activate Arthur"):
        st.write("Listening...")
        recognized_text = get_voice_input()
        if recognized_text:
            process_user_input(recognized_text)

if __name__ == "__main__":
    main()
