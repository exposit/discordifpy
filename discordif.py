#!/usr/bin/python
# This is discordifpy, a simple discord bot for running IF games. It is not trivial to get working.
# for more information beyond the readme and a somewhat relevant tutorial please see
# https://github.com/exposit/slackifpy
# licensed under MIT as applicable
# please use with caution as I am no expert
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import random
import subprocess
import threading
import time
import sys
import os
from secret import token

if sys.version_info.major >= 3:
    import queue
else:
    import Queue as queue
    input = raw_input

# put your token here (or put this line in a separate file named "secret.py")
#token = ""

# set your channel id for the bot to respond in; in the discord app, go to your settings -> appearance and activate developer mode. Then right click on the channel you want and click 'copy id'.
ifchannel = "522833461870854145"

# the prefix the bot will listen for
prefix = "!"

# set paths
game_path = "./games/"
terp_path = "./terps/"

# some general messaging from ifbot to Slack
start_msg = "_is starting the game._\n*..... GAME START .....*\n\n"
end_msg = "_is shutting the game down._\n*..... GAME END .....*\n"
default_status = "nothing at the moment"

# format game output as a code block, true or false. Default is not to.
format_code_block = False

# hard clean format
format_clean = True

game_active = False

# now open up the game database and parse it
with open(os.path.join(game_path, 'games.txt'), 'r') as g:
    games = g.readlines()

games = [x for x in games if not x == "\n"]
curr = games[0].strip()
sorted = {}
sorted[curr] = {}
for line in games:
    if line.startswith('  '):
        a,b = line.strip().split(':', 1)
        sorted[curr][a] = b.strip()
    else:
        curr = line.strip()
        sorted[curr] = {}

exclude_list = {}
for key, value in sorted.items():
    if not value['title'] == '':
        exclude_list[key] = value

game_list = {}
for key, value in exclude_list.items():
    exists = os.path.isfile(os.path.join(game_path, value['file']))
    if exists:
        game_list[key] = value

# actual bot starts here
client = Bot(description="IFBot", command_prefix=commands.when_mentioned_or(prefix), pm_help = False)

client.remove_command('help')

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    return await client.change_presence(game=discord.Game(name=default_status))

# basic functions
def read_stdout(stdout, q):
    it = iter(lambda: stdout.read(1), b'')
    for c in it:
        q.put(c)
        if stdout.closed:
            break

def get_stdout(q, encoding='latin-1'):
    out = []
    while 1:
        try:
            out.append(q.get(timeout=0.2))
        except queue.Empty:
            break
    return b''.join(out).rstrip().decode('latin-1')

def printout(q):

    send_msg = get_stdout(q)

    if send_msg:
        # format messaging to strip out some parser cruft
        # could add more catches if necessary
        send_msg = send_msg.replace("> >", "")

        if format_clean == True:
            send_msg = send_msg.replace("\n>", "")

        if format_code_block:
            send_msg = "```" + send_msg + "```"

        print('[FROM GAME]:\n\n%s' % send_msg)

        return send_msg

