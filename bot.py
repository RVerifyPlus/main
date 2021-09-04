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

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import traceback
import asyncio
import time
import json
import datetime
from sys import exit
import random
import string
import re
import aiohttp
from bs4 import BeautifulSoup
import os
from multiprocessing import Process
import logging
import sys
import uuid
import requests
import platform
import bcrypt
import core.newsettingsfunc as newsettingsfunc

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

headers = {
    'User-Agent': 'RVerifyPlus - A ROBLOX User Verification Bot.'
}

noobshirts = {
'https://www.roblox.com/catalog/382537085/I-3-Pizza-Shirt',
'https://www.roblox.com/catalog/382537702/Teal-Shirt',
'https://www.roblox.com/catalog/144076436/Grey-Striped-Shirt-with-Denim-Jacket',
'https://www.roblox.com/catalog/144076358/Blue-and-Black-Motorcycle-Shirt',
'https://www.roblox.com/catalog/144076760/Dark-Green-Jeans',
'https://www.roblox.com/catalog/382538295/Guitar-Tee-with-Black-Jacket'

}

noobpants = {
'https://www.roblox.com/catalog/144076512/Pink-Jeans',
'https://www.roblox.com/catalog/382537806/Jean-Shorts',
'https://www.roblox.com/catalog/382537569/Black-Jeans',
'https://www.roblox.com/catalog/144076760/Dark-Green-Jeans'
}

noobfaces = {
'https://www.roblox.com/catalog/86487766/Woman-Face',
'https://www.roblox.com/catalog/86487700/Man-Face'
}

noobhair = {
'https://www.roblox.com/catalog/62724852/Chestnut-Bun',
'https://www.roblox.com/catalog/376526888/Straight-Blonde-Hair',
'https://www.roblox.com/catalog/376527350/Black-Ponytail',
'https://www.roblox.com/catalog/376548738/Brown-Charmer-Hair',
'https://www.roblox.com/catalog/376524487/Blonde-Spiked-Hair',
'https://www.roblox.com/catalog/62234425/Brown-Hair',
'https://www.roblox.com/catalog/63690008/Pal-Hair'
}

with open("config.json") as g:
    config = json.load(g)

with open("db.json") as f:
    db = json.load(f)

with open("wordlist.json") as h:
    wordlist = json.load(h)

with open("nomigration.json") as n:
    nomigration = json.load(n)

with open("complaintcounter.json") as n:
    complaintcounter = json.load(n)

#with open("activitylog.json") as n:
#    activitylog = json.load(n)

date_format = "%m/%d/%Y"

def check(reaction, user):
    if user.id != client.user.id:
        return True

#async def verifycode_generator(size=7, chars=string.ascii_uppercase + string.ascii_lowercase):
 #return ''.join(random.choice(chars) for _ in range(size))

dblheaders = {"Authorization": config['dbltoken']}

get_roblox_id = "https://api.roblox.com/users/get-by-username?username={}"

async def checkPrefix(bot, msg):
    #if msg.guild != None:
        #if str(msg.author.id) in db:
            #if str(msg.guild.id) in activitylog:
                #activitylog[str(msg.guild.id)][str(msg.author.id)] = int(time.time())
                #with open('activitylog.json', 'w') as t:
                    #json.dump(activitylog, t, indent=2)
            #else:
                #activitylog[str(msg.guild.id)] = {}
                #activitylog[str(msg.guild.id)][str(msg.author.id)] = int(time.time())
                #with open('activitylog.json', 'w') as t:
                    #json.dump(activitylog, t, indent=2)
    if msg.guild != None:
        #if client.user.mentioned_in(msg):
                #author.send()
        #else:
            #return config[str(msg.guild.id)]['prefix']
        return config[str(msg.guild.id)]['prefix']
    else:
        return config['defaultprefix']

intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(intents=intents, command_prefix = checkPrefix, description="A Roblox Verification Bot.")
client.remove_command("help")

def find_key(d, value):
    for k,v in d.items():
        if isinstance(v, dict):
            p = find_key(v, value)
            if p:
                #return [k] + p
                return True
        elif v == value:
            return [k]
            #return False

def find_key2(d, value):
    for k,v in d.items():
        if isinstance(v, dict):
            p = find_key2(v, value)
            if p:
               return [k] + p
        elif v == value:
            return [k]

def verifycode_generator():
 i = 0
 while i == 0:
     safemessage = []
     for i in range(8):
         word_to_use = random.choice(wordlist["words"])
         safemessage.append(word_to_use)
         result = " ".join(safemessage)
     if result in db:
         i = 0
     else:
        i = 1
        return result

def deletecheck(message):
    count = 0
    for x in db[str(message.author.id)]['alts']:
        if x == 'count':
            pass
        else:
            if count == db[str(message.author.id)]['alts']['count']:
                return False
            else:
                if len(db[str(message.author.id)]['alts'][str(x)]['verifycode']) < 3:
                    pass
                else:
                    return x

def noobdetectionsys(html):
    shirt = 0
    pants = 0
    faces = 0
    hair = 0
    for x in noobshirts:
        if x.encode('utf-8') in html:
            shirt = 1
    for x in noobpants:
        if x.encode('utf-8') in html:
            pants = 1
    for x in noobfaces:
        if x.encode('utf-8') in html:
            faces = 1
    for x in noobhair:
        if x.encode('utf-8') in html:
            hair = 1
    count = shirt + pants + faces + hair
    if count == None:
        return None
    else:
        return count


