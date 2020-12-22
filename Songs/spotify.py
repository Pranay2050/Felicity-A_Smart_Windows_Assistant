import requests
import base64
import datetime
from urllib.parse import urlencode
import webbrowser

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        
    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("Must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
        
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization" : f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data = token_data, headers=token_headers)
        #print(r.json())

        if r.status_code not in range(200,299):
            raise Exception("Could not authenticate client.")
            #return False
        data = r.json()

        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']

        expires = now + datetime.timedelta(seconds=expires_in)
        
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        did_expire = expires < now
        return True
    
    def get_access_token(self):
        token=self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
     
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
    
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')
    
    def get_track(self, _id):
        return self.get_resource(_id, resource_type='tracks')
    
    def search(self, query, search_type="track"):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q" : query, "type" : search_type.lower()})

        lookup_url = f"{endpoint}?{data}"

        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200,299):
            return{}
        return r.json()
        
def play_on_spotify(song):
    client_id = "6176e0ed457146b59388f66d280f790d"
    client_secret = "c6b6986d41d24a3c9107521589f6ae69"

    client = SpotifyAPI(client_id, client_secret)
    r = client.search(song, search_type="track")
    URLS = r['tracks']['items'][0]["external_urls"]["spotify"]
    webbrowser.open(URLS, new=2, autoraise=False)