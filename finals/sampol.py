import os
import google.generativeai as genai
import speech_recognition as sr

# Set the API key (make sure this key is correct and valid)
os.environ['GOOGLE_API_KEY'] = 'AIzaSyDme7NsAOlmWPbwsZdOv9zsuZ-AgnWnVI0'

# Initialize the API client with the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 75

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


# Get voice input
voice_input = get_voice_input()

if voice_input:
    # Initialize GenerativeModel
    model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

    # Generate content based on voice input
    response = model.generate_content([voice_input])

    # Print the response
    for chunk in response:
        print(chunk.text, end="", flush=True)