async def checkage(authorid, server, client, authorroles, author, altverify, altaccount):
    #async with aiohttp.get('https://api.roblox.com/users/{}/groups'.format(db[authorid]['userid']), headers=headers) as r:
        #if r.status == 200:
           #html = await r.read()
           #if '3514227'.encode('utf-8') in html or '1200769'.encode('utf-8') in html or '2868472'.encode('utf-8') in html:
               #await client.send_message(client.get_channel(config[guild.id]['rverifyplus-alerts']), "**DEBUG Alert**: The account '{}' is in a suspicious group. Discord: <@{}>\n<@{}>'s profile: https://www.roblox.com/users/{}/profile".format(db[authorid]['rblxusername'], authorid,authorid,db[authorid]['userid']))
    async with aiohttp.ClientSession(loop=loop) as session:
        if not altverify:
            async with session.get(get_roblox_id.format(db[str(authorid)]['rblxusername']), headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    db[str(authorid)]['rblxusername'] = js['Username']
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
                    await session.close()
        else:
            async with session.get(get_roblox_id.format(db[str(authorid)]['alts'][altaccount]['rblxusername']), headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    if js['Username'] not in db[str(authorid)]['alts']:
                        newusername = js['Username']
                        del db[str(authorid)]['alts'][altaccount]
                        db[str(authorid)]['alts'][newusername] = {}
                        db[str(authorid)]['alts'][newusername]['userid'] = js['Id']
                        db[str(authorid)]['alts'][newusername]['verifycode'] = ""
                        db[str(authorid)]['alts'][newusername]['rblxusername'] = js['Username']
                        altaccount = js['Username']
                        with open('db.json', 'w') as f:
                            json.dump(db, f, indent=2)
                await session.close()
    async with aiohttp.ClientSession(loop=loop) as session:
        userid_select = db[str(authorid)]['userid']
        if altverify:
            userid_select = db[str(authorid)]['alts'][altaccount]['userid']
        async with session.get('https://users.roblox.com/v1/users/{}'.format(userid_select), headers=headers) as r:
            if r.status == 200:
                js2 = await r.json()
                today = datetime.date.today().strftime('%m/%d/%Y')
                rawdateTime = datetime.datetime.strptime(js2['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
                Date = "{}/{}/{}".format(rawdateTime.month, rawdateTime.day, rawdateTime.year) # Thank you Roblox, for changing your website to make my lazy ass to use the API instead of scraping the website.
                a = datetime.datetime.strptime(Date, "%m/%d/%Y")
                b = datetime.datetime.strptime(today, "%m/%d/%Y")
                delta = b - a
                Date = Date.split()[0]
                server = client.get_guild(server.id)
                memberid = server.get_member(authorid)
                await session.close()
                if not altverify:
                        if "unverifiedrole" in config[str(server.id)]:
                            if config[str(server.id)]['unverifiedrole'] in [role.id for role in author.roles]:
                                removeunrole = discord.utils.get(server.roles, id=config[str(server.id)]['unverifiedrole'])
                                await memberid.remove_roles(removeunrole, reason="User has verified")
                if len(str(config[str(server.id)]['verified-logs'])) > 3:
                    perms = client.get_channel(config[str(server.id)]['verified-logs']).permissions_for(server.me)
                    try:
                        if not perms.embed_links:
                            getchannel = client.get_channel(config[str(server.id)]['verified-logs'])
                            if not altverify:
                                await getchannel.send("**User Verified** <@{}> as {}\nhttps://www.roblox.com/users/{}/profile\nAccount was created on {}\n<@{}>\'s account is {} days old".format(str(authorid), db[str(authorid)]['rblxusername'], Date, delta.days))
                            else:
                                await getchannel.send("**User (alt) Verified** <@{}> as {}\nhttps://www.roblox.com/users/{}/profile\nAccount was created on {}\n<@{}>\'s account is {} days old".format(str(authorid), db[str(authorid)]['alts'][altaccount]['rblxusername'], db[str(authorid)]['alts'][altaccount]["userid"], Date, delta.days))
                        else:
                            async with aiohttp.ClientSession(loop=loop) as sessionthumbnail:
                                async with sessionthumbnail.get('https://thumbnails.roblox.com/v1/users/avatar?userIds={}&size=100x100&format=Png&isCircular=false'.format(userid_select), headers=headers) as t:
                                    if r.status == 200:
                                        js2 = await t.json()
                                        if 'data' in js2:
                                            for x in js2['data']: # This is the most jankiest way of getting this damn link from a dict oh my god.
                                                try:
                                                    thumbnailurl = x['imageUrl']
                                                except:
                                                    pass
                                            await session.close()
                                            getchannel = client.get_channel(config[str(server.id)]['verified-logs'])
                                            profilecreationdate = Date
                                            if not altverify:
                                                embed = discord.Embed(title="User Verified - {}".format(db[str(authorid)]['rblxusername']), colour=discord.Colour(0x3dff), url="https://www.roblox.com/users/{}/profile".format(userid_select), description="Account Created on {}\nAccount is {} days old\nDiscord: <@{}>".format(profilecreationdate, delta.days, str(authorid)))
                                            else:
                                                embed = discord.Embed(title="User (alt) Verified - {}".format(db[str(authorid)]['alts'][altaccount]['rblxusername']), colour=discord.Colour(0x3dff), url="https://www.roblox.com/users/{}/profile".format(userid_select), description="Account Created on {}\nAccount is {} days old\nDiscord: <@{}>".format(profilecreationdate, delta.days, str(authorid)))
                                            if thumbnailurl != None:
                                                embed.set_thumbnail(url=thumbnailurl)
                                            embed.set_footer(text="RVerifyPlus", icon_url="https://rverifyplus.xyz/wp-content/uploads/2018/10/cropped-rlogo2compressed-32x32.png")
                                            await getchannel.send(embed=embed)
                    except discord.Forbidden:
                        pass
                if delta.days < int(config[str(server.id)]['minage']):
                    if not altverify:
                            if len(str(config[str(server.id)]['rverifyplus-alerts'])) > 3:
                                try:
                                    getchannel = client.get_channel(config[str(server.id)]['rverifyplus-alerts'])
                                    await getchannel.send("**Alert**: The account '{}' is less than 90 days old. Discord: <@{}>\n<@{}>'s profile: https://www.roblox.com/users/{}/profile".format(db[str(authorid)]['rblxusername'], str(authorid),str(authorid),db[str(authorid)]['userid']))
                                except discord.errors.InvalidArgument:
                                    print("DEBUG: The channel {}, doesn't exist on {}".format(config[str(server.id)]['rverifyplus-alerts'],server.name))
                            if len(str(config[str(server.id)]['blacklistedrole'])) > 3:
                                rolepoints = -1
                            else:
                                rolepoints = 1

                    else:
                        rolepoints = 1
                else:
                    rolepoints = 1

                if config[str(server.id)]['noobdetection']['Enabled']:
                     async with aiohttp.ClientSession(loop=loop) as session:
                         userid_select = db[str(authorid)]['userid']
                         if altverify:
                             userid_select = db[str(authorid)]['alts'][altaccount]['userid']
                             async with session.get('https://www.roblox.com/users/{}/profile'.format(userid_select), headers=headers) as r:
                                 if r.status == 200:
                                     html = await r.read()
                                     count = noobdetectionsys(html)
                                     session.close()
                                     if not altverify:
                                         try:
                                             if count >= config[str(server.id)]['noobdetection']['level']:
                                                 if len(str(config[str(server.id)]['blacklistedrole'])) > 3:
                                                     rolepoints = -1
                                                 if len(str(config[str(server.id)]['rverifyplus-alerts'])) > 3:
                                                     try:
                                                         getchannel = client.get_channel(int(config[str(server.id)]['rverifyplus-alerts']))
                                                         await getchannel.send("**Alert**: The account '{}' is wearing noob clothing. Discord: <@{}>\n<@{}>'s profile: https://www.roblox.com/users/{}/profile".format(db[str(authorid)]['rblxusername'], str(authorid),str(authorid),db[str(authorid)]['userid']))
                                                     except discord.errors.Forbidden:
                                                         pass
                                                     except discord.errors.InvalidArgument:
                                                         print("DEBUG: The channel {}, doesn't exist on {}".format(config[str(server.id)]['rverifyplus-alerts'],server.name))

                                         except TypeError:
                                             print(server.id)
                        #if len(str(config[str(server.id)]['rverifyplus-alerts'])) > 3:
                            #try:
                                #getchannel = client.get_channel(int(config[str(server.id)]['rverifyplus-alerts']))
                                #await getchannel.send("**Alert**: The account '{}' is wearing noob clothing. Discord: <@{}>\n<@{}>'s profile: https://www.roblox.com/users/{}/profile".format(db[str(authorid)]['rblxusername'], str(authorid),str(authorid),db[str(authorid)]['userid']))
                            #except discord.errors.Forbidden:
                                #pass
                            #except discord.errors.InvalidArgument:
                                #print("DEBUG: The channel {}, doesn't exist on {}".format(config[str(server.id)]['rverifyplus-alerts'],server.name))
                if rolepoints == 1:
                    if not altverify:
                        roletogive = discord.utils.get(server.roles, id=config[str(server.id)]['verifiedrole'])
                        try:
                            if len(str(config[str(server.id)]['altrole'])) > 3 and db[str(authorid)]['alts']['count'] > 0:
                                altroletogive = discord.utils.get(server.roles, id=config[str(server.id)]['altrole'])
                        except KeyError:
                            pass
                        try:
                            await memberid.add_roles(roletogive, reason="User was Verified")
                            try:
                                if len(str(config[str(server.id)]['altrole'])) > 3 and db[str(authorid)]['alts']['count'] > 0:
                                    await memberid.add_roles(altroletogive, reason="User has a verified alt")
                            except KeyError:
                                pass
                        except discord.errors.Forbidden:
                            if len(str(config[str(server.id)]['rverifyplus-alerts'])) > 3:
                                try:
                                    getchannel = client.get_channel(config[str(server.id)]['rverifyplus-alerts'])
                                    user = client.get_user(str(authorid))
                                    await getchannel.send("**Alert**: The bot is lacking permissions to give roles, please fix my permissions.")
                                    await user.send('Error: I am lacking permissions to give you the proper role, please contact an Admin to fix me.')
                                except discord.errors.Forbidden:
                                    user = client.get_user(str(authorid))
                                    await user.send('Error: I am lacking permissions to give you the proper role, please contact an Admin to fix me.')
                                except discord.errors.InvalidArgument:
                                    print("DEBUG: The channel {}, doesn't exist on {}".format(config[str(server.id)]['rverifyplus-alerts'],server.name))
                    else:
                        if len(str(config[str(server.id)]['altrole'])) > 3:
                            altroletogive = discord.utils.get(server.roles, id=config[str(server.id)]['altrole'])
                            await memberid.add_roles(altroletogive, reason="User has a verified alt")
                else:
                    if not altverify:
                        roletogive = discord.utils.get(server.roles, id=config[str(server.id)]['blacklistedrole'])
                        try:
                            await memberid.add_roles(roletogive, reason="User was Blacklisted upon Verification")
                        except discord.errors.Forbidden:
                            if len(str(config[str(server.id)]['rverifyplus-alerts'])) > 3:
                                try:
                                    getchannel = client.get_channel(config[str(server.id)]['rverifyplus-alerts'])
                                    user = client.get_user(str(authorid))
                                    await getchannel.send("**Alert**: The bot is lacking permissions to give roles, please fix my permissions.")
                                    await user.send('Error: I am lacking permissions to give you the proper role, please contact an Admin to fix me.')
                                except discord.errors.Forbidden:
                                    user = client.get_user(str(authorid))
                                    await user.send('Error: I am lacking permissions to give you the proper role, please contact an Admin to fix me.')
                                except discord.errors.InvalidArgument:
                                    print("DEBUG: The channel {}, doesn't exist on {}".format(config[str(server.id)]['rverifyplus-alerts'],server.name))

                if config[str(server.id)]['autogameaccess']:
                    if not altverify: # I don't exactly remember how the api server handles this situation.
                        if int(config[str(server.id)]['verifiedrole']) in [role.id for role in authorroles]:
                            with open("gameaccess/{}.json".format(str(server.id))) as m:
                                gameaccessdb = json.load(m)
                                gameaccessdb[str(db[str(authorid)]['userid'])] = True
                                with open("gameaccess/{}.json".format(str(server.id)), 'w') as m:
                                    json.dump(gameaccessdb, m, indent=2)

                async with aiohttp.ClientSession(loop=loop) as session:
                    async with session.get('https://api.roblox.com/users/{}/groups'.format(db[str(authorid)]['userid']), headers=headers) as r:
                        if r.status == 200:
                            html = await r.read()
                            if '3514227'.encode('utf-8') in html or '1200769'.encode('utf-8') in html or '2868472'.encode('utf-8') in html:
                                print(authorid)
                                print(True)
                                if str(server.id) == "419847758170816513":
                                    getchannel = client.get_channel(config[str(server.id)]['rverifyplus-alerts'])
                                    await getchannel.send("**DEBUG Alert**: @everyone The account '{}' is in a suspicious group. Discord: <@{}>\n<@{}>'s profile: https://www.roblox.com/users/{}/profile".format(db[str(authorid)]['rblxusername'], authorid,authorid,db[str(authorid)]['userid']))
                                    await session.close()

            elif r.status == 404:
                try:
                    user = client.get_user(int(authorid)) # The int might be redundant but I forgot how my code works lol
                    await user.send('Your ROBLOX profile ({}) isn\'t available (Did you get account termination?), and for security reasons, you have been automatically unverified.\nRun {}verify again with a new account to be verified.'.format(db[str(authorid)]['rblxusername'], config[str(str(server.id))]['prefix']))
                    del db[str(authorid)]
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
                except discord.errors.Forbidden:
                    await message.channel('<@{}> Something went wrong with completing the verification process, and I was unable to DM you why. Please change your privacy settings to allow direct DMs, and/or unblock the bot, then run {}verify again to see the message.'.format(str(authorid),config[guild.id]['prefix']))

            else:
                await author.send('<@{}> Uh-oh, I was unable to finish verifying you because I have received this HTTP error code: {}'.format(r.status))

async def verify2(message, client):
 parsedmessage = message.content.replace('{}verify'.format(config[str(message.guild.id)]['prefix']), '')
 parsedmessage2 = parsedmessage.replace(' {}verify'.format(config[str(message.guild.id)]['prefix']), '')
 if "{}verify".format(config[str(message.guild.id)]['prefix']) in message.content and len(parsedmessage) > 4 and "{}verify".format(config[str(message.guild.id)]['prefix']) not in parsedmessage2:
     db[str(message.author.id)] = {}
     db[str(message.author.id)]["rblxusername"] = parsedmessage2.split()[0]
     try:
         await message.delete()
     except discord.NotFound:
         pass
     except discord.errors.Forbidden:
         pass
     db[str(message.author.id)]["verifycode"] = verifycode_generator()
     with open('db.json', 'w') as f:
         json.dump(db, f, indent=2)
     async with aiohttp.ClientSession(loop=loop) as session:
         async with session.get(get_roblox_id.format(parsedmessage.split()[0]), headers=headers) as r:
             if r.status == 200:
                 js = await r.json()
                 await session.close()
                 try:
                     if any(x for x in db.values() if x['userid'] == int(js['Id'])):
                         discordid = str(find_key2(db, int(js['Id']))[0])
                         db[discordid]['markfordeletion'] = True
                         db[str(message.author.id)]['olddiscord'] = discordid
                         await message.channel.send('<@{}> Warning: This username is currently registered to another user.\nCompleting the verification test will result your old information being deleted.'.format(message.author.id))
                         #await client.send_message(client.get_channel(config[str(message.guild.id)]['rverifyplus-alerts']), '**Notice** <@{}> attempted to use an already verified roblox username "https://roblox.com/users/{}/profile"'.format(message.author.id, json['Id']))
                         with open('db.json', 'w') as f:
                             json.dump(db, f, indent=2)
                 except KeyError:
                     pass
                 try:
                     try:
                         newid = bcrypt.hashpw(str(message.author.id).encode('utf-8'), bcrypt.gensalt( 12 ))
                     except:
                         newid = None
                     db[str(message.author.id)]["userid"] = js['Id']
                     db[str(message.author.id)]["hidewhois"] = False
                     db[str(message.author.id)]['alts'] = {}
                     db[str(message.author.id)]['alts']['count'] = 0
                     if newid != None:
                         db[str(message.author.id)]['uid'] = str(newid.decode('utf-8'))
                         with open('db.json', 'w') as f:
                             json.dump(db, f, indent=2)
                             await message.channel.send('<@{}> Please check your DMs for further instructions.'.format(message.author.id))
                             try:
                                 await message.author.send('Please enter the following set of codes into your ROBLOX account\'s status or description to prove your authenticity: ```{}```\nAfter adding the verification code, type {}done in the channel.\nThe username you entered was ``{}``; Incase of an error or typo, enter {}cancel in channel and try again.'.format(db[str(message.author.id)]["verifycode"],config[str(message.guild.id)]['prefix'],db[str(message.author.id)]['rblxusername'],config[str(message.guild.id)]['prefix']))
                             except discord.errors.Forbidden:
                                 await message.channel.send('<@{}> I was unable to DM you, please fix your privacy settings or unblock the bot to continue. Verification has been canceled.'.format(message.author.id))
                     else:
                         await message.channel.send('<@{}> ERROR: I wasn\'t able to generate you a unique ID because of a discord fluke, please try running !verify again.'.format(message.author.id))
                         del db[str(message.author.id)]
                         with open('db.json', 'w') as f:
                             json.dump(db, f, indent=2)
                 except KeyError:
                     await message.channel.send('<@{}> Error: Invalid username, verification has been canceled.'.format(message.author.id))
                     del db[str(message.author.id)]
                     with open('db.json', 'w') as f:
                         json.dump(db, f, indent=2)
             elif r.status == 400:
                 await message.channel.send('<@{}> Error: That username doesn\'t exist on ROBLOX, verification has been canceled.'.format(message.author.id))
                 del db[str(message.author.id)]
                 with open('db.json', 'w') as f:
                     json.dump(db, f, indent=2)
             else:
                 await message.channel.send('<@{}> Uh-oh, I got an HTTP error code {} with Roblox\'s Web API!'.format(message.author.id, r.status))
                 del db[str(message.author.id)]
                 with open('db.json', 'w') as f:
                     json.dump(db, f, indent=2)
 else:
     #try:
         #await client.delete_message(message)
     #except discord.errors.Forbidden:
         #pass
     def check(user):
         return user.author.id == message.author.id
     tempmsg = await message.channel.send('<@{}> Please provide a valid ROBLOX username either with {}verify, or as the next message in the next 30 seconds. Type "cancel" to cancel verification.'.format(message.author.id, config[str(message.guild.id)]['prefix']))
     try:
          msg = await client.wait_for('message', check=check, timeout=30)
          if msg == None:
              if message.author.id not in db:
                  await tempmsg.delete()
                  await message.channel.send('<@{}> Verification command has timed out.'.format(message.author.id))
          else:
              if "cancel" in msg.content or "{}verify".format(config[str(message.guild.id)]['prefix']) in msg.content:
                  await message.channel.send('<@{}> Verification has been canceled.'.format(message.author.id))
              elif "{}verify".format(config[str(message.guild.id)]['prefix']) in msg.content:
                  pass
              else:
                  parsedmessage = msg.content.replace('{}verify'.format(config[str(message.guild.id)]['prefix']), '')
                  parsedmessage2 = parsedmessage.replace(' {}verify'.format(config[str(message.guild.id)]['prefix']), '')
                  db[str(message.author.id)] = {}
                  db[str(message.author.id)]["rblxusername"] = parsedmessage.split()[0]
                  try:
                      await msg.delete()
                  except discord.NotFound:
                      pass
                  except discord.errors.Forbidden:
                      pass
                  db[str(message.author.id)]["verifycode"] = verifycode_generator()
                  async with aiohttp.ClientSession(loop=loop) as session:
                      async with session.get(get_roblox_id.format(parsedmessage.split()[0]), headers=headers) as r:
                          if r.status == 200:
                              js = await r.json()
                              try:
                                  if any(x for x in db.values() if x['userid'] == int(js['Id'])):
                                      discordid = str(find_key2(db, int(js['Id']))[0])
                                      db[discordid]['markfordeletion'] = True
                                      db[str(message.author.id)]['olddiscord'] = discordid
                                      await message.channel.send('<@{}> Warning: This username is currently registered to another user.\nCompleting the verification test will result your old information being deleted.'.format(message.author.id))
                                      with open('db.json', 'w') as f:
                                          json.dump(db, f, indent=2)
                              except KeyError:
                                  pass
                              try:
                                  try:
                                      newid = bcrypt.hashpw(str(message.author.id).encode('utf-8'), bcrypt.gensalt( 12 ))
                                  except:
                                      newid = None
                                  db[str(message.author.id)]["userid"] = js['Id']
                                  db[str(message.author.id)]["hidewhois"] = False
                                  db[str(message.author.id)]['alts'] = {}
                                  db[str(message.author.id)]['alts']['count'] = 0
                                  if newid != None:
                                      db[str(message.author.id)]['uid'] = str(newid.decode('utf-8'))
                                      with open('db.json', 'w') as f:
                                         json.dump(db, f, indent=2)
                                      await tempmsg.delete()
                                      await message.channel.send('<@{}> Please check your DMs for further instructions.'.format(message.author.id))
                                      try:
                                          await message.author.send('Please enter the following set of codes into your ROBLOX account\'s status or description to prove your authenticity: ```{}```\nAfter adding the verification code, type {}done in the channel.\nThe username you entered was ``{}``; Incase of an error or typo, enter {}cancel in channel and try again.'.format(db[str(message.author.id)]["verifycode"],config[str(message.guild.id)]['prefix'],db[str(message.author.id)]['rblxusername'],config[str(message.guild.id)]['prefix']))
                                      except discord.errors.Forbidden:
                                          await message.channel.send('<@{}> I was unable to DM you, please fix your privacy settings or unblock the bot to continue. Verification has been canceled.'.format(message.author.id))
                                  else:
                                      await message.channel.send('<@{}> ERROR: I wasn\'t able to generate you a unique ID because of a discord fluke, please try running !verify again.'.format(message.author.id))
                                      del db[str(message.author.id)]
                                      with open('db.json', 'w') as f:
                                          json.dump(db, f, indent=2)
                              except KeyError:
                                  await message.channel.send('<@{}> Error: Invalid username, verification has been canceled.'.format(message.author.id))
                                  del db[str(message.author.id)]
                                  with open('db.json', 'w') as f:
                                      json.dump(db, f, indent=2)
                          else:
                              await message.channel.send('<@{}> Uh-oh, I got an HTTP error code {}'.format(message.author.id, r.status))
     except asyncio.TimeoutError:
         if message.author.id not in db:
             await tempmsg.delete()
             await message.channel.send('<@{}> Verification command has timed out.'.format(message.author.id))

async def userupdate_after_verify(message):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(get_roblox_id.format(db[str(message.author.id)]['rblxusername']), headers=headers) as r:
            if r.status == 200:
                js = await r.json()
                await session.close()
                if js['Username'] == db[str(message.author.id)]['rblxusername']:
                    return
                else:
                    try:
                        editwhencomplete = await message.author.send('<@{}> Updating your records with your latest username...'.format(message.author.id))
                    except discord.errors.Forbidden:
                        editwhencomplete = None
                    db[str(message.author.id)]['rblxusername'] = js['Username']
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
                    if editwhencomplete != None:
                        await editwhencomplete.edit(content="Updating your records with your latest username... done")
                    return

async def changenick(client, author, authorid, server, authorroles):
     try:
         user = client.get_user(authorid)
         user_nickchange = server.get_member(authorid)
         await user.send('Note: The server "{}" has requested for your server username to be automatically changed as your ROBLOX username.\nIf you have the valid permissions, you can change this back once you\'re in.'.format(server.name))
         await user_nickchange.edit(nick=db[str(authorid)]['rblxusername'], reason="Nickname to Roblox username is enabled.")
     except discord.errors.Forbidden:
         pass
     altverify = False
     altaccount = None
     await checkage(authorid, server, client, authorroles, author, altverify, altaccount)

async def migrate_from_rover(message, client):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get('https://verify.eryn.io/api/user/{}'.format(message.author.id), headers=headers) as response:
            if response.status == 200:
                js = await response.json()
                if str(message.author.id) in nomigration:
                    if nomigration[str(message.author.id)] == js['robloxId']:
                        await verify2(message, client)
                    else:
                        del nomigration[str(message.author.id)]
                        with open('nomigration.json', 'w') as n:
                            json.dump(nomigration, n, indent=2)
                        await migrate_from_rover(message, client)
                if str(message.author.id) not in nomigration:
                    def check(user):
                        return user.author.id == message.author.id
                    try:
                        tempmsg = await message.channel.send('<@{}> It appears you have a verified account in RoVer, do you wish to migrate/copy your verification information from there? (Yes/No or y/n)\nQuestion will timeout in 30 seconds, otherwise enter "cancel" to cancel.'.format(message.author.id))
                        msg = await client.wait_for('message', check=check, timeout=30)
                        if msg == None:
                            await tempmsg.delete()
                            await message.channel.send('<@{}> Migration command has timed out.'.format(message.author.id))
                        else:
                            if "cancel" in msg.content.split(' ', 1)[0]:
                                await tempmsg.delete()
                                await message.channel.send('<@{}> Migration from RoVer has been canceled.'.format(message.author.id))
                            elif "yes" in msg.content.lower().split(' ', 1)[0] or "y" in msg.content.lower().split(' ', 1)[0]:
                                await message.channel.send('<@{}> Migrating from RoVer...\nCheck your DMs for the rest of the migration process setup.'.format(message.author.id))
                                try:
                                    await message.author.send('***Migration from RoVer Setup***')
                                    await session.close()
                                    await message.author.send('**RoVer**: <@{}> is verified as {}.\nIs this the account you wish to use? (Yes/No) or (y/n)\nQuestion will timeout in 120 seconds, otherwise enter "cancel" to cancel.'.format(message.author.id, js['robloxUsername']))
                                    msg = await client.wait_for('message', check=check, timeout=120)
                                    if msg == None:
                                        await message.channel.send('<@{}> Migration command has timed out, and therefore was canceled.'.format(message.author.id))
                                    else:
                                        if "cancel" in msg.content.split(' ', 1)[0]:
                                            await tempmsg.delete()
                                            await message.author.send('Migration from RoVer has been canceled.')
                                        elif "yes" in msg.content.lower().split(' ', 1)[0] or "y" in msg.content.lower().split(' ', 1)[0]:
                                            editwhencomplete = await message.author.send('***Migrating...***')
                                            try:
                                                newid = bcrypt.hashpw(str(message.author.id).encode('utf-8'), bcrypt.gensalt( 12 ))
                                            except:
                                                newid = None
                                            db[str(message.author.id)] = {}
                                            db[str(message.author.id)]['userid'] = js['robloxId']
                                            db[str(message.author.id)]['verifycode'] = ''
                                            db[str(message.author.id)]['rblxusername'] = js['robloxUsername']
                                            db[str(message.author.id)]['hidewhois'] = False
                                            if newid != None:
                                                db[str(message.author.id)]['uid'] = str(newid.decode('utf-8'))
                                                with open('db.json', 'w') as f:
                                                    json.dump(db, f, indent=2)
                                                await editwhencomplete.edit(content="***Migrating...*** done")
                                                await message.author.send('Welcome, {}'.format(db[str(message.author.id)]['rblxusername']))
                                                authorid = message.author.id
                                                server = message.guild
                                                authorroles = message.author.roles
                                                author = message.author
                                                altverify = False
                                                altaccount = None
                                                await checkage(authorid, server, client, authorroles, author, altverify, altaccount)
                                            else:
                                                await message.author.send('ERROR: I wasn\'t able to generate you a unique ID because of a discord fluke, please try running !verify again.')
                                                del db[str(message.author.id)]
                                                with open('db.json', 'w') as f:
                                                    json.dump(db, f, indent=2)
                                        elif "no" in msg.content.lower().split(' ', 1)[0] or "n" in msg.content.lower().split(' ', 1)[0]:
                                            await message.author.send('Migration from RoVer has been canceled, use {}verify (in channel) for the account you wish to use instead.'.format(config[str(message.guild.id)]['prefix']))
                                            nomigration[str(message.author.id)] = js['robloxId']
                                            with open('nomigration.json', 'w') as n:
                                                json.dump(nomigration, n, indent=2)
                                except discord.errors.Forbidden:
                                    await message.channel.send('<@{}> I was unable to DM you, please fix your privacy settings or unblock the bot to continue. Verification has been canceled.'.format(message.author.id))

                            elif "no" in msg.content.lower().split(' ', 1)[0] or "n" in msg.content.lower().split(' ', 1)[0]:
                                await message.channel.send('<@{}> Alrighty then. I\'m starting the normal verification process, then.'.format(message.author.id))
                                js = await response.json()
                                nomigration[str(message.author.id)] = js['robloxId']
                                with open('nomigration.json', 'w') as n:
                                   json.dump(nomigration, n, indent=2)
                                await verify2(message, client)

                    except asyncio.TimeoutError:
                        await tempmsg.delete()
                        await message.channel.send('<@{}> Migration command has timed out.'.format(message.author.id))

            elif response.status == 404:
                await verify2(message, client)
            else:
                await message.channel.send('<@{}> Uh-oh, I got an HTTP error code {}'.format(message.author.id, response.status))

@client.event
async def on_ready():
    dblurl = "https://discordbots.org/api/bots/" + str(client.user.id) + "/stats"
    dblheaders = {"Authorization" : config['dbltoken']}
    print('---------------------------------')
    print('Logged in as {}'.format(client.user.name))
    print('Bot discord ID: {}'.format(client.user.id))
    print('---------------------------------')
    print('*More bot stats*')
    print('I am running discord version {}'.format(discord.__version__))
    print('My python version is {}'.format(platform.python_version()))
    print('---------------------------------')
    if not os.path.exists('gameaccess'):
        os.makedirs('gameaccess')
    if not os.path.exists('serverdBs'):
        os.makedirs('serverdBs')
    if not os.path.exists('memberlist'):
        os.makedirs('memberlist')
    n = 0
    m = 0
    o = 0
    print("Running bot configuration check")
    for x in client.guilds:
        if str(x.id) not in config:
            config[str(x.id)] = {
            'verifychannel': 0,
            'verifiedrole': 0,
            'blacklistedrole': 0,
            'verified-logs': 0,
            'rverifyplus-alerts': 0,
            'game-logs': 0,
            'autoverify': False,
            'changenickonverify': False,
            'gameaccess': False,
            'autogameaccess': False,
            'serverapikey': "",
            'unverifiedrole': 0,
            'prefix': str(config['defaultprefix']),
            'minage': "60",
            'welcomemessage': "",
            'permitalts': True
            }
            n = n + 1
        if not os.path.exists('serverdBs' + '/{}.db.json'.format(str(x.id))):
            with open('serverdBs' + '/{}.db.json'.format(str(x.id)), 'wt') as inFile: inFile.write('{\n}')
            o = o + 1
        if not os.path.exists('gameaccess' + '/{}.json'.format(str(x.id))):
            with open('gameaccess' + '/{}.json'.format(str(x.id)), 'wt') as inFile: inFile.write('{\n}')
            o = o + 1
        else:
            if 'verifychannel' not in config[str(x.id)]:
                config[str(x.id)]['verifychannel'] = ""
                m = m + 1
            if 'verifiedrole' not in config[str(x.id)]:
                config[str(x.id)]['verifiedrole'] = ""
                m = m + 1
            if 'blacklistedrole' not in config[str(x.id)]:
                config[str(x.id)]['blacklistedrole'] = ""
                m = m + 1
            if "minage" not in config[str(x.id)]:
                config[str(x.id)]['minage'] = "60"
                m = m + 1
            if 'welcomemessage' not in config[str(x.id)]:
                config[str(x.id)]['welcomemessage'] = ""
                m = m + 1
            if 'permitalts' not in config[str(x.id)]:
                config[str(x.id)]['permitalts'] = True
                m = m + 1
            if 'unverifiedrole' not in config[str(x.id)]:
                config[str(x.id)]['unverifiedrole'] = ""
                m = m + 1
            if 'groups' not in config[str(x.id)]:
                config[str(x.id)]['groups'] = {
                'Enabled': False,
                'groupid': ""
                }
            if 'sharedapikey' not in config[str(x.id)]:
                config[str(x.id)]['sharedapikey'] = {
                'Enabled': False,
                'key': ""
                }
                m = m + 1
            if 'noobdetection' not in config[str(x.id)]:
                config[str(x.id)]['noobdetection'] = {
                'Enabled': False,
                'level': 2
                }
                m = m + 1
            if 'altrole' not in config[str(x.id)]:
                config[str(x.id)]['altrole'] = ""
                m = m + 1
            try:
                if config[str(x.id)]['noobdetection'] == False:
                    config[str(x.id)]['noobdetection'] = {
                    'Enabled': False,
                    'level': 3
                    }
                    m = m + 1
            except:
                pass
            try:
                if config[str(x.id)]['noobdetection'] == True:
                    config[str(x.id)]['noobdetection'] = {
                    'Enabled': True,
                    'level': 3
                    }
            except:
                pass
    with open('config.json', 'w') as g:
        json.dump(config, g, indent=2)
    if n == 1:
        print("1 server didn\'t have a config, fixing.")
    if n > 1:
        print("{} servers didn\'t have a config, fixing.".format(n))
    else:
        print("Server config check part 1 completed.")
    if m == 1:
        print("1 server was missing a new config setting, fixing.")
    if m > 1:
        print("{} servers was missing a new config setting, fixing.".format(m))
    else:
        print("Server config check part 2 completed.")
    if o == 1:
        print("1 server was missing a gameaccess/serverdb file, fixing.")
    if o > 1:
        print("{} servers was missing a gameaccess/serverdb file, fixing.".format(o))
    else:
        print("Server config check part 3 completed, all servers have their config.")
    while True:
        n = 0
        for x in db:
            if db[x]['verifycode'] != "":
                n = n + 1
        verifiedn = len(db)-n
        statustouse = "{} servers, {} users.".format(len(client.guilds), len(db)-n)
        payload = {"server_count"  : len(client.guilds)}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(dblurl, data=payload, headers=dblheaders) as r:
                    if r.status == 200:
                        await session.close()
        except aiohttp.errors.ClientOSError as er:
            print("Error: Internet connectivity error has occured, and I wasn't able to connect to discordbots.org, skipping.\nError Message: {}".format(er))
        status = list(client.guilds)[0].me.status
        game = discord.Activity(name=statustouse)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=statustouse))
        if len([x for x in db.values() if 'userid' not in x]) != 0:
            brokenid = [x['rblxusername'] for x in db.values() if 'userid' not in x]
            discordid = str(find_key2(db, re.sub(r'[^\w]', '', str(brokenid)).replace(' ', ''))[0])
            del db[discordid]
            with open('db.json', 'w') as f:
                json.dump(db, f, indent=2)
        await asyncio.sleep(60)

@client.event
async def on_guild_join(guild):
    if not os.path.exists('serverdBs' + '/{}.db.json'.format(str(guild.id))):
        with open('serverdBs' + '/{}.db.json'.format(str(guild.id)), 'wt') as inFile: inFile.write('{\n}')
    if not os.path.exists('gameaccess' + '/{}.json'.format(str(guild.id))):
        with open('gameaccess' + '/{}.json'.format(str(guild.id)), 'wt') as inFile: inFile.write('{\n}')
    if str(guild.id) not in config:
        config[str(guild.id)] = {
        'verifychannel': 0,
        'verifiedrole': 0,
        'altrole': 0,
        'blacklistedrole': 0,
        'verified-logs': 0,
        'rverifyplus-alerts': 0,
        'game-logs': 0,
        'autoverify': False,
        'changenickonverify': False,
        'gameaccess': False,
        'noobdetection': {
        'Enabled': False,
        'level': 3
        },
        'autogameaccess': False,
        'serverapikey': "",
        'unverifiedrole': 0,
        'groups': {
        'Enabled': False,
        'groupid': ""
        },
        'prefix': str(config['defaultprefix']),
        'minage': "60",
        'sharedapikey': {
        'Enabled': False,
        'key': ""
        },
        'welcomemessage': "",
        'permitalts': True
        }
        with open('config.json', 'w') as g:
            json.dump(config, g, indent=2)
        getchannel = client.get_channel(config[config['officialserver']]['rverifyplus-ctrlalerts'])
        await getchannel.send('I joined the server "{}" (Server ID: {}), with a population of {}, owned by {}'.format(guild.name, guild.id, guild.member_count, guild.owner))
@client.event
async def on_guild_remove(guild):
    if os.path.exists('serverdBs' + '/{}.db.json'.format(str(guild.id))):
        os.remove('serverdBs/' + '{}.db.json'.format(str(guild.id)))
    if str(guild.id) in config:
        del config[str(guild.id)]
        with open('config.json', 'w') as g:
            json.dump(config, g, indent=2)
    if os.path.exists('gameaccess' + '/{}.json'.format(str(guild.id))):
        os.remove('gameaccess/' + '{}.json'.format(str(guild.id)))
    #if str(guild.id) in activitylog:
        #del activitylog[str(guild.id)]
        #with open('activitylog.json', 'w') as t:
            #json.dump(activitylog, t, indent=2)
    getchannel = client.get_channel(config[config['officialserver']]['rverifyplus-ctrlalerts'])
    await getchannel.send('I left the server "{}"'.format(guild.name))

@client.event
async def on_guild_role_delete(role):
    if config[str(role.guild.id)]['verifiedrole'] == str(role.id):
        config[str(role.guild.id)]['verifiedrole'] = 0
    elif config[str(role.guild.id)]['blacklistedrole'] == str(role.id):
        config[str(role.guild.id)]['blacklistedrole'] = 0
    with open('config.json', 'w') as g:
        json.dump(config, g, indent=2)

@client.event
async def on_channel_delete(channel):
    if config[str(channel.guild.id)]['verifychannel'] == str(channel.id):
        config[str(channel.guild.id)]['verifychannel'] = 0
    elif config[str(channel.guild.id)]['rverifyplus-alerts'] == str(channel.id):
        config[str(channel.guild.id)]['rverifyplus-alerts'] = 0
    elif config[str(channel.guild.id)]['verified-logs'] == str(channel.id):
        config[str(channel.guild.id)]['verified-logs'] = 0
    with open('config.json', 'w') as g:
        json.dump(config, g, indent=2)

@client.event
async def on_member_update(before, after):
    try:
        if config[str(before.guild.id)]['gameaccess']:
            if config[str(before.guild.id)]['verifiedrole'] in [role.id for role in before.roles] and config[str(before.guild.id)]['verifiedrole'] not in [role.id for role in after.roles]:
                with open("gameaccess/{}.json".format(str(before.guild.id))) as m:
                    gameaccessdb = json.load(m)
                    if str(db[str(before.id)]['userid']) in gameaccessdb:
                        idnumber = str(db[str(before.id)]['userid'])
                        del gameaccessdb[idnumber]
                    with open("gameaccess/{}.json".format(str(before.guild.id)), 'w') as m:
                        json.dump(gameaccessdb, m, indent=2)
    except KeyError:
        if str(before.guild.id) not in config:
            config[str(before.guild.id)] = {
            'verifychannel': '',
            'verifiedrole': '',
            'blacklistedrole': '',
            'verified-logs': '',
            'rverifyplus-alerts': '',
            'game-logs': '',
            'autoverify': False,
            'changenickonverify': False,
            'gameaccess': False,
            'noobdetection': False,
            'autogameaccess': False,
            'serverapikey': "",
            'unverifiedrole': "",
            'prefix': str(config['defaultprefix']),
            'minage': "60",
            'welcomemessage': "",
            'permitalts': True
            }
            with open('config.json', 'w') as g:
                json.dump(config, g, indent=2)
            print("DEBUG ERROR: Repairing {}\'s config.".format(before.server.name))

@client.event
async def on_member_remove(member):
    if str(member.id) in db:
        if config[str(member.guild.id)]['gameaccess']:
            with open("gameaccess/{}.json".format(str(member.guild.id))) as m:
                gameaccessdb = json.load(m)
                if str(db[str(member.id)]['userid']) in gameaccessdb:
                    del gameaccessdb[str(db[str(member.id)]['userid'])]
                with open("gameaccess/{}.json".format(str(member.guild.id)), 'w') as m:
                    json.dump(gameaccessdb, m, indent=2)
        #if str(member.id) in activitylog[str(member.guild.id)]:
            #del activitylog[str(member.guild.id)][str(member.id)]
            #with open('activitylog.json', 'w') as t:
                #json.dump(activitylog, t, indent=2)

@client.event
async def on_member_ban(guild, user):
    if str(user.id) in db:
        if config[str(guild.id)]['gameaccess']:
            with open("gameaccess/{}.json".format(str(guild.id))) as m:
                gameaccessdb = json.load(m)
                if str(db[str(user.id)]['userid']) in gameaccessdb:
                    del gameaccessdb[str(db[str(user.id)]['userid'])]
                    with open("gameaccess/{}.json".format(str(guild.id)), 'w') as m:
                        json.dump(gameaccessdb, m, indent=2)
        with open("serverdBs/{}.db.json".format(str(guild.id))) as u:
            serverdB = json.load(u)
            if 'bans' not in serverdB:
                serverdB['bans'] = {}

            serverdB['bans'][str(user.id)] = str(db[str(user.id)]['userid'])
            with open('serverdBs/{}.db.json'.format(str(guild.id)), 'w') as u:
                json.dump(serverdB, u, indent=2)

@client.event
async def on_member_unban(guild, user):
    if str(user.id) in db:
        with open("serverdBs/{}.db.json".format(str(guild.id))) as u:
            serverdB = json.load(u)
            if 'bans' in serverdB:
                if str(user.id) in serverdB['bans']:
                    del serverdB['bans'][str(user.id)]
                    with open("serverdBs/{}.db.json".format(str(guild.id)), 'w') as u:
                        json.dump(serverdB, u, indent=2)

@client.event
async def on_member_join(member):
    if "welcomemessage" in config[str(member.guild.id)]:
        if config[str(member.guild.id)]['welcomemessage'] != "":
            if config[str(member.guild.id)]['autoverify']:
                if str(member.id) in db:
                    if db[str(member.id)]['verifycode'] == "":
                        pass
                else:
                    try:
                        await member.send('**CUSTOM WELCOME MESSAGE**: {}'.format(config[str(member.guild.id)]['welcomemessage']))
                    except discord.errors.Forbidden:
                        pass
            else:
                try:
                    await member.send('**CUSTOM WELCOME MESSAGE**: {}'.format(config[str(member.guild.id)]['welcomemessage']))
                except discord.errors.Forbidden:
                    pass
    if "unverifiedrole" in config[str(member.guild.id)]:
        if config[str(member.guild.id)]['unverifiedrole'] != "":
            roletogive = discord.utils.get(member.guild.roles, id=config[str(member.guild.id)]['unverifiedrole'])
            try:
                if discord.utils.get(member.guild.roles, id=config[str(member.guild.id)]['unverifiedrole']) == None: # The bot will make sure the role still exists before attempting to give, this will reduce errors.
                    config[str(member.guild.id)]['unverifiedrole'] = 0
                    with open('config.json', 'w') as g:
                        json.dump(config, g, indent=2)
                else:
                    await member.add_roles(roletogive, reason="New user joined the server, giving UnVerifiedRole.")
            except discord.errors.Forbidden:
                if len(config[str(member.guild.id)]['rverifyplus-alerts']) > 3:
                    try:
                        getchannel = client.get_channel(config[str(member.guild.id)]['rverifyplus-alerts'])
                        await getchannel.send("**Alert**: The bot is lacking permissions to give roles, please fix my permissions.")
                    except discord.errors.InvalidArgument:
                        print("DEBUG: The channel {}, doesn't exist on {}".format(config[str(member.guild.id)]['rverifyplus-alerts'],server.name))

    if config[str(member.guild.id)]['autoverify']:
        if member.id in db:
            if db[str(member.id)]['verifycode'] == "":
                authorid = member.id
                server = member.guild
                authorroles = member.roles
                author = member
                altverify = False
                altaccount = None
                if config[str(member.guild.id)]['changenickonverify']:
                    await changenick(client, author, authorid, server, authorroles)
                else:
                    await checkage(authorid, server, client, authorroles, author, altverify, altaccount)
                try:
                    await client.send_message(member, 'Welcome back, {}'.format(db[str(member.id)]['rblxusername']))
                except discord.errors.Forbidden:
                    pass
    #asyncio.wait(5) -- Complete role added from other bots tracking.
@client.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.CommandNotFound, commands.UserInputError)

    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
        return

    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@client.command(pass_context=True)
async def userupdate(ctx):
    message = ctx.message
    if not message.author.bot:
        if str(message.author.id) in db:
            async with aiohttp.ClientSession(loop=loop) as session:
                async with session.get(get_roblox_id.format(db[str(message.author.id)]['rblxusername']), headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        if js['Username'] == db[str(message.author.id)]['rblxusername']:
                            await message.channel.send('<@{}> Your username is already up-to-date.'.format(message.author.id))
                        else:
                            editwhencomplete = await message.channel.send('<@{}> Updating your records with your latest username...'.format(message.author.id))
                            db[str(message.author.id)]['rblxusername'] = js['Username']
                            with open('db.json', 'w') as f:
                                json.dump(db, f, indent=2)
                            await editwhencomplete.edit(new_content="Updating your records with your latest username... done")
                            if config[str(message.guild.id)]['changenickonverify']:
                                await client.change_nickname(message.author, db[str(message.author.id)]['rblxusername'])

                    else:
                        await message.channel.send('<@{}> Uh-oh, I got an HTTP error code {}'.format(message.author.id, r.status))
        else:
            await message.channel.send('<@{}> You cannot use {}userupdate if you haven\'t verified yet.\nStart your verification process using {}verify.'.format(message.author.id,config[str(message.guild.id)]['prefix'],config[str(message.guild.id)]['prefix']))

@client.command(pass_context=True)
async def denyga(ctx):
    message = ctx.message
    if not message.author.bot:
        if str(message.author.id) in db:
            if str(message.author.id) in (str(message.guild.owner_id), str(message.author.guild_permissions.administrator), str(message.author.guild_permissions.manage_guild), config['ownerid'], str(message.author.guild_permissions.kick_members)):
                try:
                    user_to_search = message.content.split()[1]
                    removetags = re.sub('<@!', '', user_to_search)
                    removetags2 = re.sub('<@', '', removetags)
                    removetags3 = re.sub('>', '', removetags2)
                    if removetags3.isdigit():
                        if removetags3 in db and len(db[removetags3]['verifycode']) == 0:
                            with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                gameaccessdb = json.load(m)
                                if config[str(message.guild.id)]['gameaccess']:
                                    gameaccessdb[str(db[removetags3]['userid'])] = False
                                    with open("gameaccess/{}.json".format(str(message.guild.id)), 'w') as m:
                                        json.dump(gameaccessdb, m, indent=2)
                                    await message.channel.send('<@{}> GameAccess has been **disabled** for this user.'.format(message.author.id))
                                else:
                                    await message.channel.send('<@{}> GameAccess is not enabled for this server.'.format(message.author.id))
                        else:
                            await message.channel.send('<@{}> User could not be found in database.'.format(message.author.id))
                    else:
                        try:
                            discordid = find_key2(db, removetags2)[0]
                            if config[str(message.guild.id)]['gameaccess']:
                                with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                    gameaccessdb = json.load(m)
                                gameaccessdb[str(db[discordid]['userid'])] = False
                                with open("gameaccess/{}.json".format(str(message.guild.id)), 'w') as m:
                                    json.dump(gameaccessdb, m, indent=2)
                                await message.channel.send('<@{}> GameAccess has been **disabled** for this user.'.format(message.author.id))
                            else:
                                await message.channel.send('<@{}> GameAccess is not enabled for this server.'.format(message.author.id))
                        except TypeError:
                            await message.channel.send('<@{}> That roblox username couldn\'t be found. This type of usage is case sensitive when it comes to usernames.'.format(message.author.id))
                except IndexError:
                    await message.channel.send('<@{}> Syntax: {}denyga DiscordID/Roblox Username (case-sensitive)'.format(message.author.id,config[str(message.guild.id)]['prefix']))

@client.command(pass_context=True)
async def allowga(ctx):
    message = ctx.message
    if not message.author.bot:
        if str(message.author.id) in db:
            if message.author.id == message.guild.owner_id or message.author.guild_permissions.administrator or message.author.guild_permissions.manage_guild or message.author.id == config['ownerid'] or message.author.guild_permissions.kick_members:
                try:
                    user_to_search = message.content.split()[1]
                    removetags = re.sub('<@!', '', user_to_search)
                    removetags2 = re.sub('<@', '', removetags)
                    removetags3 = re.sub('>', '', removetags2)
                    if removetags3.isdigit():
                        if removetags3 in db and len(db[removetags3]['verifycode']) == 0:
                            with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                gameaccessdb = json.load(m)
                                if config[str(message.guild.id)]['gameaccess']:
                                    if str(db[removetags3]['userid']) in gameaccessdb:
                                        if not gameaccessdb[str(db[removetags3]['userid'])]:
                                            gameaccessdb[str(db[removetags3]['userid'])] = True
                                            with open("gameaccess/{}.json".format(str(message.guild.id)), 'w') as m:
                                                json.dump(gameaccessdb, m, indent=2)
                                            await message.channel.send('<@{}> GameAccess has been **re-enabled** for this user.'.format(message.author.id))
                                        else:
                                            await message.channel.send('<@{}> Error: GameAccess is not disabled for this user.'.format(message.author.id))
                                    else:
                                        await message.channel.send('<@{}> Error: This user doesn\'t have GameAccess.'.format(message.author.id))
                                else:
                                    await message.channel.send('<@{}> GameAccess is not enabled for this server.'.format(message.author.id))
                        else:
                            await message.channel.send('<@{}> User could not be found in database.'.format(message.author.id))
                    else:
                        try:
                            discordid = find_key2(db, removetags2)[0]
                            if config[str(message.guild.id)]['gameaccess']:
                                with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                    gameaccessdb = json.load(m)
                                if str(db[discordid]['userid']) in gameaccessdb:
                                    if not gameaccessdb[str(db[discordid]['userid'])]:
                                        gameaccessdb[str(db[discordid]['userid'])] = True
                                        with open("gameaccess/{}.json".format(str(message.guild.id)), 'w') as m:
                                            json.dump(gameaccessdb, m, indent=2)
                                        await message.channel.send('<@{}> GameAccess has been **re-enabled** for this user.'.format(message.author.id))
                                    else:
                                        await message.channel.send('<@{}> Error: GameAccess is not disabled for this user.'.format(message.author.id))
                                else:
                                    await message.channel.send('<@{}> Error: This user doesn\'t have GameAccess.'.format(message.author.id))
                            else:
                                await message.channel.send('<@{}> GameAccess is not enabled for this server.'.format(message.author.id))
                        except TypeError:
                            await message.channel.send('<@{}> That roblox username couldn\'t be found. This type of usage is case sensitive when it comes to usernames.'.format(message.author.id))
                except IndexError:
                    await message.channel.send('<@{}> Syntax: {}enablega DiscordID/Roblox Username (case-sensitive)'.format(message.author.id,config[str(message.guild.id)]['prefix']))


@client.command(pass_context=True)
async def cancel(ctx):
    message = ctx.message
    if not message.author.bot:
        if str(message.author.id) in db:
            try:
                if len(db[str(message.author.id)]['verifycode']) > 3:
                    await message.channel.send('<@{}> Verification has been canceled.'.format(message.author.id))
                    if "olddiscord" in db[str(message.author.id)]:
                        del db[db[str(message.author.id)]["olddiscord"]]["markfordeletion"]
                    del db[str(message.author.id)]
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
                    with open("ingameverify.json") as m:
                        ingameverifydb = json.load(m)
                        if str(message.author.id) in ingameverifydb:
                            del ingameverifydb[str(message.author.id)]
                            with open('ingameverify.json', 'w') as m:
                                json.dump(ingameverifydb, m, indent=2)
                else:
                    if str(deletecheck(message)) in db[str(message.author.id)]['alts']:
                        x = str(deletecheck(message))
                        await message.channel.send('<@{}> Alt Verification has been canceled.'.format(message.author.id))
                        if "olddiscord" in db[str(message.author.id)]['alts'][x]:
                            del db[db[str(message.author.id)]['alts']["olddiscord"]]["markfordeletion"]
                        del db[str(message.author.id)]['alts'][x]
                        db[str(message.author.id)]['alts']['count'] = db[str(message.author.id)]['alts']['count'] - 1
                        with open('db.json', 'w') as f:
                            json.dump(db, f, indent=2)
                        with open("ingameverify.json") as m:
                            ingameverifydb = json.load(m)
                            if str(message.author.id) in ingameverifydb:
                                del ingameverifydb[str(message.author.id)]
                                with open('ingameverify.json', 'w') as m:
                                    json.dump(ingameverifydb, m, indent=2)
                    elif deletecheck(message) == False or deletecheck(message) == None:
                        await message.channel.send('<@{}> You already been verified! If you need to unverify yourself, then use {}unverify instead.'.format(message.author.id,config[str(message.guild.id)]['prefix']))

            except KeyError:
                await message.channel.send('<@{}> Verification has been canceled.'.format(message.author.id))
                print("INFO: The verification entry for {} ({}) was deleted due to corruption.".format(message.author, message.author.id))
                del db[str(message.author.id)]
                with open('db.json', 'w') as f:
                    json.dump(db, f, indent=2)
                with open("ingameverify.json") as m:
                    ingameverifydb = json.load(m)
                    if str(message.author.id) in ingameverifydb:
                        del ingameverifydb[str(message.author.id)]
                        with open('ingameverify.json', 'w') as m:
                            json.dump(ingameverifydb, m, indent=2)

        else:
            await message.channel.send('<@{}> How can you cancel a verification, if you never started it? Try using {}verify to begin.'.format(message.author.id, config[str(message.guild.id)]['prefix']))


@client.command(pass_context=True)
async def unverify(ctx):
    message = ctx.message
    def check(user):
        return user.author.id == message.author.id
    if not message.author.bot:
        if message.guild == None:
            await message.author.send('Sorry, but for security purposes, you can only unverify yourself in a (appropiate) channel.')
        else:
            if str(message.author.id) in db:
                await message.channel.send('<@{}> Are you sure you want to unverify/remove yourself from the database? (This will also remove your verified role!)\nEnter "Yes" or "Y", or "No" or "N" as the next message.'.format(message.author.id))
                try:
                    msg = await client.wait_for('message', check=check, timeout=30)
                    if msg.content.lower() == 'yes' or msg.content.lower() == 'y':
                        await message.channel.send('<@{}> You have been deleted from my database, farewell. :frowning:\nRun {}verify again if you decided to switch ROBLOX accounts, or come back.'.format(message.author.id, config[str(message.guild.id)]['prefix']))
                        for x in client.guilds:
                            if x.get_member(message.author.id):
                                memberid = x.get_member(message.author.id)
                                if config[str(x.id)]['verifiedrole'] in [role.id for role in memberid.roles]:
                                    roletoremove = discord.utils.get(x.roles, id=config[str(x.id)]['verifiedrole'])
                                    await memberid.remove_roles(roletoremove, reason="User has unverified")
                                if len(str(config[str(x.id)]['blacklistedrole'])) > 3:
                                        if config[str(x.id)]['blacklistedrole'] in [role.id for role in memberid.roles]:
                                            roletoremove = discord.utils.get(x.roles, id=config[str(x.id)]['blacklistedrole'])
                                            await memberid.remove_roles(roletoremove, reason="User has unverified")
                                if len(str(config[str(x.id)]['altrole'])) > 3:
                                    roletoremove = discord.utils.get(x.roles, id=config[str(x.id)]['altrole'])
                                    await memberid.remove_roles(roletoremove, reason="User has unverified")
                                if len(str(config[str(x.id)]['unverifiedrole'])) > 3:
                                    if config[str(x.id)]['unverifiedrole'] in [role.id for role in memberid.roles]:
                                        roletoadd = discord.utils.get(x.roles, id=config[str(x.id)]['unverifiedrole'])
                                        await memberid.add_roles(roletoadd, reason="User has unverified, giving them a UnVerifiedRole.")
                                if config[str(x.id)]['gameaccess']:
                                    with open("gameaccess/{}.json".format(str(x.id))) as m:
                                        gameaccessdb = json.load(m)
                                        if str(db[str(message.author.id)]['userid']) in gameaccessdb:
                                            del gameaccessdb[str(db[str(message.author.id)]['userid'])]
                                            with open("gameaccess/{}.json".format(str(x.id)), 'w') as m:
                                                json.dump(gameaccessdb, m, indent=2)
                        del db[str(message.author.id)]
                        with open('db.json', 'w') as f:
                            json.dump(db, f, indent=2)
                    elif msg.content.lower() == "no" or msg.content.lower() == "n":
                        await message.channel.send('<@{}> Yay, you have decided to stay!'.format(message.author.id))
                    else:
                        await message.channel.send('<@{}> "{}" is not a Yes/Y or a No/N, so !unverify has been canceled.'.format(message.author.id, msg.content))
                except asyncio.TimeoutError:
                    await tempmsg.delete()
                    await message.channel.send('<@{}> Migration command has timed out.'.format(message.author.id))
            else:
                await message.channel.send('<@{}> B-But, how can you unverify...if you didn\'t verify to begin with :thinking:'.format(message.author.id))

@client.command(pass_context=True)
async def done(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.guild == None:
            await message.author.send('Sorry, but you cannot use \'done\' in a DM with me. You **must** use it in the appropiate verify channel.')
        else:
            if str(message.author.id) in db:
                if db[str(message.author.id)]['verifycode'] == "":
                    count = 0
                    for x in db[str(message.author.id)]['alts']:
                        if x == 'count':
                            pass
                        else:
                            if count == db[str(message.author.id)]['alts']['count']:
                                await message.channel.send('<@{}> You already have the verified role! To unverify, use {}unverify instead.'.format(message.author.id,config[str(message.guild.id)]['prefix']))
                            else:
                                if db[str(message.author.id)]['alts'][x]['verifycode'] == "":
                                    count = count + 1
                                else:
                                    async with aiohttp.ClientSession(loop=loop) as session:
                                        async with session.get("https://www.roblox.com/users/{}/profile".format(db[str(message.author.id)]['alts'][x]["userid"]), headers=headers) as r:
                                            if r.status == 200:
                                                html = await r.read()
                                                await session.close()
                                                if db[str(message.author.id)]['alts'][x]['verifycode'].encode('utf-8') in html:
                                                    with open("serverdBs/{}.db.json".format(str(message.guild.id))) as u:
                                                        serverdB = json.load(u)
                                                        if 'bans' in serverdB:
                                                            if find_key(serverdB, str(db[str(message.author.id)]['userid'])) is not None:
                                                                db[str(message.author.id)]['verifycode'] = ""
                                                                if "olddiscord" in db[str(message.author.id)]['alts'][x]:
                                                                    del db[db[str(message.author.id)]['alts'][x]["olddiscord"]]
                                                                    del db[str(message.author.id)]['alts'][x]["olddiscord"]
                                                                with open('db.json', 'w') as f:
                                                                    json.dump(db, f, indent=2)
                                                                try:
                                                                    await message.author.ban(reason="Ban Evasion Detected.", delete_message_days=7)
                                                                except discord.errors.Forbidden:
                                                                    if len(config[str(message.guild.id)]['rverifyplus-alerts']) > 3:
                                                                        await client.send_message(client.get_channel(config[str(message.guild.id)]['rverifyplus-alerts']), "**Alert**: I lack the ban permission to ban a user whose ban-evading in this server.\nDiscord user: <@{}>\nROBLOX Username: {}".format(mesasge.author.id,db[str(message.author.id)]['rblxusername']))
                                                                if len(config[str(message.guild.id)]['rverifyplus-alerts']) > 3:
                                                                    await client.send_message(client.get_channel(config[str(message.guild.id)]['rverifyplus-alerts']), "**Alert**: The user <@{}> was banned from the server for verifying with a previously banned ROBLOX username.\nROBLOX's Username: {}".format(message.author.id,db[str(message.author.id)]['rblxusername']))
                                                            else:
                                                                await message.author.send('Alt Verification was successful, welcome to the server!\nYou can remove the verification code from your status/description, it\'s no longer needed.')
                                                                if "olddiscord" in db[str(message.author.id)]['alts'][x]:
                                                                    del db[db[str(message.author.id)]['alts'][x]["olddiscord"]]
                                                                    del db[str(message.author.id)]['alts'][x]["olddiscord"]
                                                                db[str(message.author.id)]['alts'][x]['verifycode'] = ""
                                                                with open('db.json', 'w') as f:
                                                                    json.dump(db, f, indent=2)
                                                                authorid = message.author.id
                                                                server = message.guild
                                                                authorroles = message.author.roles
                                                                author = message.author
                                                                altverify = True
                                                                altaccount = x
                                                                await checkage(authorid, server, client, authorroles, author, altverify, altaccount)
                                                        else:
                                                            await message.author.send('Verification was successful, welcome to the server!\nYou can remove the verification code from your status/description, it\'s no longer needed.')
                                                            db[str(message.author.id)]['alts'][x]['verifycode'] = ""
                                                            with open('db.json', 'w') as f:
                                                                json.dump(db, f, indent=2)
                                                            authorid = message.author.id
                                                            server = message.guild
                                                            authorroles = message.author.roles
                                                            author = message.author
                                                            altverify = True
                                                            altaccount = x
                                                            await checkage(authorid, server, client, authorroles, author, altverify, altaccount)
                else:
                    async with aiohttp.ClientSession(loop=loop) as session:
                        async with session.get("https://www.roblox.com/users/{}/profile".format(db[str(message.author.id)]["userid"]), headers=headers) as r:
                            if r.status == 200:
                                html = await r.read()
                                await session.close()
                                if db[str(message.author.id)]['verifycode'].encode('utf-8') in html:
                                    with open("serverdBs/{}.db.json".format(str(message.guild.id))) as u:
                                        serverdB = json.load(u)
                                        if 'bans' in serverdB:
                                            if find_key(serverdB, str(db[str(message.author.id)]['userid'])) is not None:
                                                db[str(message.author.id)]['verifycode'] = ""
                                                if "olddiscord" in db[str(message.author.id)]:
                                                    del db[db[str(message.author.id)]["olddiscord"]]
                                                    del db[str(message.author.id)]["olddiscord"]
                                                with open('db.json', 'w') as f:
                                                    json.dump(db, f, indent=2)
                                                try:
                                                    await message.author.ban(reason="Ban Evasion Detected.", delete_message_days=7)
                                                except discord.errors.Forbidden:
                                                    if len(config[str(message.guild.id)]['rverifyplus-alerts']) > 3:
                                                        await client.send_message(client.get_channel(config[str(message.guild.id)]['rverifyplus-alerts']), "**Alert**: I lack the ban permission to ban a user whose ban-evading in this server.\nDiscord user: <@{}>\nROBLOX Username: {}".format(mesasge.author.id,db[str(message.author.id)]['rblxusername']))
                                                if len(config[str(message.guild.id)]['rverifyplus-alerts']) > 3:
                                                    await client.send_message(client.get_channel(config[str(message.guild.id)]['rverifyplus-alerts']), "**Alert**: The user <@{}> was banned from the server for verifying with a previously banned ROBLOX username.\nROBLOX's Username: {}".format(message.author.id,db[str(message.author.id)]['rblxusername']))
                                            else:
                                                await message.author.send('Verification was successful, welcome to the server!\nYou can remove the verification code from your status/description, it\'s no longer needed.')
                                                if "olddiscord" in db[str(message.author.id)]:
                                                    del db[db[str(message.author.id)]["olddiscord"]]
                                                    del db[str(message.author.id)]["olddiscord"]
                                                db[str(message.author.id)]['verifycode'] = ""
                                                with open('db.json', 'w') as f:
                                                    json.dump(db, f, indent=2)
                                                authorid = message.author.id
                                                server = message.guild
                                                authorroles = message.author.roles
                                                author = message.author
                                                altverify = False
                                                altaccount = None
                                                if config[str(message.guild.id)]['changenickonverify']:
                                                    await changenick(client, author, authorid, server, authorroles)
                                                else:
                                                    await checkage(authorid, server, client, authorroles, author, altverify, altaccount)
                                        else:
                                            await message.author.send('Verification was successful, welcome to the server!\nYou can remove the verification code from your status/description, it\'s no longer needed.')
                                            db[str(message.author.id)]['verifycode'] = ""
                                            with open('db.json', 'w') as f:
                                                json.dump(db, f, indent=2)
                                            authorid = message.author.id
                                            server = message.guild
                                            authorroles = message.author.roles
                                            author = message.author
                                            altverify = False
                                            altaccount = None
                                            await checkage(authorid, server, client, authorroles, author, altverify, altaccount)
                                else:
                                    await message.channel.send('<@{}> Er, I couldn\'t find the verification code in either your status or description, perhaps try again?\nTip: Make sure the verification code isn\'t hashtagged/filtered.\nIn the case of filtering/hashtags, change your verification code using {}newcode.'.format(message.author.id,config[str(message.guild.id)]['prefix']))
                            else:
                                await message.channel.send('<@{}> Uh-oh, I got an HTTP error code {}'.format(message.author.id, r.status))
            else:
                await message.channel.send('<@{}> You cannot use {}done if you haven\'t verified yet.\nStart your verification process using {}verify.'.format(message.author.id, config[str(message.guild.id)]['prefix'],config[str(message.guild.id)]['prefix']))


@client.command(pass_context=True)
async def gameaccess(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.guild == None:
            await message.author.send('Sorry, but you cannot use \'gameaccess\' in a DM with me.')
        else:
            if config[str(message.guild.id)]['verifiedrole'] in [role.id for role in message.author.roles]:
                try:
                    with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                        gameaccessdb = json.load(m)
                    if str(db[str(message.author.id)]['userid']) in gameaccessdb:
                        if gameaccessdb[str(db[str(message.author.id)]['userid'])]:
                            await message.channel.send('<@{}> You already have game access.'.format(message.author.id))
                        else:
                            await message.channel.send('<@{}> Your GameAccess was revoked/disabled by the server administration team.'.format(message.author.id))
                    else:
                        gameaccessdb[str(db[str(message.author.id)]['userid'])] = True
                        with open("gameaccess/{}.json".format(str(message.guild.id)), 'w') as m:
                            json.dump(gameaccessdb, m, indent=2)
                        await message.channel.send('<@{}> Granted you access to the game.'.format(message.author.id))
                except KeyError:
                    await message.channel.send('<@{}> Error: Your database listing seems to be corrupted or gone, try reverifying yourself.'.format(message.author.id))
            else:
                await message.channel.send('<@{}> Sorry, but blacklisted or non-verified users cannot have game access.'.format(message.author.id))

@client.command(pass_context=True)
async def newcode(ctx):
    message = ctx.message
    if not message.author.bot:
        if str(message.author.id) in db:
            if db[str(message.author.id)]['verifycode'] != "":
                db[str(message.author.id)]['verifycode'] = verifycode_generator()
                with open('db.json', 'w') as f:
                    json.dump(db, f, indent=2)
                await message.channel.send('<@{}> Please check your DMs for your **new** verify code.'.format(message.author.id))
                try:
                    await message.author.send('Please enter the following **new** verify code in your ROBLOX account\'s status or description to prove your authenticity: ```{}```\nAfter adding the verification code, type {}done in the channel.\nThe username you entered was ``{}``; Incase of an error or typo, enter {}cancel in channel and try again.'.format(db[str(message.author.id)]["verifycode"],config[str(message.guild.id)]['prefix'],db[str(message.author.id)]['rblxusername'],config[str(message.guild.id)]['prefix']))
                except discord.errors.Forbidden:
                    await message.channel.send('<@{}> I wasn\'t unable to DM you, please fix your privacy settings or unblock the bot, then run {}newcode again.'.format(message.author.id,config[str(message.guild.id)]['prefix']))
            else:
                await message.channel.send('<@{}> You\'re already verified.'.format(message.author.id))
        else:
            await message.channel.send('<@{}> You haven\'t started any process of verifying, begin using {}verify first to start verifying your ROBLOX account.'.format(message.author.id, config[str(message.guild.id)]['prefix']))


@client.command(pass_context=True)
async def settings(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.guild == None:
            await message.author.send('You cannot use the settings command in a DM with me.')
        else:
            if str(message.author.id) in (str(message.guild.owner_id), str(message.author.guild_permissions.administrator), str(message.author.guild_permissions.manage_guild), config['ownerid']):
                if str(message.guild.id) not in config:
                    await message.channel.send('<@{}> This server is somehow not added into my database, fixing that...'.format(message.author.id))
                    config[str(message.guild.id)] = {
                    'verifychannel': '',
                    'verifiedrole': '',
                    'altrole': '',
                    'blacklistedrole': '',
                    'verified-logs': '',
                    'rverifyplus-alerts': '',
                    'game-logs': '',
                    'autoverify': False,
                    'changenickonverify': False,
                    'gameaccess': False,
                    'noobdetection': {
                    'Enabled': False,
                    'level': 3
                    },
                    'autogameaccess': False,
                    'serverapikey': "",
                    'unverifiedrole': "",
                    'prefix': str(config['defaultprefix']),
                    'minage': "60",
                    'welcomemessage': "",
                    'permitalts': True
                    }
                    with open('config.json', 'w') as g:
                        json.dump(config, g, indent=2)
                    await message.channel.send('<@{}> Server added, run {}settings again to finish configuring it.'.format(config[str(message.guild.id)]['prefix']))
                else:
                    parsedmessage = message.content.replace('{}settings'.format(config[str(message.guild.id)]['prefix']), '')
                    one = config[str(message.guild.id)]['verifychannel']
                    two = config[str(message.guild.id)]['verifiedrole']
                    three = config[str(message.guild.id)]['blacklistedrole']
                    four = config[str(message.guild.id)]['verified-logs']
                    five = config[str(message.guild.id)]['rverifyplus-alerts']
                    six = config[str(message.guild.id)]['autoverify']
                    seven = config[str(message.guild.id)]['changenickonverify']
                    eight = config[str(message.guild.id)]['gameaccess']
                    try: # Keep this for atleast a while until my mess is resolved.
                        nine = config[str(message.guild.id)]['noobdetection']['Enabled']
                    except TypeError:
                        print("Server ID {} has a broken noobdetection, fixing that.")
                        del config[str(message.guild.id)]['noobdetection']
                        config[str(message.guild.id)]['noobdetection'] = {
                        'Enabled': False,
                        'level': 3
                        }
                        with open('config.json', 'w') as g:
                            json.dump(config, g, indent=2)
                    nine = config[str(message.guild.id)]['noobdetection']['Enabled']
                    nine_one = config[str(message.guild.id)]['noobdetection']['level']
                    ten = config[str(message.guild.id)]['autogameaccess']
                    eleven = config[str(message.guild.id)]['serverapikey']
                    twelve = config[str(message.guild.id)]['prefix']
                    thirteen = config[str(message.guild.id)]['unverifiedrole']
                    fourteen = config[str(message.guild.id)]['minage']
                    fifteen = config[str(message.guild.id)]['welcomemessage']
                    sixteen = config[str(message.guild.id)]['permitalts']
                    seventeen = config[str(message.guild.id)]['altrole']
                    #eighteen = config[str(message.guild.id)]['modaccess']
                    #nineteen = config[str(message.guild.id)]['adminaccess']
                    if config[str(message.guild.id)]['verifychannel'] == 0 or config[str(message.guild.id)]['verifychannel'] == "" or config[str(message.guild.id)]['verifychannel'] == "None":
                        one = "Not set"
                        one_name = "Not set"
                    else:
                        one_name = message.guild.get_channel(one)
                    if config[str(message.guild.id)]['verifiedrole'] == 0 or config[str(message.guild.id)]['verifiedrole'] == "None" or config[str(message.guild.id)]['verifiedrole'] == "":
                        two = "Not set"
                        two_name = "Not set"
                    else:
                        two_name = discord.utils.get(ctx.message.guild.roles, id=two)
                    if config[str(message.guild.id)]['blacklistedrole'] == 0 or config[str(message.guild.id)]['blacklistedrole'] == "None" or config[str(message.guild.id)]['blacklistedrole'] == "":
                        three = "Not set"
                        three_name = "Not set"
                    else:
                        three_name = discord.utils.get(ctx.message.guild.roles, id=config[str(message.guild.id)]['blacklistedrole'])
                    if config[str(message.guild.id)]['unverifiedrole'] == 0 or config[str(message.guild.id)]['unverifiedrole'] == "None" or config[str(message.guild.id)]['unverifiedrole'] == "":
                        thirteen = "Not set"
                        thirteen_name = "Not set"
                    else:
                        thirteen_name = discord.utils.get(ctx.message.guild.roles, id=config[str(message.guild.id)]['unverifiedrole'])
                    if config[str(message.guild.id)]['altrole'] == 0 or config[str(message.guild.id)]['altrole'] == "None" or config[str(message.guild.id)]['altrole'] == "":
                        seventeen = "Not set"
                        seventeen_name = "Not set"
                    else:
                        seventeen_name = discord.utils.get(ctx.message.guild.roles, id=config[str(message.guild.id)]['altrole'])
                    if config[str(message.guild.id)]['verified-logs'] == 0 or config[str(message.guild.id)]['verified-logs'] == "None" or config[str(message.guild.id)]['verified-logs'] == "":
                        four = "Not set"
                        four_name = "Not set"
                    else:
                        four_name = message.guild.get_channel(config[str(message.guild.id)]['verified-logs'])
                    if config[str(message.guild.id)]['rverifyplus-alerts'] == 0 or config[str(message.guild.id)]['rverifyplus-alerts'] == "None" or config[str(message.guild.id)]['rverifyplus-alerts'] == "":
                        five = "Not set"
                        five_name = "Not set"
                    else:
                        five_name = message.guild.get_channel(config[str(message.guild.id)]['rverifyplus-alerts'])

                    if len(parsedmessage) < 3:
                        await message.channel.send('**SERVER SETTINGS FOR {}**```\nVerify channel (VERCHAN): #{} (ID: {})\nVerified Role (VERROLE): {} (ID: {})\nVerified Alt Role (altrole): {} (ID: {})\nBlacklisted Role (BLROLE): {} (ID: {})\nUnVerified Role (UNROLE): {} (ID: {})\nVerified-logs channel (VERLOGS): #{} (ID: {})\nRVerifyPlus-alerts channel (ALERTCHAN): #{} (ID: {})\nAuto-Verify member on join (AUTOVERIFY): {}\nChange member\'s nick on verify (CHNICK): {}\nEnable gameaccess (GA): {}\nEnable noob detection (ND): {}\nAuto Gameaccess (AutoGA): {}\nServerAPIKey (API)\nMinimum Account Age (MINAGE): {} days\nCommand prefix (PREFIX): {}```\nTo change a setting, specify it with {}settings SHORTCODE. Ex: {}settings ALERTCHAN.'.format(ctx.message.guild.name, one_name, one, two_name, two, seventeen_name, seventeen, three_name, three, thirteen_name, thirteen, four_name, four, five_name, five, six, seven, eight, nine, ten, fourteen, twelve, twelve, twelve))
                    else:
                        if parsedmessage.split()[0].lower() == "verchan":
                            if len(parsedmessage) == len("VERCHAN") + 1:
                                await message.channel.send('```Verify channel (VERCHAN): {} (#{})```\nTo change it, add the Channel ID or name next to VERCHAN, or to allow any channel, set it to "None". Ex: {}settings VERCHAN ID OR {}settings VERCHAN #channame'.format(one, ctx.message.guild.get_channel(one),twelve,twelve))
                            else:
                                try:
                                    parsedmessage2 = re.sub('<#', '', parsedmessage.split()[1])
                                    parsedmessage3 = re.sub('>', '', parsedmessage2)
                                    try:
                                        if parsedmessage3.lower() == "none":
                                            await message.channel.send('(Specific) Verify channel has been **disabled** for this server.')
                                            config[str(message.guild.id)]['verifychannel'] = 0
                                            with open('config.json', 'w') as g:
                                                json.dump(config, g, indent=2)
                                        else:
                                            if ctx.message.guild.get_channel(int(parsedmessage3)) != None:
                                                perms = ctx.message.guild.get_channel(int(parsedmessage3)).permissions_for(message.guild.me)
                                                if not perms.send_messages or not perms.read_messages:
                                                    await message.channel.send('Error: That channel exists, but I do not have the proper permissions to access it (I need send and read messages for minimal functionality in VERCHAN, recommended to have manage messages included.)')
                                                else:
                                                    await message.channel.send('Verify channel has been set to ```{} ({})``` for this server.'.format(parsedmessage3, ctx.message.guild.get_channel(int(parsedmessage3))))
                                                    config[str(message.guild.id)]['verifychannel'] = int(parsedmessage3)
                                                    with open('config.json', 'w') as g:
                                                        json.dump(config, g, indent=2)
                                            else:
                                                await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(ctx.message.author.id, parsedmessage.split()[1]))

                                    except KeyError:
                                        await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(ctx.message.author.id, parsedmessage.split()[1]))

                                    except ValueError:
                                        await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(ctx.message.author.id, parsedmessage.split()[1]))

                                except IndexError:
                                    await message.channel.send('```Verify channel (VERCHAN): {} (#{})```\nTo change it, add the Channel ID or name next to VERCHAN. Ex: {}settings VERCHAN ID OR {}settings VERCHAN #channame'.format(one, ctx.message.guild.get_channel(one),twelve,twelve))
                        if parsedmessage.split()[0].lower() == "verrole":
                            if len(parsedmessage) == len("VERROLE") + 1:
                                await message.channel.send('```Verified Role (VERROLE): {}```\nTo change it, add the role name or ID next to VERROLE. Ex: {}settings VERROLE RoleName'.format(two_name,twelve))
                            else:
                                role = discord.utils.get(message.guild.roles, name=' '.join(parsedmessage.split()[1:]))
                                if role != None:
                                    await message.channel.send('Verified role has been set to ```{} (ID: {})``` for this server.'.format(' '.join(parsedmessage.split()[1:]), role.id))
                                    config[str(message.guild.id)]['verifiedrole'] = role.id
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                else:
                                    await message.channel.send('<@{}> Error: The role "{}" doesn\'t exist on this server.\nTip: Make sure you are using the *correct* role name, and not a highlight (Highlight as in @VerifiedRole).'.format(ctx.message.author.id, ' '.join(parsedmessage.split()[1:])))
                        if parsedmessage.split()[0].lower() == "altrole":
                            if len(parsedmessage) == len("ALTROLE") + 1:
                                if len(str(config[str(message.guild.id)]['altrole'])) < 3 or len(str(config[str(message.guild.id)]['altrole'])) == 0:
                                    await message.channel.send('```Alt Verified Role (ALTROLE): Disabled```\nTo enable it, add the role name or ID next to ALTROLE. Ex: {}settings ALTROLE RoleName'.format(twelve))
                                else:
                                    await message.channel.send('```Alt Verified Role (ALTROLE): {}```\nTo change it, add the role name or ID next to ALTROLE. Ex: {}settings ALTROLE RoleName'.format(seventeen_name,twelve))
                            else:
                                if parsedmessage.split()[1].lower() != "none":
                                    role = discord.utils.get(message.guild.roles, name=' '.join(parsedmessage.split()[1:]))
                                    if role != None:
                                        await message.channel.send('Verified Alt role has been set to ```{} (ID: {})``` for this server.'.format(' '.join(parsedmessage.split()[1:]), role.id))
                                        config[str(message.guild.id)]['altrole'] = role.id
                                        with open('config.json', 'w') as g:
                                            json.dump(config, g, indent=2)
                                    else:
                                        await message.channel.send('<@{}> Error: The role "{}" doesn\'t exist on this server.\nTip: Make sure you are using the *correct* role name, and not a highlight (Highlight as in @VerifiedRole).'.format(ctx.message.author.id, ' '.join(parsedmessage.split()[1:])))
                                else:
                                    await message.channel.send('<@{}> Alt Verified Role has now been **disabled** for this server.'.format(ctx.message.author.id))
                                    config[str(message.guild.id)]['altrole'] = 0
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                        if parsedmessage.split()[0].lower() == "blrole":
                            if len(parsedmessage) == len("BLROLE") + 1:
                                if len(str(config[str(message.guild.id)]['blacklistedrole'])) < 3:
                                    await message.channel.send('```Blacklisted Role (BLROLE): Disabled```\nTo enable it, add the role name next to BLROLE. Ex: {}settings BLROLE RoleName'.format(twelve))
                                else:
                                    await message.channel.send('```Blacklisted Role (BLROLE): {}```\nTo change it, add the role name next to BLROLE. Ex: {}settings BLROLE RoleName\nTo disable it, Replace RoleName with "None".'.format(three_name,twelve))
                            else:
                                if parsedmessage.split()[1].lower() != "none":
                                    role = discord.utils.get(message.guild.roles, name=' '.join(parsedmessage.split()[1:]))
                                    if role != None:
                                        if role.id != config[str(message.guild.id)]['verifiedrole']:
                                            await message.channel.send('Blacklisted role has been set to ```{} (ID: {})``` for this server.'.format(' '.join(parsedmessage.split()[1:]), role.id))
                                            config[str(message.guild.id)]['blacklistedrole'] = role.id
                                            with open('config.json', 'w') as g:
                                                json.dump(config, g, indent=2)
                                        else:
                                            await message.channel.send('<@{}> You cannot have your blacklisted role the same as your verified role!'.format(ctx.message.author.id))
                                    else:
                                        await message.channel.send('<@{}> Error: The role "{}" doesn\'t exist on this server.'.format(ctx.message.author.id, ' '.join(parsedmessage.split()[1:])))
                                else:
                                    await message.channel.send('<@{}> Blacklisted Role has now been **disabled** for this server.'.format(ctx.message.author.id))
                                    config[str(message.guild.id)]['blacklistedrole'] = 0
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)

                        if parsedmessage.split()[0].lower() == "unrole":
                            if len(parsedmessage) == len("UNROLE") + 1:
                                if len(str(config[str(message.guild.id)]['unverifiedrole'])) < 3 or len(str(config[str(message.guild.id)]['unverifedrole'])) == 0:
                                    await message.channel.send('```UnVerified Role (UNROLE): Disabled```\nTo enable it, add the role name or ID next to UNROLE. Ex: {}settings UNROLE RoleName'.format(twelve))
                                else:
                                    await message.channel.send('```UnVerified Role (UNROLE): {}```\nTo change it, add the role name or ID next to UNROLE. To remove/disable it, use None. Ex: {}settings UNROLE RoleName'.format(thirteen_name,twelve))
                            else:
                                if parsedmessage.split()[1].lower() != "none":
                                    role = discord.utils.get(message.guild.roles, name=' '.join(parsedmessage.split()[1:]))
                                    if role != None:
                                        await message.channel.send('UnVerified role has been set to ```{} (ID: {})``` for this server.'.format(' '.join(parsedmessage.split()[1:]), role.id))
                                        config[str(message.guild.id)]['unverifiedrole'] = role.id
                                        with open('config.json', 'w') as g:
                                            json.dump(config, g, indent=2)
                                    else:
                                        await message.channel.send('<@{}> Error: The role "{}" doesn\'t exist on this server.\nTip: Make sure you are using the *correct* role name, and not a highlight (Highlight as in @VerifiedRole).'.format(message.author.id, ' '.join(parsedmessage.split()[1:])))
                                else:
                                    await message.channel.send('<@{}> Unverified Role has now been **disabled** for this server.'.format(ctx.message.author.id))
                                    config[str(message.guild.id)]['unverifiedrole'] = 0
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                        if parsedmessage.split()[0].lower() == "verlogs":
                            if len(parsedmessage) == len("VERLOGS") + 1:
                                await message.channel.send('```Verified-logs channel (VERLOGS): {} (#{})```\nTo change it, add the Channel ID or name next to VERLOGS. Ex: {}settings VERLOGS ID OR {}settings VERLOGS #channelname'.format(four, message.guild.get_channel(four),twelve,twelve))
                            try:
                                parsedmessage2 = re.sub('<#', '', parsedmessage.split()[1])
                                parsedmessage3 = re.sub('>', '', parsedmessage2)
                                try:
                                    if parsedmessage3.lower() == "none":
                                        await message.channel.send('Verify-logs has been **disabled** for this server.')
                                        config[str(message.guild.id)]['verify-logs'] = 0
                                        with open('config.json', 'w') as g:
                                            json.dump(config, g, indent=2)
                                    else:
                                        if message.guild.get_channel(int(parsedmessage3)) != None:
                                            perms = ctx.message.guild.get_channel(int(parsedmessage3)).permissions_for(message.guild.me)
                                            if not perms.send_messages or not perms.read_messages:
                                                await message.channel.send('Error: That channel exists, but I do not have the proper permissions to access it (I need send and read messages for minimal functionality in VERCHAN, recommended to have manage messages included.)')
                                            else:
                                                await message.channel.send('Verified-logs channel has been set to ```{} (#{})``` for this server.'.format(parsedmessage3, message.guild.get_channel(int(parsedmessage3))))
                                                config[str(message.guild.id)]['verified-logs'] = int(parsedmessage3)
                                                with open('config.json', 'w') as g:
                                                    json.dump(config, g, indent=2)
                                        else:
                                            await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(message.author.id, parsedmessage.split()[1]))

                                except KeyError:
                                    await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(message.author.id, parsedmessage.split()[1]))

                                except ValueError:
                                    await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(message.author.id, parsedmessage.split()[1]))

                            except IndexError:
                                await message.channel.send('```Verified-logs channel (VERLOGS): {} (#{})```\nTo change it, add the Channel ID or name next to VERLOGS. Ex: {}settings VERLOGS ID OR {}settings VERLOGS #channelname'.format(four, message.guild.get_channel(four),twelve,twelve))


                        if parsedmessage.split()[0].lower() == "alertchan":
                            if len(parsedmessage) == len("ALERTCHAN") + 1:
                                await message.channel.send('```RVerifyPlus-alerts channel (ALERTCHAN): {} (#{})```\nTo change it, add the Channel ID or name next to ALERTCHAN, or set it to "None" tp disable. Ex: {}settings ALERTCHAN ID OR {}settings ALERTCHAN #channelname'.format(five, ctx.message.guild.get_channel(five),twelve,twelve))
                            try:
                                parsedmessage2 = re.sub('<#', '', parsedmessage.split()[1])
                                parsedmessage3 = re.sub('>', '', parsedmessage2)
                                try:
                                    if parsedmessage3.lower() == "none":
                                        await message.channel.send('RVerifyPlus-alerts has been **disabled** for this server.')
                                        config[str(message.guild.id)]['rverifyplus-alerts'] = 0
                                        with open('config.json', 'w') as g:
                                            json.dump(config, g, indent=2)
                                    else:
                                        if ctx.message.guild.get_channel(int(parsedmessage3)) != None:
                                            perms = ctx.message.guild.get_channel(int(parsedmessage3)).permissions_for(message.guild.me)
                                            if not perms.send_messages or not perms.read_messages:
                                                await message.channel.send('Error: That channel exists, but I do not have the proper permissions to access it (I need send and read messages for minimal functionality in VERCHAN, recommended to have manage messages included.)')
                                            else:
                                                await message.channel.send('RVerifyPlus-alerts channel has been set to ```{} (#{})``` for this server.'.format(parsedmessage3, message.guild.get_channel(int(parsedmessage3))))
                                                config[str(message.guild.id)]['rverifyplus-alerts'] = int(parsedmessage3)
                                                with open('config.json', 'w') as g:
                                                    json.dump(config, g, indent=2)
                                        else:
                                            await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(message.author.id, parsedmessage.split()[1]))

                                except KeyError:
                                    await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(message.author.id, parsedmessage.split()[1]))

                                except ValueError:
                                    await message.channel.send('<@{}> Error: {} isn\'t a valid channel in this server.'.format(message.author.id, parsedmessage.split()[1]))

                            except IndexError:
                                await message.channel.send('```RVerifyPlus-alerts channel (ALERTCHAN): {} (#{})```\nTo change it, add the Channel ID or name next to ALERTCHAN. Ex: {}settings ALERTCHAN ID OR {}settings ALERTCHAN #channelname'.format(five, message.guild.get_channel(five),twelve,twelve))

                        if parsedmessage.split()[0].lower() == "autoverify":
                            if len(parsedmessage) == len("AUTOVERIFY") + 1:
                                await message.channel.send('```Auto-verify users on join (AUTOVERIFY): {}```\nTo change it, use "True" or "False" (no quotes) next to AUTOVERIFY. Ex: {}settings AUTOVERIFY True'.format(six,twelve))
                            else:
                                if parsedmessage.split()[1].lower() == "True".lower():
                                    await message.channel.send('"Auto-verify users on join" has been **enabled** for this server.'.format(parsedmessage.split()[1]))
                                    config[str(message.guild.id)]['autoverify'] = True
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                elif parsedmessage.split()[1].lower() == "False".lower():
                                    await message.channel.send('"Auto-verify users on join" has been **disabled** for this server.'.format(parsedmessage.split()[1]))
                                    config[str(message.guild.id)]['autoverify'] = False
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                else:
                                    await message.channel.send('<@{}> Error: {} isn\'t either "True" or "False".'.format(message.author.id, parsedmessage.split()[1]))

                        if parsedmessage.split()[0].lower() == "chnick":
                            if len(parsedmessage) == len("CHNICK") + 1:
                                await message.channel.send('```Change nick on-verify (CHNICK): {}```\nTo change it, use "True" or "False" (no quotes) next to CHNICK. Ex: {}settings CHNICK True'.format(seven,twelve))
                            else:
                                if parsedmessage.split()[1].lower() == "True".lower():
                                    await message.channel.send('"Change nick on-verify" has been **enabled** for this server.'.format(parsedmessage.split()[1]))
                                    config[str(message.guild.id)]['changenickonverify'] = True
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                elif parsedmessage.split()[1].lower() == "False".lower():
                                    await message.channel.send('"Change nick on-verify" has been **disabled** for this server.'.format(parsedmessage.split()[1]))
                                    config[str(message.guild.id)]['changenickonverify'] = False
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                else:
                                    await message.channel.send('<@{}> Error: {} isn\'t either "True" or "False".'.format(message.author.id, parsedmessage.split()[1]))

                        if parsedmessage.split()[0].lower() == "ga":
                            if len(parsedmessage) == len("GA") + 1:
                                await message.channel.send('```Gameaccess (GA): {}```\nTo change it, use "True" or "False" (no quotes) next to GA. Ex: {}settings GA True'.format(eight,twelve))
                            else:
                                if parsedmessage.split()[1].lower() == "True".lower():
                                    await message.channel.send('Gameaccess has been **enabled** for this server.'.format(parsedmessage.split()[1]))
                                    config[str(message.guild.id)]['gameaccess'] = True
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                elif parsedmessage.split()[1].lower() == "False".lower():
                                    await message.channel.send('"Gameaccess has been **disabled** for this server.'.format(parsedmessage.split()[1]))
                                    config[str(message.guild.id)]['gameaccess'] = False
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                else:
                                    await message.channel.send('<@{}> Error: {} isn\'t either "True" or "False".'.format(message.author.id, parsedmessage.split()[1]))

                        if parsedmessage.split()[0].lower() == "nd":
                            if len(parsedmessage) == len("ND") + 1:
                                if config[str(message.guild.id)]['noobdetection']:
                                    await message.channel.send('```Noob detection *Now revamped* (ND): {}```\nTo enable/disable, use "True" or "False" (no quotes) next to ND. Ex: {}settings ND True\nTo change the detection level, use level next to ND.'.format(nine,twelve))
                            else:
                                if parsedmessage.split()[1].lower() == "True".lower():
                                    await message.channel.send('Noob detection has been **enabled** for this server.'.format(parsedmessage.split()[1]))
                                    config[str(message.guild.id)]['noobdetection']['Enabled'] = True
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                elif parsedmessage.split()[1].lower() == "False".lower():
                                    await message.channel.send('Noob detection has been **disabled** for this server.'.format(parsedmessage.split()[1]))
                                    config[str(message.guild.id)]['noobdetection']['Enabled'] = False
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                elif parsedmessage.split()[1].lower() == "level".lower():
                                    if len(parsedmessage) == len("nd level") + 1:
                                        await message.channel.send('Current detection level is set to **Level {}**, to change it, add the level number next to ``ND level``, Ex: ``{}settings ND level 4``\nThe higher the level means the more variables it will check for, with the max being 5, and the lowest being 1 (extreme, will trigger if one variable was detected). Works best with age detection setting.'.format(nine_one,twelve))
                                    else:
                                        if parsedmessage.split()[2] == "1" or parsedmessage.split()[2] == "2" or parsedmessage.split()[2] == "3" or parsedmessage.split()[2] == "4" or parsedmessage.split()[2] == "5":
                                            await message.channel.send('Noob detection level has been set to **Level {}** for this server.'.format(parsedmessage.split()[2]))
                                            config[str(message.guild.id)]['noobdetection']['level'] = int(parsedmessage.split()[2])
                                            with open('config.json', 'w') as g:
                                                json.dump(config, g, indent=2)
                                        else:
                                            await message.channel.send('<@{}> Error: {} isn\'t a valid level setting.'.format(message.author.id, parsedmessage.split()[2]))
                                else:
                                    await message.channel.send('<@{}> Error: {} isn\'t a valid option.'.format(message.author.id, parsedmessage.split()[1]))


                        if parsedmessage.split()[0].lower() == "autoga":
                            if len(parsedmessage) == len("AutoGA") + 1:
                                await message.channel.send('```Auto GameAccess (AutoGA): {}```\nTo change it, use "True" or "False" (no quotes) next to AutoGA. Ex: {}settings AutoGA True'.format(nine,twelve))
                            else:
                                if parsedmessage.split()[1].lower() == "true":
                                    await message.channel.send('Ok, Users will no longer need to run {}gameaccess.'.format(twelve))
                                    config[str(message.guild.id)]['autogameaccess'] = True
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                elif parsedmessage.split()[1].lower() == "false":
                                    await message.channel.send('Ok, Users are now required to use {}gameaccess.'.format(twelve))
                                    config[str(message.guild.id)]['autogameaccess'] = False
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                else:
                                    await message.channel.send('<@{}> Error: {} isn\'t either "True" or "False".'.format(message.author.id, parsedmessage.split()[1]))

                        if parsedmessage.split()[0].lower() == "api":
                            if len(parsedmessage) == len("API") + 1:
                                if len(config[str(message.guild.id)]['serverapikey']) > 3:
                                    await message.channel.send('ServerAPIKey (API) is **private** and will be DM\'ed to you.\nTo generate a new one, do {}settings API Generate\nTo remove it, {}settings API Remove'.format(twelve,twelve))
                                    try:
                                        await message.author.send('{}\'s ServerAPIKey is ``{}``, do not share this with anyone who doesn\'t need it.'.format(message.guild.name, config[str(message.guild.id)]['serverapikey']))
                                    except discord.errors.Forbidden:
                                        await message.channel.send('<@{}> Error: I wasn\'t able to DM you, please make sure the bot is unblocked, and DMs are enabled.'.format(message.author.id))
                                else:
                                    await message.channel.send('You have no ServerAPIKey (API) yet. To generate a new key, do {}settings API Generate'.format(twelve,twelve))
                            else:
                                if parsedmessage.split()[1].lower() == "generate":
                                    await message.channel.send('<@{}> Check your DMs for the new ServerAPIKey.'.format(message.author.id))
                                    config[str(message.guild.id)]['serverapikey'] = str(uuid.uuid4())
                                    try:
                                        await message.author.send('{}\'s **new** ServerAPIKey is ``{}``, do not share this with anyone who doesn\'t need it.'.format(message.guild.name, config[str(message.guild.id)]['serverapikey']))
                                    except discord.errors.Forbidden:
                                        await message.channel.send('<@{}> Error: I wasn\'t able to DM you, please make sure the bot is unblocked, and DMs are enabled.'.format(message.author.id))
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)

                                elif parsedmessage.split()[1].lower() == "remove":
                                    await message.channel.send('<@{}> ServerAPIKey has been deleted.'.format(message.author.id))
                                    config[str(message.guild.id)]['serverapikey'] = ""
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                else:
                                    await message.channel.send('<@{}> Error: {} isn\'t a valid option.'.format(message.author.id, parsedmessage.split()[1]))

                        if parsedmessage.split()[0].lower() == "minage":
                            if len(parsedmessage) == len("minage") + 1:
                                await message.channel.send('```Minimum Account Age (minage): {}```\nTo change it, enter the number (in days) you want to use set as the minimum requirement to not be blacklisted **(This ONLY works with blacklistedrole)**. You can also enter "0" if you wish. Ex: {}settings minage 90'.format(fourteen,twelve))
                            else:
                                await message.channel.send('Minimum Account Age has now been changed to {} days'.format(parsedmessage.split()[1]))
                                config[str(message.guild.id)]['minage'] = str(parsedmessage.split()[1])
                                with open('config.json', 'w') as g:
                                    json.dump(config, g, indent=2)

                        if parsedmessage.split()[0].lower() == "prefix":
                            if len(parsedmessage) == len("prefix") + 1:
                                await message.channel.send('```Command prefix (prefix): {}```\nTo change it, enter the symbol you want to use as the prefix for this server, next to prefix. Ex: {}settings prefix %'.format(twelve,twelve))
                            else:
                                await message.channel.send('Changed prefix to {}'.format(parsedmessage.split()[1]))
                                config[str(message.guild.id)]['prefix'] = str(parsedmessage.split()[1])
                                with open('config.json', 'w') as g:
                                    json.dump(config, g, indent=2)
                        if parsedmessage.split()[0].lower() == "wmsg":
                            if len(parsedmessage) == len("wmsg") + 1:
                                await message.channel.send('```Welcome message (wmsg): {}```\nTo change it, enter the message (300 characters max.) you want to use as the welcome message in DMs, when a user joins (if auto-verify is off) for this server. To disable it, replace the message with "None". Ex: {}settings wmsg Welcome to my server! Verify with !verify'.format(fifteen,twelve))
                            else:
                                parsedmessage2 = re.sub(' wmsg ', '', parsedmessage)
                                if len(parsedmessage2) <= 300:
                                    if parsedmessage2.lower() == "none":
                                        await message.channel.send('Welcome message has been disabled!')
                                        config[str(message.guild.id)]['welcomemessage'] = ""
                                        with open('config.json', 'w') as g:
                                            json.dump(config, g, indent=2)
                                    else:
                                        await message.channel.send('Changed welcome message to "{}"'.format(parsedmessage2))
                                        config[str(message.guild.id)]['welcomemessage'] = str(parsedmessage2)
                                        with open('config.json', 'w') as g:
                                            json.dump(config, g, indent=2)
                                else:
                                    await message.channel.send('<@{}> Error: That welcome message exceeds the 300 character limit.'.format(ctx.message.author.id))
            else:
                await message.channel.send("<@{}> Permission denied - Server Owner/Admin command only.".format(ctx.message.author.id))