# basic routines
def start_game(game_index):

    game_data = game_list[game_index]
    game_file = game_data["file"]
    interpreter = game_data["interpreter"]
    if game_data["args"] != "None":
        arguments = game_data["args"].split(" ")

    print('\n[Status] ' + start_msg)

    curr_terp = terp_path + interpreter
    curr_game = game_path + game_file

    if game_data["args"] != "None":
        ARGS = [curr_terp, arguments[0], arguments[1], curr_game]
    else:
        ARGS = [curr_terp, curr_game]

    # okay, actually start things
    global gam
    global q

    gam = subprocess.Popen(ARGS, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    q = queue.Queue()

    outthread = threading.Thread(target=read_stdout, args=(gam.stdout, q))
    outthread.daemon = True
    outthread.start()

    return start_msg + printout(q)

# commands trapped for
@client.command(pass_context=True)
async def details(ctx, *args):

    if not ctx.message.channel.id == ifchannel:
        return

    if len(args) > 0:
        target_game = args[0]
    else:
        target_game = "none specified"

    if target_game in game_list.keys():
        result = game_list[target_game]
        key = target_game
        title = '**%s** [%s] \n' % (result['title'], key)
        author = '_%s_\n' % result['author']
        genre = '%s\n' % result['genre']
        final = '%s %s %s "%s"' % (title, author, genre, result["blurb"])
    else:
        final = "I'm sorry, which game was that again? Use _@ifbot list_ or _!list_to list all available games."

    await client.say(final)
    await asyncio.sleep(1)

@client.command(pass_context=True)
async def help(ctx, *args):

    if not ctx.message.channel.id == ifchannel:
        return

    result = "To start a game, type in _@ifbot launch <game id>_ or _!launch <game id>_. To see a list of games and id codes, type _@ifbot list_ or _!list_. To see details about a game, type _@ifbot details <id code>_ or _!details <id code>_\n\nAny messages in this channel that don't start with !, [, or * will be processed as input to the game; \"look\" or \"examine\" are good places to start. Most games also have a \"help\" command.\n\nPlease note that games are referred to by a short code, not by full name.\n"

    await client.say(result)
    await asyncio.sleep(1)

@client.command(pass_context=True)
async def launch(ctx, *args):

    if not ctx.message.channel.id == ifchannel:
        return

    global gam
    global q
    global game_active

    try:
        poll = gam.poll()
        if poll == None:
            game_active = True
        else:
            game_active = False
    except:
        game_active = False

    if not game_active:
        target_game = args[0]
        if target_game in game_list.keys():
            result = start_game(target_game)
            title = game_list[target_game]['title']
            await client.change_presence(game=discord.Game(name=title))
        else:
            result = "I'm sorry, which game was that again? Use _@ifbot list_ or _!list_ to list all available games."
    else:
        result = "A game is currently in progress. Please use _quit_ to exit first."

    # now chunk if it is too long
    for chunk in [result[i:i+2000] for i in range(0, len(result), 2000)]:
        await client.say(chunk)
        await asyncio.sleep(1)

@client.command(pass_context=True)
async def list(ctx, *args):

    if not ctx.message.channel.id == ifchannel:
        return

    answer = ""
    for key in game_list:
        curr = game_list[key]
        short =  "%s..." % curr['blurb'][:98]
        adln = "**%s** [%s] (%s) %s \n" % (curr['title'], key, curr['genre'], short)
        answer = answer + adln

    await client.say(answer)
    await asyncio.sleep(1)

@client.event
async def on_message(message):

    global gam
    global q
    global game_active

    try:
        poll = gam.poll()
        if poll == None:
            game_active = True
        else:
            game_active = False
    except:
        game_active = False

    if not game_active:
        result = "No game is running. Try _@ifbot help_ or _!help_."

    if message.author.bot == False and message.channel.id == ifchannel and game_active:

        command = message.content[:]

        if command.startswith((prefix, '*', '[')) or "@ifbot" in command:
            # this is not a command to the game
            result = ""
            await client.process_commands(message)

        else:

            command = (command + '\n').encode('latin-1')
            gam.stdin.write(command)

            result = printout(q)

        if result == None:
            result = end_msg
            print(end_msg)
            await client.change_presence(game=discord.Game(name=default_status))

        # now chunk if it is too long
        for chunk in [result[i:i+2000] for i in range(0, len(result), 2000)]:
            await client.send_message(message.channel, chunk)
            await asyncio.sleep(1)

    else:
        await client.process_commands(message)

#@client.event
#async def on_command_error(error, ctx):

#    print(error, ctx)

    # default response if no other queries are caught
#    answer = "Something has gone wrong or is not working properly. Please ask me for help with _@ifbot help_ or _!help_ or mention a mod."

#    if ctx.message.channel.id == ifchannel:
#        await client.send_message(ctx.message.channel, answer)
    #await client.send_message(client.get_channel(channel), answer)

client.run(token)
