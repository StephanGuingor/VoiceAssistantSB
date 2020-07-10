"""
Programs for Computer
"""
from program import Program
from computer import Computer,stop

import webbrowser
import speech_recognition as sr
import os
import dotenv
import requests
from urllib.parse import urlencode
from urllib.request import urlretrieve
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

OWN_URL = 'REDIRECT_URL'
dotenv.load_dotenv('.env')


class Spotify:
    def __init__(self):
        pass
    
    @classmethod
    def parse_method(cls):
        pass
    @classmethod
    def spotify_login(cls):
        url = 'https://accounts.spotify.com/authorize?'
        params = {
            'client_id':os.getenv('SPOTIFY_CLIENT_ID'),
            'response_type':'token',
            'redirect_uri':OWN_URL,
            'scope':'user-read-currently-playing user-modify-playback-state',

        }
        prms = urlencode(params)
        webbrowser.open(url+prms)
    @classmethod
    def get_refreshed_token(cls):
        url = 'https://accounts.spotify.com/api/token'
        # x-www-url-encoded
        data = {"grant_type":"refresh_token",
                "refresh_token":os.getenv('AUTH_REFRESH')}

        try:
            # BASIC AUTH
            rsp = requests.post(url,data=data, auth=(os.getenv('SPOTIPY_CLIENT_ID'),os.getenv('SPOTIPY_CLIENT_SECRET')))
            
            rsp.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            content = rsp.json()
            access_token = content['access_token']
            print("New token: " + access_token)

            with open('.env','r') as fr:
                lines = fr.readlines()
                with open('.env','w') as fw:
                    for line in lines:
                        print(line)
                        if line.startswith("AUTH_TOKEN"):
                            fw.write(f"AUTH_TOKEN={access_token}\n\r")
                        else:
                            fw.write(line)
   
    @classmethod
    def spotify_get_name(cls):
        token = os.getenv('AUTH_TOKEN')
    
        rsp = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization':'Bearer ' + token})
        json = rsp.json()
        print(json['item']['name'])
    @classmethod
    def spotify_next(cls):
        token = os.getenv('AUTH_TOKEN')
        print(token)
        requests.post('https://api.spotify.com/v1/me/player/next',headers={'Authorization':'Bearer ' + token})

    

class ComputerController(Program):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.callback = self._callback
        self.audio_callback = self._audio_callback

    def _callback(self,x):
        print("Recording...")

    def _audio_callback(self,fname):
        print("INSIDE callback")
        r = sr.Recognizer()
        with sr.AudioFile(fname) as source:
            audio = r.record(source)  # read the entire audio file
        
        try:
            # can use gdp
            text = r.recognize_google(audio)
            print(text.lower().startswith('spotify'))
            if text.lower().startswith('youtube'):
                text = ''.join(text.lower().replace('youtube',''))
                print(text)
                if len(text) > 0:
                    webbrowser.open('https://www.youtube.com/results?search_query='+ "+".join(text.split(' ')))
                else:
                    webbrowser.open('https://www.youtube.com/')
            elif text.lower().startswith('spotify'):
                print("Calling Spotify")
                Spotify.spotify_next()
        except sr.UnknownValueError:
            print("No query recieved. Going to home page -->")
               
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        os.remove(fname)



class OpenYoutube(Program):
    def __init__(self,**kwargs):
        
        super().__init__(**kwargs)
        self.callback = self._callback

    def _callback(self,x):
        computer =  Computer()


        yt,recorder_callback = youtubeProgram()
     

        computer.add_program(yt)
      
        computer.timeout_start(20,audio_callback=recorder_callback)
        


def youtubeProgram():
    

    # Creating Youtube Keword 
    yt = Program('snowboy.umdl')
    
    def yt_callback(x): # called before recorder
        print("-----OPEN YOUTUBE CALLBACK-----")

    def recorder_callback(fname): # recieves recorded file
        print("Proccessing request...")
        r = sr.Recognizer()
        with sr.AudioFile(fname) as source:
            audio = r.record(source)  # read the entire audio file
    
        try:
            # can use gdp
            text = r.recognize_google(audio)
            webbrowser.open('https://www.youtube.com/results?search_query='+ "+".join(text.split(' ')))
        except sr.UnknownValueError:
            print("No query recieved. Going to home page -->")
            webbrowser.open('https://www.youtube.com/') # default / home page
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        os.remove(fname)


        yt.callback = yt_callback

    return yt,recorder_callback


if __name__ == "__main__":
    Spotify.get_refreshed_token()