@client.command(pass_context=True)
async def complaint(ctx):
    message = ctx.message
    if not message.author.bot:
        parsedmessage = message.content.replace('{}complaint'.format(config[str(message.guild.id)]['prefix']), '')
        if len(parsedmessage) > 3:
            if message.author.id in complaintcounter:
                complaintcounter['number'] = int(complaintcounter['number']) + 1
                if int(complaintcounter[str(message.author.id)]['ratelimit']) < int(time.time()) - 3600:
                    if str(message.guild.id) in complaintcounter:
                        if int(complaintcounter[str(message.guild.id)]['ratelimit']) < int(time.time()) - 600:
                            await client.send_message(client.get_channel(config[config['officialserver']]['complaint-logs']), '**Complaint __#{}__**\nUser: **{}**\nGuild: ``{} (ID: {})``\nChannel: ``#{}``\nTime: __{} EST__\nMessage:\n```{}```'.format(complaintcounter['number'], message.author, message.guild.name, message.guild.id, message.channel.name, time.strftime("%H:%M:%S", time.localtime()), parsedmessage))
                            complaintcounter[str(message.guild.id)]['ratelimit'] = int(time.time())
                            with open('complaintcounter.json', 'w') as z:
                                json.dump(complaintcounter, z, indent=2)
                        else:
                            await message.channel.send('<@{}> Error: This command is being server ratelimited! (10 minutes per server, per complaint)'.format(message.author.id))
                    else:
                        complaintcounter['number'] = int(complaintcounter['number']) + 1
                        getchannel = client.get_channel(config[config['officialserver']]['complaint-logs'])
                        await getchannel.send('**Complaint __#{}__**\nUser: **{}**\nGuild: ``{} (ID: {})``\nChannel: ``#{}``\nTime: __{} EST__\nMessage:\n```{}```'.format(complaintcounter['number'], message.author, message.guild.name, message.guild.id, message.channel.name, time.strftime("%H:%M:%S", time.localtime()), parsedmessage))
                        complaintcounter[str(message.guild.id)] = {
                        "ratelimit": int(time.time())
                        }
                        with open('complaintcounter.json', 'w') as z:
                            json.dump(complaintcounter, z, indent=2)
                else:
                    await message.channel.send('<@{}> Error: This command is being user ratelimited! (1 hour per user, per complaint)'.format(message.author.id))
            else:
                complaintcounter['number'] = int(complaintcounter['number']) + 1
                if str(message.guild.id) in complaintcounter:
                    if int(complaintcounter[str(message.guild.id)]['ratelimit']) < int(time.time()) - 600:
                        getchannel = client.get_channel(config[config['officialserver']]['complaint-logs'])
                        await getchannel.send('**Complaint __#{}__**\nUser: **{}**\nGuild: ``{} (ID: {})``\nChannel: ``#{}``\nTime: __{} EST__\nMessage:\n```{}```'.format(complaintcounter['number'], message.author, message.guild.name, message.guild.id, message.channel.name, time.strftime("%H:%M:%S", time.localtime()), parsedmessage))
                        complaintcounter[str(message.guild.id)]['ratelimit'] = int(time.time())
                        with open('complaintcounter.json', 'w') as z:
                            json.dump(complaintcounter, z, indent=2)
                    else:
                        await message.channel.send('<@{}> Error: This command is being server ratelimited! (10 minutes per server, per complaint)'.format(message.author.id))
                else:
                    complaintcounter['number'] = int(complaintcounter['number']) + 1
                    getchannel = client.get_channel(config[config['officialserver']]['complaint-logs'])
                    await getchannel.send('**Complaint __#{}__**\nUser: **{}**\nGuild: ``{} (ID: {})``\nChannel: ``#{}``\nTime: __{} EST__\nMessage:\n```{}```'.format(complaintcounter['number'], message.author, message.guild.name, message.guild.id, message.channel.name, time.strftime("%H:%M:%S", time.localtime()), parsedmessage))
                    complaintcounter[str(message.guild.id)] = {
                    "ratelimit": int(time.time())
                    }
                    with open('complaintcounter.json', 'w') as z:
                        json.dump(complaintcounter, z, indent=2)
                complaintcounter[str(message.author.id)] = {
                "ratelimit": int(time.time())
                }
                with open('complaintcounter.json', 'w') as z:
                    json.dump(complaintcounter, z, indent=2)

