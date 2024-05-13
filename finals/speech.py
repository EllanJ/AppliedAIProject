import speech_recognition as sr

def arthur_recognize_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Capture audio from the default microphone
    with sr.Microphone() as source:
        print("Arthur is listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for audio input

    try:
        print("Arthur is recognizing...")
        # Use Google Speech Recognition to convert audio to text
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Arthur could not understand audio")
    except sr.RequestError as e:
        print("Arthur could not request results from Google Speech Recognition service; {0}".format(e))

# Example usage
recognized_text = arthur_recognize_speech()
