import speech_recognition as sr

def get_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)


    HOUNDIFY_CLIENT_ID = "Client ID"  # Houndify client IDs are Base64-encoded strings
    HOUNDIFY_CLIENT_KEY = "Client Key"  # Houndify client keys are Base64-encoded strings
    try:
        recog = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
        print("You Said :",recog)
        return (recog)
    except sr.UnknownValueError:
        print("Houndify could not understand audio")
        return ("Houndify could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Houndify service; {0}".format(e))
        return("Could not request results from Houndify service; {0}".format(e))