@client.command(pass_context=True)
async def leaveserver(ctx):
    if not ctx.message.author.bot:
        message = ctx.message
        parsedmessage = message.content.replace('{}leaveserver'.format(config[str(message.guild.id)]['prefix']), '')
        if len(parsedmessage) < 3:
            if str(message.author.id) == config['ownerid'] or ctx.message.author.id == ctx.message.guild.owner_id or ctx.message.author.guild_permissions.administrator:
                await message.channel.send("<@{}> :warning: Are you sure you want me to depart from {}? By doing so, the server's local database, gameaccess file (If exists), and server settings will be **forever deleted!**\n***Enter the ID of the server to continue, or otherwise respond with \"No\".***\nCommand will timeout in 60 seconds.".format(message.author.id, message.guild.name))
                msg = await client.wait_for('message', check=check, timeout=60)
                if msg == None:
                    await message.channel.send("<@{}> Command has timed out.".format(message.author.id))
                elif "No" in msg.content:
                    await message.channel.send("<@{}> Canceled.".format(message.author.id))
                elif msg.content == str(message.guild.id):
                    editwhenfinished = await message.channel.send("<@{}> Purging local databases, configs, etc...".format(message.author.id))
                    del config[str(message.guild.id)]
                    with open('config.json', 'w') as g:
                        json.dump(config, g, indent=2)
                    if os.path.exists('serverdBs' + '/{}.db.json'.format(message.guild.id)):
                        os.remove('serverdBs/' + '{}.db.json'.format(message.guild.id))
                    if os.path.exists('gameaccess' + '/{}.json'.format(message.guild.id)):
                        os.remove('gameaccess/' + '{}.json'.format(message.guild.id))
                    await client.edit_message(editwhenfinished, new_content="Purging local databases, configs, etc... **purging complete**")
                    await message.channel.send("Farewell, everyone. :wave:")
                    await client.leave_server(message.guild)
                else:
                    await message.channel.send("<@{}> Incorrect option or server ID, command has been canceled.".format(message.author.id))
        else:
            print("Denied")
