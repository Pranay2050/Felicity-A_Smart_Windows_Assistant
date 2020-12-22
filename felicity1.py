import run_apps
import wson_assistant
import speech
import youtube
import spotify
import open_directories
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def initialize_assistant():
    authenticator = IAMAuthenticator('ElOVnbZ2oF0gCU8IVGtDdwvT1UAg_5jBAC6dSUVL5De0')
    return AssistantV1(
        version='2018-07-10',
        authenticator=authenticator)
    assistant.set_service_url('https://api.eu-gb.assistant.watson.cloud.ibm.com')
    assistant.set_http_config({'timeout': 100})

def initialize_felicity():
    app_dict = run_apps.initialize_app_dict()
    return app_dict

def process_query(app_dict):
    
    query = speech.get_speech()
    assistant_response = wson_assistant.initialize_assistant(query)
    #print(assistant_response)
    if "|" not in assistant_response:
        print("I could not understand you...please try again!!")
        return
    response = assistant_response.split("|")
    #print(response)
    if response[0] == "play":
        
        if len(response) == 2:
            print("Playing your request on Youtube")
            youtube.play_on_youtube(response[1])
            
        elif len(response) == 3:
            if response[2] == "youtube":
                print("Playing",response[1], "on Youtube")
                youtube.play_on_youtube(response[1])

            elif response[2]== "spotify":
                print("Playing",response[1], "on Spotify")
                spotify.play_on_spotify(response[1])
                
            else:
                print("Playing",response[1], "on Youtube")
                youtube.play_on_youtube(response[1])
                
        else:
            print("Could not decide what to play from the data...Please try again!!!")
                
    elif response[0] == "run":
        run_apps.run_app(response[1], app_dict)
        
    elif response[0] == "open":
        open_directories.open_child(response[1])
