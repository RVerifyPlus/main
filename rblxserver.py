#!/usr/bin/env python3.7
# RVerifyPlus - A ROBLOX User Verficiation bot for discord.
# Copyright (C) 2018 - 2021 nolsen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import Flask, Response, request
import json
import os
import requests
import time
import logging
from time import gmtime, strftime, localtime
import re
app = Flask(__name__)

headers = {
    'User-Agent': 'RVerifyPlus - A ROBLOX User Verification Bot.'
}

logging.basicConfig(filename='logs.txt',
                            filemode='a',
                            format='%(message)s',
                            level=logging.INFO)

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

def find_key(d, value):
    for k,v in d.items():
        if isinstance(v, dict):
            p = find_key(v, value)
            if p:
               return [k] + p
        elif v == value:
            return [k]

def check(data, config):
    headersfordiscord = {
                          "Authorization": "Bot " + config["token"],
                          'User-Agent': 'RVerifyPlus - A ROBLOX User Verification Bot.'
    }

    # For Activity Tracker: Add new API to retrieve certain information, like discord ID.

    if "JOIN" in data['Status']:
        with open("db.json") as f:
            db = json.load(f)
            if "UserID" in data:
                try:
                    if "AltsPermitted" in data:
                        if data['AltsPermitted'] == "True":
                            if any(x for x in db.values() if x['userid'] == int(data['UserID'])):
                                with open("gameaccess/{}.json".format(data['GuildID'])) as z:
                                    gameaccess = json.load(z)
                                    discordid = str(find_key(db, int(data['UserID']))[0])
                                    if data['UserID'] in gameaccess:
                                        if gameaccess[data['UserID']]:
                                            if len(config[data['GuildID']]['game-logs']) > 3:
                                                if not os.path.exists('ratecache' + '/{}.channel.json'.format(data['GuildID'])):
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'wt') as inFile: inFile.write('{\n"X-RateLimit-Remaining": -9999,\n "X-RateLimit-Reset": "None"}')
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                        cache = json.load(h)
                                                else:
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                        cache = json.load(h)
                                                if cache['X-RateLimit-Remaining'] > 1 or cache['X-RateLimit-Remaining'] == -9999:
                                                    access_granted(data, config, db, cache)
                                                    return Response("True")
                                                else:
                                                    x = 1
                                                    while x == 1:
                                                        if int(cache['X-RateLimit-Reset']) < int(time.time()):
                                                            x = 2
                                                            access_granted(data, config, db, cache)
                                                            return Response("True")
                                            else:
                                                return Response("True")
                                        else:
                                            deny_notverified_userid(data, config, db)
                                            return Response("False")
                                    else:
                                        deny_notverified_userid(data, config, db)
                                        return Response("False")
                            else:
                                discordid = str(find_key(db, int(data['UserID']))[0])
                                with open("gameaccess/{}.json".format(data['GuildID'])) as z:
                                    gameaccess = json.load(z)
                                if discordid != None and str(db[discordid]['userid']) in gameaccess:
                                    if gameaccess[str(db[discordid]['userid'])]:
                                        if len(config[data['GuildID']]['game-logs']) > 3:
                                            if not os.path.exists('ratecache' + '/{}.channel.json'.format(data['GuildID'])):
                                                with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'wt') as inFile: inFile.write('{\n"X-RateLimit-Remaining": -9999,\n "X-RateLimit-Reset": "None"}')
                                                with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                    cache = json.load(h)
                                            else:
                                                with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                    cache = json.load(h)
                                            if cache['X-RateLimit-Remaining'] > 1 or cache['X-RateLimit-Remaining'] == -9999:
                                                access_granted(data, config, db, cache)
                                                return Response("True {}".format(db[discordid]['userid']))
                                            else:
                                                x = 1
                                                while x == 1:
                                                    if int(cache['X-RateLimit-Reset']) < int(time.time()):
                                                        x = 2
                                                        access_granted(data, config, db, cache)
                                                        return Response("True")
                                        else:
                                            return Response("True")
                                    else:
                                        deny_notverified_userid(data, config, db)
                                        return Response("False")
                                else:
                                    deny_notverified_userid(data, config, db)
                                    return Response("False")
                        if data['AltsPermitted'] == "Only":
                            discordid = str(find_key(db, int(data['UserID']))[0])
                            with open("gameaccess/{}.json".format(data['GuildID'])) as z:
                                gameaccess = json.load(z)
                                if discordid != None and str(data['UserID']) != db[discordid]['userid']:
                                    if str(db[discordid]['userid']) in gameaccess:
                                        if gameaccess[str(db[discordid]['userid'])]:
                                            if len(config[data['GuildID']]['game-logs']) > 3:
                                                if not os.path.exists('ratecache' + '/{}.channel.json'.format(data['GuildID'])):
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'wt') as inFile: inFile.write('{\n"X-RateLimit-Remaining": -9999,\n "X-RateLimit-Reset": "None"}')
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                        cache = json.load(h)
                                                else:
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                        cache = json.load(h)
                                                if cache['X-RateLimit-Remaining'] > 1 or cache['X-RateLimit-Remaining'] == -9999:
                                                    access_granted(data, config, db, cache)
                                                    return Response("True {}".format(db[discordid]['userid']))
                                                else:
                                                    x = 1
                                                    while x == 1:
                                                        if int(cache['X-RateLimit-Reset']) < int(time.time()):
                                                            x = 2
                                                            access_granted(data, config, db, cache)
                                                            return Response("True {}".format(db[discordid]['userid']))
                                            else:
                                                return Response("True {}".format(db[discordid]['userid']))
                                        else:
                                            deny_notverified_userid(data, config, db)
                                            return Response("False")
                                    else:
                                        deny_notverified_userid(data, config, db)
                                        return Response("False")
                                else:
                                    deny_notverified_userid(data, config, db)
                                    return Response("False")
                        if data['AltsPermitted'] == "False":
                            if any(x for x in db.values() if x['userid'] == int(data['UserID'])):
                                with open("gameaccess/{}.json".format(data['GuildID'])) as z:
                                    gameaccess = json.load(z)
                                    discordid = str(find_key(db, int(data['UserID']))[0])
                                    if data['UserID'] in gameaccess:
                                        if gameaccess[data['UserID']]:
                                            if len(config[data['GuildID']]['game-logs']) > 3:
                                                if not os.path.exists('ratecache' + '/{}.channel.json'.format(data['GuildID'])):
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'wt') as inFile: inFile.write('{\n"X-RateLimit-Remaining": -9999,\n "X-RateLimit-Reset": "None"}')
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                        cache = json.load(h)
                                                else:
                                                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                        cache = json.load(h)
                                                if cache['X-RateLimit-Remaining'] > 1 or cache['X-RateLimit-Remaining'] == -9999:
                                                    access_granted(data, config, db, cache)
                                                    return Response("True")
                                                else:
                                                    x = 1
                                                    while x == 1:
                                                        if int(cache['X-RateLimit-Reset']) < int(time.time()):
                                                            x = 2
                                                            access_granted(data, config, db, cache)
                                                            return Response("True")
                                            else:
                                                return Response("True")
                                        else:
                                            deny_notverified_userid(data, config, db)
                                            return Response("False")
                                    else:
                                        deny_notverified_userid(data, config, db)
                                        return Response("False")
                    else: # Backwards compatibility with older scripts that lack alt support.
                        if any(x for x in db.values() if x['userid'] == int(data['UserID'])):
                            with open("gameaccess/{}.json".format(data['GuildID'])) as z:
                                gameaccess = json.load(z)
                                discordid = str(find_key(db, int(data['UserID']))[0])
                                if data['UserID'] in gameaccess:
                                    if gameaccess[data['UserID']]:
                                        if len(config[data['GuildID']]['game-logs']) > 3:
                                            if not os.path.exists('ratecache' + '/{}.channel.json'.format(data['GuildID'])):
                                                with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'wt') as inFile: inFile.write('{\n"X-RateLimit-Remaining": -9999,\n "X-RateLimit-Reset": "None"}')
                                                with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                    cache = json.load(h)
                                            else:
                                                with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                                                    cache = json.load(h)
                                            if cache['X-RateLimit-Remaining'] > 1 or cache['X-RateLimit-Remaining'] == -9999:
                                                access_granted(data, config, db, cache)
                                                return Response("True")
                                            else:
                                                x = 1
                                                while x == 1:
                                                    if int(cache['X-RateLimit-Reset']) < int(time.time()):
                                                        x = 2
                                                        access_granted(data, config, db, cache)
                                                        return Response("True")
                                        else:
                                            return Response("True")
                                    else:
                                        deny_notverified_userid(data, config, db)
                                        return Response("False")
                                else:
                                    deny_notverified_userid(data, config, db)
                                    return Response("False")
                except KeyError:
                    return Response("DBError")
            else:
                return Response("False")

    if "ROLECHECK" in data['Status']:
        with open("db.json") as f:
            db = json.load(f)
        if "UserID" in data:
            if any(x for x in db.values() if x['userid'] == int(data['UserID'])):
                with open("gameaccess/{}.json".format(data['GuildID'])) as z:
                    gameaccess = json.load(z)
                    discordid = str(find_key(db, int(data['UserID']))[0])
                    if data['UserID'] in gameaccess:
                        if gameaccess[data['UserID']]:
                            if not os.path.exists('ratecache' + '/{}.guild.json'.format(data['GuildID'])):
                                with open('ratecache' + '/{}.guild.json'.format(data['GuildID']), 'wt') as inFile: inFile.write('{\n"X-RateLimit-Remaining": -9999,\n "X-RateLimit-Reset": "None"}')
                                with open('ratecache' + '/{}.guild.json'.format(data['GuildID'])) as h:
                                    cache = json.load(h)
                            else:
                                with open('ratecache' + '/{}.guild.json'.format(data['GuildID'])) as h:
                                    cache = json.load(h)
                            if cache['X-RateLimit-Remaining'] > 2 or cache['X-RateLimit-Remaining'] == -9999:
                                r = requests.get("https://discordapp.com/api/guilds/{}/members/{}".format(data['GuildID'], discordid), headers=headersfordiscord)
                                print(r.headers.get('X-RateLimit-Remaining'))
                                print(r.status_code)
                                js = r.json()
                                if str(r.status_code) == "429":
                                    print("Alert: We have hit discord's API limit.")
                                    sys.exit()
                                if r.headers.get('X-RateLimit-Remaining') == '1':
                                    print("Almost hitting the ratelimit!")
                                cache['X-RateLimit-Remaining'] = int(r.headers.get('X-RateLimit-Remaining'))
                                cache['X-RateLimit-Reset'] = int(r.headers.get('X-RateLimit-Reset'))
                                with open('ratecache' + '/{}.guild.json'.format(data['GuildID']), 'w') as h:
                                    json.dump(cache, h, indent=2)
                                try:
                                    return Response(json.dumps(js['roles']))
                                except KeyError:
                                    print(discordid)
                                    print(data['GuildID'])
                                    return Response("Fail")
                            else:
                                x = 1
                                while x == 1:
                                    if int(cache['X-RateLimit-Reset']) < int(time.time()):
                                        x = 2
                                        r = requests.get("https://discordapp.com/api/guilds/{}/members/{}".format(data['GuildID'], discordid), headers=headersfordiscord)
                                        print(r.headers.get('X-RateLimit-Remaining'))
                                        print(r.status_code)
                                        js = r.json()
                                        if str(r.status_code) == "429":
                                            print("Alert: We have hit discord's API limit.")
                                            sys.exit()
                                        if r.headers.get('X-RateLimit-Remaining') == '1':
                                            print("Almost hitting the ratelimit!")
                                        cache['X-RateLimit-Remaining'] = int(r.headers.get('X-RateLimit-Remaining'))
                                        cache['X-RateLimit-Reset'] = int(r.headers.get('X-RateLimit-Reset'))
                                        with open('ratecache' + '/{}.guild.json'.format(data['GuildID']), 'w') as h:
                                            json.dump(cache, h, indent=2)
                                        try:
                                            return Response(json.dumps(js['roles']))
                                        except KeyError:
                                            print(discordid)
                                            print(data['GuildID'])
                                            return Response("Fail")
                    else:
                        return Response("False")
            else:
                return Response("False")
        else:
            return Response("Error: Missing UserID in POST request.")