@client.command(pass_context=True)
async def help(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.guild == None:
            await message.author.send('See https://rverifyplus.xyz/bot-commands/ to view my list of commands.')
        else:
            if message.channel.permissions_for(message.guild.me).send_messages:
                await message.channel.send('<@{}> See https://rverifyplus.xyz/bot-commands/ to view my list of commands.'.format(message.author.id))
            else:
                try:
                    await message.author.send('See https://rverifyplus.xyz/bot-commands/ to view my list of commands.')
                except discord.errors.Forbidden:
                    pass

async def linkalt2(message, client):
    parsedmessage = message.content.replace('{}linkalt'.format(config[str(message.guild.id)]['prefix']), '')
    parsedmessage2 = parsedmessage.replace(' {}linkalt'.format(config[str(message.guild.id)]['prefix']), '')
    if "{}linkalt".format(config[str(message.guild.id)]['prefix']) in message.content and len(parsedmessage) > 4 and "{}linkalt".format(config[str(message.guild.id)]['prefix']) not in parsedmessage2:
        try:
            db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])] = {}
            db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]['rblxusername'] = parsedmessage2.split()[0]
            if "count" in db[str(message.author.id)]['alts']:
                pass # This is a bandage fix for accounts missing counter.
            else:
                db[str(message.author.id)]['alts']['count'] = 0
                print("{} was missing alt counter and this is now fixed.".format(message.author.id))
        except KeyError:
            db[str(message.author.id)]['alts'] = {}
            db[str(message.author.id)]['alts']['count'] = 0
            db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])] = {}
            db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]['rblxusername'] = parsedmessage2.split()[0]
        #db[str(message.author.id)]["rblxusername"] = parsedmessage2.split()[0]
        try:
            await message.delete()
        except discord.NotFound:
            pass
        except discord.errors.Forbidden:
            pass
        db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]["verifycode"] = verifycode_generator()
        with open('db.json', 'w') as f:
            json.dump(db, f, indent=2)
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(get_roblox_id.format(parsedmessage.split()[0]), headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    await session.close()
                    try:
                        if any(x for x in db.values() if x['userid'] == int(js['Id'])):
                            discordid = str(find_key2(db, int(js['Id']))[0])
                            db[discordid]['markfordeletion'] = True
                            db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]['olddiscord'] = discordid
                            await message.channel.send('<@{}> Warning: This username is currently registered to another user.\nCompleting the verification test will result your old information being deleted.'.format(message.author.id))
                            #await client.send_message(client.get_channel(config[str(message.guild.id)]['rverifyplus-alerts']), '**Notice** <@{}> attempted to use an already verified roblox username "https://roblox.com/users/{}/profile"'.format(message.author.id, json['Id']))
                            with open('db.json', 'w') as f:
                                json.dump(db, f, indent=2)
                    except KeyError:
                        pass
                    try:
                        db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]["userid"] = js['Id']
                        db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]["hidewhois"] = False
                        db[str(message.author.id)]['alts']['count'] = db[str(message.author.id)]['alts']['count'] + 1
                        with open('db.json', 'w') as f:
                            json.dump(db, f, indent=2)
                            await message.channel.send('<@{}> Please check your DMs for further instructions.'.format(message.author.id))
                            try:
                                verifycodereplace = db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]["verifycode"]
                                await message.author.send('Please enter the following set of codes into your ROBLOX account\'s status or description to prove your authenticity: ```{}```\nAfter adding the verification code, type {}done in the channel.\nThe username you entered was ``{}``; Incase of an error or typo, enter {}cancel in channel and try again.'.format(verifycodereplace, config[str(message.guild.id)]['prefix'],db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]['rblxusername'],config[str(message.guild.id)]['prefix']))
                            except discord.errors.Forbidden:
                                await message.channel.send('<@{}> I was unable to DM you, please fix your privacy settings or unblock the bot to continue. Verification has been canceled.'.format(message.author.id))
                    except KeyError:
                        await message.channel.send('<@{}> Error: Invalid username, verification has been canceled.'.format(message.author.id))
                        del db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]
                        with open('db.json', 'w') as f:
                            json.dump(db, f, indent=2)
                elif r.status == 400:
                    await message.channel.send('<@{}> Error: That username doesn\'t exist on ROBLOX, verification has been canceled.'.format(message.author.id))
                    del db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
                else:
                    await message.channel.send('<@{}> Uh-oh, I got an HTTP error code {} with Roblox\'s Web API!'.format(message.author.id, r.status))
                    del db[str(message.author.id)]['alts'][str(parsedmessage2.split()[0])]
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
    else:
        #try:
            #await client.delete_message(message)
        #except discord.errors.Forbidden:
            #pass
        def check(user):
            return user.author.id == message.author.id
        tempmsg = await message.channel.send('<@{}> Please provide a valid ROBLOX username either with {}linkalt, or as the next message in the next 30 seconds. Type "cancel" to cancel verification.'.format(message.author.id, config[str(message.guild.id)]['prefix']))
        try:
             msg = await client.wait_for('message', check=check, timeout=30)
             if msg == None:
                 if message.author.id not in db:
                     await tempmsg.delete()
                     await message.channel.send('<@{}> Verification command has timed out.'.format(message.author.id))
             else:
                 if "cancel" in msg.content or "{}verify".format(config[str(message.guild.id)]['prefix']) in msg.content:
                     await message.channel.send('<@{}> Verification has been canceled.'.format(message.author.id))
                 elif "{}verify".format(config[str(message.guild.id)]['prefix']) in msg.content:
                     pass
                 else:
                     parsedmessage = msg.content.replace('{}linkalt'.format(config[str(message.guild.id)]['prefix']), '')
                     parsedmessage2 = parsedmessage.replace(' {}linkalt'.format(config[str(message.guild.id)]['prefix']), '')
                     #db[str(message.author.id)] = {}
                     #db[str(message.author.id)]["rblxusername"] = parsedmessage.split()[0]\
                     try:
                         db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])] = {}
                         db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]['rblxusername'] = parsedmessage2.split()[0]
                     except KeyError:
                         db[str(message.author.id)]['alts'] = {}
                         db[str(message.author.id)]['alts']['count'] = 0
                         db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])] = {}
                         db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]['rblxusername'] = parsedmessage2.split()[0]
                         with open('db.json', 'w') as f:
                             json.dump(db, f, indent=2)
                     try:
                         await msg.delete()
                     except discord.NotFound:
                         pass
                     except discord.errors.Forbidden:
                         pass
                     db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]["verifycode"] = verifycode_generator()
                     async with aiohttp.ClientSession(loop=loop) as session:
                         async with session.get(get_roblox_id.format(parsedmessage.split()[0]), headers=headers) as r:
                             if r.status == 200:
                                 js = await r.json()
                                 try:
                                     if any(x for x in db.values() if x['userid'] == int(js['Id'])):
                                         discordid = str(find_key2(db, int(js['Id']))[0])
                                         db[discordid]['markfordeletion'] = True
                                         db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]['olddiscord'] = discordid
                                         await message.channel.send('<@{}> Warning: This username is currently registered to another user.\nCompleting the verification test will result your old information being deleted.'.format(message.author.id))
                                         with open('db.json', 'w') as f:
                                             json.dump(db, f, indent=2)
                                 except KeyError:
                                     pass
                                 try:
                                     db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]["userid"] = js['Id']
                                     db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]["hidewhois"] = False
                                     db[str(message.author.id)]['alts']['count'] = db[str(message.author.id)]['alts']['count'] + 1
                                     with open('db.json', 'w') as f:
                                         json.dump(db, f, indent=2)
                                     await tempmsg.delete()
                                     await message.channel.send('<@{}> Please check your DMs for further instructions.'.format(message.author.id))
                                     try:
                                        verifycodereplace = db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]["verifycode"]
                                        await message.author.send('Please enter the following set of codes into your ROBLOX account\'s status or description to prove your authenticity: ```{}```\nAfter adding the verification code, type {}done in the channel.\nThe username you entered was ``{}``; Incase of an error or typo, enter {}cancel in channel and try again.'.format(verifycodereplace,config[str(message.guild.id)]['prefix'],db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]['rblxusername'],config[str(message.guild.id)]['prefix']))
                                     except discord.errors.Forbidden:
                                         await message.channel.send('<@{}> I was unable to DM you, please fix your privacy settings or unblock the bot to continue. Verification has been canceled.'.format(message.author.id))
                                 except KeyError:
                                     await message.channel.send('<@{}> Error: Invalid username, verification has been canceled.'.format(message.author.id))
                                     del db[str(message.author.id)]['alts'][str(parsedmessage.split()[0])]
                                     with open('db.json', 'w') as f:
                                         json.dump(db, f, indent=2)
                             else:
                                 await message.channel.send('<@{}> Uh-oh, I got an HTTP error code {}'.format(message.author.id, r.status))
        except asyncio.TimeoutError:
            if message.author.id not in db:
                await tempmsg.delete()
                await message.channel.send('<@{}> Verification command has timed out.'.format(message.author.id))


