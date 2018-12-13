# discordifpy

#### What It Is

This is a python script that interfaces between Discord and an interactive fiction interpreter. This allows you to play parser-based interactive fiction games in a Discord channel with friends.

It requires Python and an internet connection; I run it off my computer on demand. Setting it up as an actual remote bot should be doable if you know what you're doing there.

Please remember that this is not thoroughly tested. Some games will work better than others, especially those that have fancy maps and do parser tricks. Not all games will work or be playable even if they do work.

**IMPORTANT Use this script at your own risk. I strongly advise using a VM. And not leaving the bot running 24/7 if you're not comfortable with whatever shenanigans your users might get up to.**

It is built off of [slackifpy](https://github.com/exposit/slackifpy).

#### IF You Know What You Are Doing

Download the repo. I suggest using a VM running linux as host. Install discord.py for python. Download the games you want to play. Get the source for and compile the appropriate interpreter(s) with glk. Update gamedb.py with game info. Make a discord bot. Change the configuration options in the main script as the comments direct, using your channel id and your bot token. The bot wil report in once it is active; use "@ifbot help" in Discord to get a list of commands.

#### Step By Step

This is not a hard or complicated process, but it requires multiple steps and there's potential for confusion at nearly every one of them. Treat each step as a separate task that might require extensive googling. Don't be afraid to google for tutorials or error messages at each step.

0. (optional but recommended) Consider using the instructions for [slackifpy](https://github.com/exposit/slackifpy) as a guide. I haven't tested this with a VM but it should work fine.

1. Download and extract the discordifpy zip. NOTE: The folder structure is pretty arbitrary and easily changed, but I suggest leaving it for now and changing it if you intend to after you've got a sample game up and running.

2. Verify that you have Python. You need Python 3. Install discord.py on the system where you will be running discordif.py. You may need to install pip.

    [https://github.com/Rapptz/discord.py](https://github.com/Rapptz/discord.py)

3. This is the hardest step to explain because there are many variables. You need to download and compile interpreters for each type of IF game you want to run. This requires working with source and the command line.

  ### You don't need all the interpreters, just the ones that handle the games you want to run. This will most likely be [FROTZ](https://github.com/DavidGriffith/frotz).

  **IMPORTANT**: You need to compile from the operating system you will ultimately use to run discordifpy. If any of these steps fail at any point, you're probably missing dependencies. Read the error message and google it.

  Every interpreter has notes and install instructions -- the steps I list here worked for me but there are a lot of variables.

  - **FROTZ:** You ultimately want to compile "dfrotz", which outputs text to the terminal instead of to a fancy window. First, grab the zip from github. Unpack the zip. Anywhere is fine, but the Downloads folder works. READ THE README. Open a terminal in the frotz-master directory you just unpacked. Type "make dumb" and wait for it to finish. You should now have a file named "dfrotz" that wasn't there before. Copy it to the "terps" subfolder.

      https://github.com/DavidGriffith/frotz

  - **GLULXE:** Compile glulxe with cheapglk; this is the default so it's easy. READ THE README. Download both zips and extract. Rename cheapglk-master to cheapglk. Open cheapglk in the terminal and type "./make", then repeat for the glulxe folder.

    https://github.com/erkyrath/glulxe
    https://github.com/erkyrath/cheapglk

  - **FROBTADS:** This one can be tricky because of dependencies. Download the zip and extract. READ THE README. Go to the FrobTads directory and open a terminal. At the terminal, type "./bootstrap", then "./configure", and finally "make". Be prepared for it to take awhile.

    https://github.com/realnc/frobtads

4. Download a game that's playable by at least one of the interpreters you've compiled. The sample gamedb assumes you've got [9:05 by Adam Cadre](http://ifdb.tads.org/viewgame?id=qzftg3j8nh5f34i2) from the [ifdb.tads.org](ifdb). Unzip it, and drop the 905.z5 file into the "games" subfolder.

5. Open gamedb.py in a text editor. It's already set up for 9:05 and dfrotz. But you can add more games if you'd like. Sample frobTADs and Glulxe game definitions are included for reference. Case matters. The uniqueid can be any string without spaces but should be short and memorable.

  **NOTE:** If you are using frobTads, be sure to put "-i plain" in place of "None" in the arguments field for each TADs game in gamedb.py.

6. Open discordif.py. Change the paths variables to reflect your own path if necessary. Change any other variables.

7. Set up your Discord to work with discordif.py and discordif.py to work with your Discord.

    - Make a dedicated channel for your ifbot to operate in. Ours is called "xintfiction" so it ends up at the bottom of the channel list.

    - Follow the instructions [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to get a token.

    - Paste the token into discordif.py in the "token" variable. This token needs to be kept secret. You can alternatively copy that "token = ''" line into a separate file and uncomment the import.

  **NOTE** Once you put your token in, don't share this file anywhere. It will allow malicious people to possibly do malicious things. If you think your token is compromised, reset the bot token on the discord website.

8. Run discordif.py. Navigate to the directory you unzipped discordif.py and run "python discordif.py". The bot should report in. In Discord, type in "@ifbot list". You should see a list of all games you've listed in gamedb. Use "@ifbot help" to get help.

9. If everything works as expected, you're good to go. If the script chokes, read the error messages and address them. If you get a "file not found" issue on launch, check your path variables -- they may need to be more explicit or set for your system.

Good luck!
