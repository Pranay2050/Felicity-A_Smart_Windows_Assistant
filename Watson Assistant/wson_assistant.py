from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def initialize_assistant(string):
    authenticator = IAMAuthenticator('ElOVnbZ2oF0gCU8IVGtDdwvT1UAg_5jBAC6dSUVL5De0')
    assistant = AssistantV1(
        version='2018-07-10',
        authenticator=authenticator)
    assistant.set_service_url('https://api.eu-gb.assistant.watson.cloud.ibm.com')
    assistant.set_http_config({'timeout': 100})
    
    response = assistant.message(workspace_id='3f9677d5-cadf-4856-81be-36173e8d5eeb', input={
        'text': string}).get_result()
    return(response["output"]["text"][0])