from pip._vendor.requests import get
import re
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from os import environ

load_dotenv()
track_url = input('Enter a Spotify track URL: ')
match = re.findall(r"[\bhttps://open.\b]*spotify[\b.com\b]*[/:]*track[/:]*[A-Za-z0-9?=]+", track_url)

while len(match) == 0:
	track_url = input('Enter a valid Spotify track URL: ')
	match = re.findall(r"[\bhttps://open.\b]*spotify[\b.com\b]*[/:]*track[/:]*[A-Za-z0-9?=]+", track_url)

print('Gathering geolocation...')

ip: str = get('https://api.ipify.org').text
res = json.loads(get(f'https://geolocation-db.com/jsonp/\'{ip}').content.decode().split("(")[1].strip(")"))

print(f'\nDiscovered geolocation: {res["country_name"]} ({res["country_code"]})')
print('\nGathering track metadata...')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=environ.get('CLIENT_ID'), client_secret=environ.get('CLIENT_SECRET')))
track = sp.track(track_url)

print('\nIdentified track:')

if len(track["artists"]) == 1: 
	artist = track["artists"][0]["name"] 
else: artist = ", ".join([artist["name"] for artist in track["artists"]])

print(f'\t{track["name"]} - {artist}')

if res["country_code"] in track["available_markets"]:
	print('\nThis track is available in your current region!')
else: print('\nThis track is not available in your current region.')