@client.command(pass_context=True)
async def serverlookup(ctx):
    message = ctx.message
    parsedmessage = message.content.replace('{}serverlookup'.format(config[str(message.guild.id)]['prefix']), '')
    parsedmessage2 = parsedmessage.replace(' ', '')
    if not message.author.bot:
        if message.author.id == config['ownerid']:
            n = 0
            for x in client.servers:
                if parsedmessage2 == x.id:
                    n = n + 1
                    break
            if n == 1:
                await message.channel.send('<@{}> **Server Information**\nName: {}\nID: {}\nPopulation: {}\nOwner: {}'.format(message.author.id, x.name, x.id, x.member_count, x.owner))
            else:
                await message.channel.send('<@{}> I am not in that Guild, whose ID you provided for.'.format(message.author.id))

@client.command(pass_context=True)
async def groups(ctx):
    message = ctx.message
    parsedmessage = ctx.message.content.replace('{}groups'.format(config[ctx.message.guild.id]['prefix']), '')
    parsedmessage2 = parsedmessage.replace(' ', '')
    if not message.author.bot:
        if message.guild == None:
            await message.author.send('Sorry, but you cannot use this command in DM with me.')
        else:
            if not config[str(message.guild.id)]['groups']['Enabled']:
                if len(parsedmessage2) < 2:
                    await message.channel.send('<@{}> Groups are not configured for this server yet. Start configuring with {}groups setup'.format(message.author.id, config[str(message.guild.id)]['prefix']))
                else:
                    if parsedmessage2 == "setup":
                        await message.channel.send('**Group configuration for {}**'.format(message.guild.name))
                        await message.channel.send('<@{}> Please specify your **Group ID** you wish to use for this server in the next message, within 120 seconds.'.format(message.author.id))
                        waitforid = await client.wait_for_message(author=message.author, timeout=120)
                        if waitforid == None:
                            pass
                        else:
                            async with aiohttp.get('https://api.roblox.com/groups/{}'.format(waitforid.content, headers=headers)) as r:
                                if r.status == 200:
                                    js = await r.json()
                                    config[str(message.guild.id)]['groups']['Enabled'] = True
                                    config[str(message.guild.id)]['groups']['groupid'] = str(waitforid.content)
                                    config[str(message.guild.id)]['groups']['binds'] = {}
                                    with open('config.json', 'w') as g:
                                        json.dump(config, g, indent=2)
                                    await message.channel.send('<@{}> Basic setup has been complete. To start binding roles, use {}groups bind'.format(message.author.id, config[str(message.guild.id)]['prefix']))
                    else:
                        await message.channel.send('<@{}> Invalid option, did you meant **setup**?'.format(message.author.id))
            else:
                if len(parsedmessage2) < 2:
                    async with aiohttp.get('https://api.roblox.com/groups/{}'.format(config[str(message.guild.id)]['groups']['groupid'], headers=headers)) as r:
                        if r.status == 200:
                            js = await r.json()
                            groupname = js["Name"]
                            groupowner = js["Owner"]["Name"]
                            groupdesc = js["Description"]
                    embed=discord.Embed(title="RVerifyPlus Group Configuration", description="for {}".format(message.guild.name))
                    #embed.set_thumbnail(url="")
                    embed.add_field(name="Group Name", value="{}".format(groupname), inline=True)
                    embed.add_field(name="Group ID", value="{}".format(config[str(message.guild.id)]['groups']['groupid']), inline=True)
                    embed.add_field(name="Group Owner", value="{}".format(groupowner), inline=True)
                    if len(groupdesc) < 300:
                        embed.add_field(name="Group Description", value="{}".format(groupdesc), inline=True)
                    await message.channel.send(embed=embed)
                else:
                    if parsedmessage.split()[0].lower() == "bind":
                        parsedmessage3 = parsedmessage2.replace('bind', '')
                        parsedmessage4 = parsedmessage3.replace(' ', '')
                        if len(parsedmessage4) < 1:
                            await message.channel.send('**Current group binds for {}**'.format(message.guild.name))
                            for x in config[str(message.guild.id)]['groups']['binds']:
                                await asyncio.sleep(0.5)
                                rolename = discord.utils.get(ctx.message.guild.roles, id=config[str(message.guild.id)]['groups']['binds'][x]['rolename'])
                                await message.channel.send('Binding #{}: Rank "{}" is bounded to the role "{}"'.format(config[str(message.guild.id)]['groups']['binds'][x]['bindingnumber'], config[str(message.guild.id)]['groups']['binds'][x]['rank'], rolename))
                            await message.channel.send('To bind more roles, see {}groups bind add'.format(config[str(message.guild.id)]['prefix']))
                        else:
                            if parsedmessage.split()[1] == "add":
                                parsedmessage4 = parsedmessage3.replace('add', '')
                                parsedmessage5 = parsedmessage4.replace(' ', '')
                                if len(parsedmessage5) < 1:
                                    await message.channel.send('<@{}> Syntax: add **Roblox Role Name**'.format(message.author.id))
                                else:
                                    try:
                                        async with aiohttp.get('https://api.roblox.com/groups/{}'.format(config[str(message.guild.id)]['groups']['groupid'], headers=headers)) as r:
                                            if r.status == 200:
                                                js = await r.json()
                                                if ' '.join(parsedmessage.split()[2:]) in str(js['Roles']):
                                                    await message.channel.send('<@{}> Within 120 seconds, specify the role name as the next message to use for "{}"'.format(message.author.id, ' '.join(parsedmessage.split()[2:])))
                                                    waitforname = await client.wait_for_message(author=message.author, timeout=120)
                                                    if waitforname == None:
                                                        pass
                                                    else:
                                                        role = discord.utils.get(ctx.message.guild.roles, name=waitforname.content)
                                                        if role != None:
                                                            await message.channel.send('Binding role has been set! ```{} - {} (ID: {})``` for this server.'.format(' '.join(parsedmessage.split()[2:]), waitforname.content, role.id))
                                                            x = 0
                                                            n = 1
                                                            while x == 0:
                                                                if str(n) in config[ctx.message.guild.id]['groups']['binds']:
                                                                    n = n + 1
                                                                else:
                                                                    x = 1
                                                            config[ctx.message.guild.id]['groups']['binds'][n] = {}
                                                            config[str(message.guild.id)]['groups']['binds'][n]['bindingnumber'] = str(n)
                                                            config[ctx.message.guild.id]['groups']['binds'][n]['rank'] = str(' '.join(parsedmessage.split()[2:]))
                                                            config[ctx.message.guild.id]['groups']['binds'][n]['rolename'] = role.id
                                                            with open('config.json', 'w') as g:
                                                                json.dump(config, g, indent=2)
                                                        else:
                                                            await message.channel.send('<@{}> Error: The role "{}" doesn\'t exist on this server.\nTip: Make sure you are using the *correct* role name, and not a highlight (Highlight as in @VerifiedRole).'.format(ctx.message.author.id, waitforname.content))
                                    except KeyError:
                                        await message.channel.send('<@{}> Error: Invalid Syntax, make sure you included in this format: **RobloxRoleName** **DiscordRoleName**, without the bold.'.format(message.author.id))
                    elif parsedmessage.split()[0].lower() == "unbind":
                        pass


