import json
import requests
import websockets
import asyncio
import os
import datetime, time
from colorama import Fore
os.system('cls')
os.system('title Spotify websocket python example by Linguini')
token = ''
async def get_access():
    r = json.loads(requests.get('https://canary.discord.com/api/v9/users/@me/connections', headers={'authorization': token}).text)
    for thing in r:
        if thing['type'] == 'spotify':
            access_token = thing['access_token']
            return access_token


def get_time():
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	current_time = str(current_time)
	final_time = current_time.split(':')
	if int(final_time[0]) > 12:
		timmy = int(final_time[0])-12
		halftime = 'PM'
	else:
		timmy = final_time[0]
		halftime = 'AM'
		if timmy == '00':
			timmy = '12'
	current_time = f'{timmy}:{final_time[1]} {halftime}'
	return current_time

def printer(msg):
    print(f"{Fore.MAGENTA}[{get_time()}] {Fore.LIGHTBLUE_EX}>{Fore.RESET} {Fore.LIGHTMAGENTA_EX}{msg}{Fore.RESET}")

async def on_player_state_change(d):
    artistnames = []
    current = d['event']['state']['item']['name']
    artistlist = d['event']['state']['item']['artists']
    playing = bool(d['event']['state']['is_playing'])
    volume = d['event']['state']['device']['volume_percent']
    #print(current)
    for thing in artistlist:
        artistnames.append(thing['name'])
        artists = ', '.join(artistnames)
    if playing:
        printer(f"Playing: {Fore.LIGHTRED_EX}{current}{Fore.LIGHTMAGENTA_EX} By {Fore.LIGHTCYAN_EX}{artists} {Fore.LIGHTGREEN_EX}at {volume}% volume. ")
    else:
        printer(f"Stopped: {Fore.LIGHTRED_EX}{current}{Fore.LIGHTMAGENTA_EX} By {Fore.LIGHTCYAN_EX}{artists} {Fore.LIGHTGREEN_EX}at {volume}% volume.")


async def gateway():
    auth = await get_access()
    async with websockets.connect(f'wss://dealer.spotify.com/?access_token={auth}') as ws:
        connect_id = json.loads(await ws.recv())['headers']['Spotify-Connection-Id']
        notifying = json.loads(requests.put(f'https://api.spotify.com/v1/me/notifications/player?connection_id={connect_id}&access_token={auth}').text)
        print(f"{Fore.GREEN}{notifying['message']}{Fore.RESET}")
        while True:
            try:
                raw = json.loads(await ws.recv())['payloads'][0]['events'][0]
                event_type = raw['type']
                if event_type == 'PLAYER_STATE_CHANGED':
                    await on_player_state_change(raw)
                #print(event_type)
            except:
                pass


asyncio.run(gateway())