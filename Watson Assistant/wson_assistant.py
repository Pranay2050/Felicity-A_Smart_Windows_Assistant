from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def initialize_assistant(string):
    authenticator = IAMAuthenticator('IBM Service API Key')
    assistant = AssistantV1(
        version='2018-07-10',
        authenticator=authenticator)
    assistant.set_service_url('https://api.eu-gb.assistant.watson.cloud.ibm.com')
    assistant.set_http_config({'timeout': 100})
    
    response = assistant.message(workspace_id='Assistant ID', input={
        'text': string}).get_result()
    return(response["output"]["text"][0])