@client.command(pass_context=True)
async def hidewhois(ctx):
    message = ctx.message
    parsedmessage = message.content.replace('{}hidewhois '.format(config[str(message.guild.id)]['prefix']), '')
    if not message.author.bot:
        if message.guild == None:
            pass # Too tired to complete.
        elif str(message.author.id) in db:
            if parsedmessage.lower() == "server true":
                await message.channel.send('<@{}> server-specific whois hide is now enabled for you.'.format(message.author.id))
                db[str(message.author.id)]['ssettings'] = {}
                db[str(message.author.id)]['ssettings'][str(message.guild.id)] = {}
                db[str(message.author.id)]['ssettings'][str(message.guild.id)]['hidewhois'] = True
                with open('db.json', 'w') as f:
                    json.dump(db, f, indent=2)
            elif parsedmessage.lower() == "server false":
                try:
                    del db[str(message.author.id)]['ssettings'][str(message.guild.id)]['hidewhois']
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
                    await message.channel.send('<@{}> server-specific whois hide is now disabled for you.'.format(message.author.id))
                except KeyError:
                    await message.channel.send('<@{}> server-specific whois hide wasn\'t enabled for you.'.format(message.author.id))
            else:
                if parsedmessage.lower() == "true":
                    await message.channel.send('<@{}> whois hide is now enabled for you.'.format(message.author.id))
                    db[str(message.author.id)]['hidewhois'] = True
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
                elif parsedmessage.lower() == "false":
                    await message.channel.send('<@{}> whois hide is now disabled for you.'.format(message.author.id))
                    db[str(message.author.id)]['hidewhois'] = False
                    with open('db.json', 'w') as f:
                        json.dump(db, f, indent=2)
                else:
                    await message.channel.send('<@{}> Syntax: {}hidewhois True (or) False.\n Description: Hides your WHOIS from anyone who isn\'t a server admin/mod, and from other servers that you are not in.\n For server-specific hidewhois, then add a "server" in your command. Example: {}settings server True (or) False'.format(message.author.id,config[str(message.guild.id)]['prefix'],config[str(message.guild.id)]['prefix']))
        else:
            pass

