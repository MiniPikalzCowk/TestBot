import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
import os
import urllib.request
import re
import time
from html.parser import HTMLParser
bot = commands.Bot(command_prefix="-")
bot_token = os.environ['BOT_TOKEN']
def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

def replacesbs(s,sb,nsb):
    if find_str(s,sb) > -1:
        currentOne = s[:find_str(s,sb)]
        length = len(sb)
        currentOne = currentOne + nsb + s[find_str(s,sb)+length:]
        return currentOne
    else:
        return s



@bot.command(pass_context=False)
async def Check():
    roles = []
    f = open("Roles2","a+")
    f.seek(0)
    texted = f.read()
    await bot.say("Starting Check-Up of rank changes...")
    #print(urllib.request.urlopen("https://groups.roblox.com/v1/groups/4071297/roles/27596202/users?sortOrder=Asc&limit=100").read().decode())
    h = urllib.request.urlopen("https://groups.roblox.com/v1/groups/4071297/roles")
    kek = h.read().decode()
    currentStringStuff = ""
    if "\"id\"" in kek:
        while True:
            if not "\"id\"" in kek:
                break
            newstring = kek[find_str(kek,"\"id\"" )+5:]
            newstring2 = newstring[find_str(newstring,",")+9:]
            roles.append([newstring[:find_str(newstring,",")],newstring2[:find_str(newstring2,",")-1]])
            kek = replacesbs(kek,"\"id\"","")
    for x in roles:
        url = "https://groups.roblox.com/v1/groups/4071297/roles/" + x[0] + "/users?sortOrder=Asc&limit=100"
        lol = urllib.request.urlopen(url)
        
        
        this = lol.read().decode()
        currentUpdateString = x[1] + "s:"
        
        if "username\"" in this:
            while True:
                if not "username\"" in this:
                   break
                newstring = this[find_str(this,"username\"")+11:]
                username = newstring[:find_str(newstring,"\"")]
                currentUpdateString = currentUpdateString + " " + username
                this = replacesbs(this,"username\"","")
                if username in texted:
                    

                    unranked = texted[find_str(texted,username)+len(username)+1:]
                    rank = unranked[:find_str(unranked,"'")]
                    if rank != x[1]:
                        
                        await bot.say("**" + username + "'s** rank has changed from **" + rank + "** to **" + x[1] + ".**" )
                        part1 = texted[:find_str(texted,username)]
                        part2 = texted[find_str(texted,username)+2+len(username)+len(rank):]
                        currentStringStuff = part1 + username + ";" + x[1] + "'" + part2
                        
                        time.sleep(0.1)
                else:

                    currentStringStuff = currentStringStuff + username + ";" + x[1] + "'"
                    time.sleep(0.1)
        
        #await bot.say(currentUpdateString)
        time.sleep(0.1)
    f.close()
    f = open("Roles2","w+")
    time.sleep(0.5)
    f.write(currentStringStuff)
    time.sleep(1)
    await bot.say("Rank Check-Up complete!")
    f.close()
    
    bot.run(bot_token)