def access_granted(data, config, db, cache):
    headersfordiscord = {
                          "Authorization": "Bot " + config["token"],
                          'User-Agent': 'RVerifyPlus - A ROBLOX User Verification Bot.'
    }
    text = "({} EST) {} has joined the server!".format(strftime("%H:%M:%S", localtime()), db[find_key(db, int(data['UserID']))[0]]['rblxusername'])
    r = requests.post("https://discordapp.com/api/channels/{}/messages".format(config[data['GuildID']]['game-logs']), json={"content": text}, headers=headersfordiscord)
    print(r.headers.get('X-RateLimit-Remaining'))
    #print(r.headers.get('X-RateLimit-Reset'))
    if str(r.status_code) == "429":
        print("Alert: We have hit discord's API limit.")
        sys.exit()
    if r.headers.get('X-RateLimit-Remaining') == '1':
        print("Almost hitting the ratelimit!")
    cache['X-RateLimit-Remaining'] = int(r.headers.get('X-RateLimit-Remaining'))
    cache['X-RateLimit-Reset'] = int(r.headers.get('X-RateLimit-Reset'))
    with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'w') as h:
        json.dump(cache, h, indent=2)

def deny_notverified_userid(data, config, db):
    if len(config[data['GuildID']]['game-logs']) > 3:
        headersfordiscord = {
                              "Authorization": "Bot " + config["token"],
                              'User-Agent': 'RVerifyPlus - A ROBLOX User Verification Bot.'
        }
        r = requests.get('https://api.roblox.com/users/{}/'.format(data['UserID']), headers=headers)
        js = r.json()
        text = "({} EST) {} attempted to join the server, but wasn\'t verified.".format(strftime("%H:%M:%S", localtime()), js['Username'])

        if not os.path.exists('ratecache' + '/{}.channel.json'.format(data['GuildID'])):
            with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'wt') as inFile: inFile.write('{\n"X-RateLimit-Remaining": -9999,\n "X-RateLimit-Reset": "None"}')
            with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                cache = json.load(h)
        else:
            with open('ratecache' + '/{}.channel.json'.format(data['GuildID'])) as h:
                cache = json.load(h)
        if cache['X-RateLimit-Remaining'] > 2 or cache['X-RateLimit-Remaining'] == -9999:
            r = requests.post("https://discordapp.com/api/channels/{}/messages".format(config[data['GuildID']]['game-logs']), json={"content": text}, headers=headersfordiscord)
            print(r.headers.get('X-RateLimit-Remaining'))
            print(r.status_code)
            if r.headers.get('X-RateLimit-Remaining') == '1':
                print("Almost hitting the ratelimit!")
            cache['X-RateLimit-Remaining'] = int(r.headers.get('X-RateLimit-Remaining'))
            cache['X-RateLimit-Reset'] = int(r.headers.get('X-RateLimit-Reset'))
            with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'w') as h:
                json.dump(cache, h, indent=2)
            if str(r.status_code) == "429":
                sys.exit()
                print("Alert: We have hit discord's API limit.")

        else:
            x = 1
            while x == 1:
                if int(cache['X-RateLimit-Reset']) < int(time.time()):
                    x = 2
                    text = "({} EST) {} attempted to join the server, but wasn\'t verified.".format(strftime("%H:%M:%S", localtime()), js['Username'])
                    r = requests.post("https://discordapp.com/api/channels/{}/messages".format(config[data['GuildID']]['game-logs']), json={"content": text}, headers=headersfordiscord)
                    print(r.headers.get('X-RateLimit-Remaining'))
                    print(r.status_code)
                    if r.status_code == "429":
                        print("Alert: We have hit discord's API limit.")
                        sys.exit()
                    if r.headers.get('X-RateLimit-Remaining') == '1':
                        print("Almost hitting the ratelimit!")
                    cache['X-RateLimit-Remaining'] = int(r.headers.get('X-RateLimit-Remaining'))
                    cache['X-RateLimit-Reset'] = int(r.headers.get('X-RateLimit-Reset'))
                    with open('ratecache' + '/{}.channel.json'.format(data['GuildID']), 'w') as h:
                        json.dump(cache, h, indent=2)
        return

def accept_verified_userid(data):
    text = "({} EST) {} has joined the server!".format(strftime("%H:%M:%S", localtime()), db[find_key(db, int(data['UserID']))[0]]['rblxusername'])

@app.route('/api/request/',methods=['POST'])
def foo():
   data = json.loads(request.data)
   print(data)
   with open("config.json") as g:
       config = json.load(g)
   if data['GuildID'] in config:
       if config[data['GuildID']]['gameaccess']:
           if data['ServerAPIKey'] == config[data['GuildID']]['serverapikey']:
               return check(data, config)
           else:
               if config[data['GuildID']]['sharedapikey']['Enabled']:
                   if data['ServerAPIKey'] == config[data['GuildID']]['sharedapikey']['key']:
                       return check(data, config)
                   else:
                       #print("Or this")
                       return Response("InvalidSharedKey")
               else:
                   #print("Debug: GuildID doesn't have valid key")
                   return Response("InvalidKey")
       else:
           #print("Debug: GuildID doesn't have GA enabled.")
           return Response("GANotEnabled")
   else:
       #print("Debug: GuildID not in Config")
       return Response("InvalidGuildID")

if __name__ == '__main__':
    app.run(threaded=True)