@client.command(pass_context=True)
async def verify(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.guild == None:
            await message.author.send('Sorry, but you cannot verify yourself in a DM with me. You **must** verify in the appropiate verify channel.')
        else:
            if len(str(config[str(message.guild.id)]['verifiedrole'])) > 3:
                if len(str(config[str(message.guild.id)]['verifychannel'])) > 3:
                    if message.channel.id == config[str(message.guild.id)]['verifychannel']:
                        if str(message.author.id) in db:
                            if db[str(message.author.id)]["verifycode"] == "":
                                if config[str(message.guild.id)]['verifiedrole'] in [role.id for role in message.author.roles] or config[str(message.guild.id)]['blacklistedrole'] in [role.id for role in message.author.roles]:
                                    try:
                                        await message.channel.send('<@{}> You already have the verified role! To unverify, use {}unverify instead.'.format(message.author.id,config[str(message.guild.id)]['prefix']))
                                    except discord.errors.Forbidden:
                                        try:
                                            await message.author.send('You already have the verified role! To unverify, use {}unverify (in the server) instead.'.format(message.author.id,config[str(message.guild.id)]['prefix']))
                                        except discord.errors.Forbidden:
                                            pass
                                else:
                                    await userupdate_after_verify(message)
                                    try:
                                        await message.author.send('Welcome back, {}'.format(db[str(message.author.id)]['rblxusername']))
                                    except discord.errors.Forbidden:
                                        pass
                                    try:
                                        await message.delete()
                                    except discord.errors.Forbidden:
                                        pass
                                    authorid = message.author.id
                                    server = message.guild
                                    authorroles = message.author.roles
                                    author = message.author
                                    altverify = False
                                    altaccount = None
                                    if config[str(message.guild.id)]['changenickonverify']:
                                        await changenick(client, author, authorid, server, authorroles)
                                    else:
                                        await checkage(authorid, server, client, authorroles, author, altverify, altaccount)
                            else:
                                await message.channel.send('<@{}> Verification process has already started, check your last DMs with me for the instructions, or {}cancel to cancel then {}verify to try again, or {}done to complete it.'.format(message.author.id,config[str(message.guild.id)]['prefix'],config[str(message.guild.id)]['prefix'],config[str(message.guild.id)]['prefix']))
                        else:
                            await migrate_from_rover(ctx.message, client)
                    else:
                        try:
                            getchannel = message.guild.get_channel(config[str(message.guild.id)]['verifychannel'])
                            await message.channel.send('<@{}> Error: {}verify has been restricted to {} for this server.'.format(message.author.id,config[str(message.guild.id)]['prefix'], getchannel.mention))
                        except discord.errors.Forbidden:
                            getchannel = message.guild.get_channel(config[str(message.guild.id)]['verifychannel'])
                            await message.author.send('Error: {}verify has been restricted to #{} for this server, which I also lack the permissions to speak in.'.format(config[str(message.guild.id)]['prefix'],getchannel.mention))

                else:
                    if str(message.author.id) in db:
                        if db[str(message.author.id)]["verifycode"] == "":
                            if config[str(message.guild.id)]['verifiedrole'] in [role.id for role in message.author.roles] or config[str(message.guild.id)]['blacklistedrole'] in [role.id for role in message.author.roles]:
                                await message.channel.send('<@{}> You already have the verified role! To unverify, use {}unverify instead.'.format(message.author.id,config[str(message.guild.id)]['prefix']))
                            else:
                                try:
                                    await message.author.send('Welcome back, {}'.format(db[str(message.author.id)]['rblxusername']))
                                except discord.errors.Forbidden:
                                    pass
                                try:
                                    await message.delete()
                                except discord.errors.Forbidden:
                                    pass
                                authorid = ctx.message.author.id
                                server = ctx.message.guild
                                authorroles = ctx.message.author.roles
                                author = ctx.message.author
                                altverify = False
                                altaccount = None
                                if config[str(message.guild.id)]['changenickonverify']:
                                    await changenick(client, author, authorid, server, authorroles)
                                else:
                                    await checkage(authorid, server, client, authorroles, author, altverify, altaccount)
                        else:
                            await message.channel.send('<@{}> Verification process has already started, check your last DMs with me for the instructions, or {}cancel to cancel then {}verify to try again, or {}done to complete it.'.format(message.author.id,config[str(message.guild.id)]['prefix'],config[str(message.guild.id)]['prefix'],config[str(message.guild.id)]['prefix']))
                    else:
                        await migrate_from_rover(ctx.message, client)
            else:
                await message.channel.send('<@{}> Error: I haven\'t been configured properly yet, make sure the appropiate verify channel and role has been set using {}settings.'.format(message.author.id,config[str(message.guild.id)]['prefix']))

@client.command(pass_context=True)
async def invitelink(ctx):
    message = ctx.message
    if not message.author.bot:
        if config['botispublic'] == True or str(message.author.id) == config['ownerid']:
            await message.channel.send('<@{}> Check your DMs for the bot-invite link.'.format(message.author.id))
            try:
                await message.author.send('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=402746374\nIf you have any questions on how to set it up/configure/etc, then join the offical discord server, discord.gg/p3uXEEr.\nI need atleast to be able to send and manage others (and self) messages, manage roles, embed links, and read message history.\nAlso make sure my role is higher than the verified/blacklisted roles.'.format(client.user.id))
            except discord.errors.Forbidden:
                await message.channel.send('<@{}> I wasn\'t unable to DM you, please fix your privacy settings or unblock the bot, then try again.'.format(message.author.id))
        else:
            await message.channel.send('<@{}> Sorry, but this bot has been configured to be a private bot.'.format(message.author.id))

@client.command(pass_context=True)
async def whois(ctx):
    message = ctx.message
    if not message.author.bot:
        try:
            user_to_search = message.content.split()[1]
            removetags = re.sub('<@!', '', user_to_search)
            removetags2 = re.sub('<@', '', removetags)
            removetags3 = re.sub('>', '', removetags2)
            if removetags3.isdigit():
                if removetags3 in db and len(db[removetags3]['verifycode']) == 0:
                    try:
                        if db[removetags3]['ssettings'][str(message.guild.id)]['hidewhois']:
                            if message.author.id == message.guild.owner_id or message.author.guild_permissions.administrator or message.author.guild_permissions.manage_guild or message.author.id == config['ownerid'] or db[str(message.author.id)]['userid'] == db[removetags3]['userid']:
                                if message.guild.get_member(int(removetags3)) != None:
                                    try:
                                        await message.author.send('<@{}> is verified as {}\nProfile: https://www.roblox.com/users/{}/profile'.format(removetags3, db[removetags3]['rblxusername'], db[removetags3]['userid']))
                                        with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                            gameaccessdb = json.load(m)
                                            if config[str(message.guild.id)]['gameaccess'] and str(db[removetags3]['userid']) in gameaccessdb:
                                                if gameaccessdb[str(db[removetags3]['userid'])]:
                                                    await message.author.send('The user **does have** GameAccess.')
                                                else:
                                                    await message.author.send('The user has GameAccess **revoked**.')
                                            else:
                                                await message.author.send('The user **does not have** GameAccess.')
                                            await message.author.send('The user **has** Server-Specific WHOIS HIDE enabled.')
                                    except discord.errors.Forbidden:
                                        await message.channel.send('<@{}> Cannot send you WHOIS information because your privacy settings is restricting me from sending you Direct Messages, fix your settings and try again.'.format(message.author.id))
                                else:
                                    await message.channel.send('<@{}> The user **has** Server-Specific WHOIS HIDE enabled, information is restricted from being accessed outside the server they\'re in.'.format(message.author.id))
                            else:
                                await message.channel.send('<@{}> The user **has** Server-Specific WHOIS HIDE enabled, information is restricted to server admins and mods.'.format(message.author.id))
                    except KeyError:
                        if not db[removetags3]['hidewhois']:
                            await message.channel.send('<@{}> is verified as {}\nProfile: https://www.roblox.com/users/{}/profile'.format(removetags3, db[removetags3]['rblxusername'], db[removetags3]['userid']))
                            with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                gameaccessdb = json.load(m)
                                if config[str(message.guild.id)]['gameaccess'] and str(db[removetags3]['userid']) in gameaccessdb:
                                    if gameaccessdb[str(db[removetags3]['userid'])]:
                                        await message.channel.send('The user **does have** GameAccess.')
                                    else:
                                        await message.channel.send('The user has GameAccess **revoked**.')
                                else:
                                    await message.channel.send('The user **does not have** GameAccess.')
                        else:
                            if message.author.id == message.guild.owner_id or message.author.guild_permissions.administrator or message.author.guild_permissions.manage_guild or str(message.author.id) == config['ownerid'] or db[str(message.author.id)]['userid'] == db[removetags3]['userid']:
                                if message.guild.get_member(int(removetags3)) != None:
                                    try:
                                        await message.author.send('<@{}> is verified as {}\nProfile: https://www.roblox.com/users/{}/profile'.format(removetags3, db[removetags3]['rblxusername'], db[removetags3]['userid']))
                                        with open("gameaccess/{}.json".format(message.guild.id)) as m:
                                            gameaccessdb = json.load(m)
                                            if config[str(message.guild.id)]['gameaccess'] and str(db[removetags3]['userid']) in gameaccessdb:
                                                if gameaccessdb[str(db[removetags3]['userid'])]:
                                                    await message.author.send('The user **does have** GameAccess.')
                                                else:
                                                    await message.author.send('The user has GameAccess **revoked**.')
                                            else:
                                                await message.author.send('The user **does not have** GameAccess.')
                                            await message.author.send('The user **has** WHOIS HIDE enabled.')
                                    except discord.errors.Forbidden:
                                        await message.channel.send('<@{}> Cannot send you WHOIS information because your privacy settings is restricting me from sending you Direct Messages, fix your settings and try again.'.format(message.author.id))
                                else:
                                    await message.channel.send('<@{}> The user **has** WHOIS HIDE enabled, information is restricted from being accessed outside the server they\'re in.'.format(message.author.id))
                            else:
                                await message.channel.send('<@{}> The user **has** WHOIS HIDE enabled, information is restricted to server admins and mods.'.format(message.author.id))
                elif removetags3 not in db:
                    await message.channel.send('<@{}> That discord user cannot be found.'.format(message.author.id))
            else:
                try:
                    discordid = find_key2(db, removetags2)[0]
                    try:
                        if db[discordid]['ssettings'][str(message.guild.id)]['hidewhois']:
                            if message.author.id == message.guild.owner_id or message.author.guild_permissions.administrator or message.author.guild_permissions.manage_guild or message.author.id == config['ownerid'] or db[str(message.author.id)]['userid'] == db[discordid]['userid']:
                                if message.guild.get_member(int(discordid)) != None:
                                    try:
                                        await message.author.send('<@{}> is verified as {}\nProfile: https://www.roblox.com/users/{}/profile'.format(discordid, db[discordid]['rblxusername'], db[discordid]['userid']))
                                        with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                            gameaccessdb = json.load(m)
                                            if config[str(message.guild.id)]['gameaccess'] and str(db[discordid]['userid']) in gameaccessdb:
                                                if gameaccessdb[str(db[discordid]['userid'])]:
                                                    await message.author.send('The user **does have** GameAccess.')
                                                else:
                                                    await message.author.send('The user has GameAccess **revoked**.')
                                            else:
                                                await message.author.send('The user **does not have** GameAccess.')
                                            await message.author.send('The user **has** Server-Specific WHOIS HIDE enabled.')
                                    except discord.errors.Forbidden:
                                        await message.channel.send('<@{}> Cannot send you WHOIS information because your privacy settings is restricting me from sending you Direct Messages, fix your settings and try again.'.format(message.author.id))
                                else:
                                    await message.channel.send('<@{}> The user **has** Server-Specific WHOIS HIDE enabled, information is restricted from being accessed outside the server they\'re in.'.format(message.author.id))
                            else:
                                await message.channel.send('<@{}> The user **has** Server-Specific WHOIS HIDE enabled, information is restricted to server admins and mods.'.format(message.author.id))
                    except KeyError:
                        if not db[discordid]['hidewhois']:
                            await message.channel.send('The ROBLOX username "{}" is verified as <@{}>'.format(db[discordid]['rblxusername'], discordid))
                            with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                gameaccessdb = json.load(m)
                                if config[str(message.guild.id)]['gameaccess'] and str(db[discordid]['userid']) in gameaccessdb:
                                    if gameaccessdb[str(db[discordid]['userid'])]:
                                        await message.channel.send('The user **does have** GameAccess.')
                                    else:
                                        await message.channel.send('The user has GameAccess **revoked**.')
                                else:
                                    await message.channel.send('The user **does not have** GameAccess.')
                        else:
                            if message.author.id == message.guild.owner_id or message.author.guild_permissions.administrator or message.author.guild_permissions.manage_guild or message.author.id == config['ownerid'] or db[str(message.author.id)]['userid'] == db[discordid]['userid']:
                                if message.guild.get_member(discordid) != None:
                                    try:
                                        await message.author.send('<@{}> is verified as {}\nProfile: https://www.roblox.com/users/{}/profile'.format(discordid, db[discordid]['rblxusername'], db[discordid]['userid']))
                                        with open("gameaccess/{}.json".format(str(message.guild.id))) as m:
                                            gameaccessdb = json.load(m)
                                            if config[str(message.guild.id)]['gameaccess'] and str(db[discordid]['userid']) in gameaccessdb:
                                                if gameaccessdb[str(db[discordid]['userid'])]:
                                                    await message.author.send('The user **does have** GameAccess.')
                                                else:
                                                    await message.author.send('The user has GameAccess **revoked**.')
                                            else:
                                                await message.author.send('The user **does not have** GameAccess.')
                                            await message.author.send('The user **has** WHOIS HIDE enabled.')
                                    except discord.errors.Forbidden:
                                        await message.channel.send('<@{}> Cannot send you WHOIS information because your privacy settings is restricting me from sending you Direct Messages, fix your settings and try again.'.format(message.author.id))
                                else:
                                    await message.channel.send('<@{}> The user **has** WHOIS HIDE enabled, information is restricted from being accessed outside the server they\'re in.'.format(message.author.id))
                            else:
                                await message.channel.send('<@{}> The user **has** WHOIS HIDE enabled, information is restricted to server admins and mods.'.format(message.author.id))
                except TypeError:
                    await message.channel.send('<@{}> That roblox username couldn\'t be found. This type of search is case sensitive when it comes to usernames.'.format(message.author.id))
        except IndexError:
            await message.channel.send('<@{}> Syntax: {}whois DiscordID/Roblox Username (case-sensitive) (Better searching still in development.)'.format(message.author.id,config[str(message.guild.id)]['prefix']))

@client.command(pass_context=True)
async def ping(ctx):
    message = ctx.message
    if not message.author.bot:
        await message.channel.send("<@{}> Pong!".format(message.author.id))

@client.command(pass_context=True)
async def roleid(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.author.id == message.guild.owner_id or message.author.guild_permissions.administrator or message.author.guild_permissions.manage_guild or str(message.author.id) == config['ownerid']:
            parsedmessage = ctx.message.content.replace('{}roleid'.format(config[str(message.guild.id)]['prefix']), '')
            if len(parsedmessage) > 1:
                role = discord.utils.get(message.guild.roles, name=' '.join(parsedmessage.split()[0:]))
                if role != None:
                    await message.channel.send('<@{}> This role id is ``{}``'.format(message.author.id, role.id))
                else:
                    await message.channel.send('<@{}> Error: The role "{}" doesn\'t exist on this server.\nTip: Make sure you are using the *correct* role name, and not a highlight (Highlight as in @VerifiedRole).'.format(ctx.message.author.id, ' '.join(parsedmessage.split()[0:])))
            else:
                await message.channel.send('<@{}> Syntax: {}roleid rolename. This command grabs you the ID of the role.'.format(message.author.id,config[str(message.guild.id)]['prefix']))
        else:
            await message.channel.send("<@{}> Permission denied - Server Owner/Admin command only.".format(ctx.message.author.id))


@client.command(pass_context=True)
async def ban(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.author.id == config['ownerid'] or message.author.guild_permissions.administrator:
            if int(message.content.split()[1]) > 1:
                persontoban = message.guild.get_member(int(message.content.split()[1]))
                await persontoban.ban(delete_message_days=7)
                await message.delete()

@client.command(pass_context=True)
async def kick(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.author.id == config['ownerid'] or message.author.guild_permissions.administrator:
            if message.content.split()[1] > 1:
                persontokick = message.guild.get_member(message.content.split()[1])
                await client.kick(persontokick)

@client.command(pass_context=True)
async def linkalt(ctx):
    message = ctx.message
    if not message.author.bot:
        if message.guild == None:
            await message.author.send('For security reasons, You cannot use this command in a DM with me.')
        else:
            if str(message.author.id) in db:
                await linkalt2(message, client)
            else:
                await message.channel.send('<@{}> You haven\'t verify at all yet. You must do this before you can start linking alts to your account. Verify with {}verify'.format(message.author.id,config[str(message.guild.id)]['prefix']))

@client.event
async def on_message(message):

 if message.content.startswith('RVerify RVerify'):
     if str(message.author.id) == config['ownerid']:
          await message.channel.send("Yes papa")

 if message.content.startswith('*quit'):
     if not message.author.bot:
          if message.author.id == config['ownerid']:
              await message.channel.send("Shutting down.")
              exit("Shutdown")
          else:
             await message.channel.send("<@{}> Permission denied - Owner command only.".format(message.author.id))

 await client.process_commands(message)

@asyncio.coroutine
def main_task():
    print("Performing user database integrity check before connecting...")
    q = 0
    if len([x for x in db.values() if 'userid' not in x]) != 0:
        brokenid = [x['rblxusername'] for x in db.values() if 'userid' not in x]
        discordid = str(find_key2(db, re.sub(r'[^\w]', '', str(brokenid)).replace(' ', ''))[0])
        q = q + 1
        del db[discordid]
        with open('db.json', 'w') as f:
            json.dump(db, f, indent=2)

    if q >= 1:
        print("{} user(s) database was corrupted and is now repaired.".format(q))
    else:
        print("User Database integrity check completed; No corruption found.")

    n = 0
    z = 0
    for x in db:
        if "hidewhois" not in db[x]:
            db[x]['hidewhois'] = False
            n = n + 1
        else:
            z = z + 1
    print("{} was missing hidewhois".format(n))
    print("{} had hidewhois".format(z))
    with open('db.json', 'w') as f:
        json.dump(db, f, indent=2)
    yield from client.login(config['token'])
    yield from client.connect()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main_task())
except:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
