# Samurai Discord Bot 

![Discord Bot](https://github.com/ParzivalEugene/Samurai/blob/master/main/images/chat_bot.svg)
  
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ParzivalEugene/Samurai) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ParzivalEugene/Samurai)  
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/ParzivalEugene/Samurai) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/ParzivalEugene/Samurai/master)  
  
## Table of Contents  
  
* [Description](#description)  
* [Commands](#commands)
* [Glossary](#glossary)
* [Music module](#music-module)  
* [Leveling module](#leveling-module)  
* [Birthdays module](#birthdays-module)  
* [Tic Tac Toe](#tic-tac-toe)  
* [Connect Four](#connect-four)  
* [Translator](#translator)  
* [Useful modules](#useful-modules)   
* [License](#license)  
  
## Description  
  
An incredible discord bot named Samurai. It is simply irreplaceable on any server. A samurai can create a level system, moderate participants, wish them a happy birthday. Also, a samurai can play  simple games (tic-tac-toe and connect four) with different tactics. It can play songs from YouTube, create queues and playlists. Reacts amazingly accurately to appeals to him and will always keep up  the conversation. Recommended for installation on each server.  
  
## Commands  
  
Samurai is very clever bot that tries its best to be alive.  Use all commands with **.** prefix. Example: **.help**.
  
> **help** - Main command, will display a description of the bot with commands and rules for their use.  

### Glossary
>Samurai module responsible for translation and vibe.
Allows you to choose vibe and language in which the samurai will speak.

| command | description |  
| --- | --- |
| **gl_help** | Displays help for glossary |
| **gl** | Displays current server setup |
| **gl_lang \<lang>** | Sets up the bot language. **Use abbreviations** |
| **gl_vibe \<vibe>** | Sets up the bot vibe |
  
### Music module  
> Samurai module responsible for music.  
Allows you to create playlists, listen, pause videos from [youtube](https://www.youtube.com/).  
Great for hanging out with friends or helping you tune in to the right wave.  
  
| command | description |  
| --- | --- |  
| **player_help** | Displays help for music module-related commands |  
| **join** | Connects bot to your voice channel |  
| **leave** | Disconnects the bot from your voice channel and clears the queue |  
| **play \<url** or **keywords>** | Loads your input and adds it to the queue. If there is no playing track, then it will start playing  |
| **pause** | Pauses playback |
| **resume** | Resumes playback |
| **restart** | Plays song again |
| **stop** | Stops the currently playing track and clear the queue |
| **skip** | Skips to the next song |
| **skipto \<index>** | Skips to the current song |
| **previous** | Returns to the previous song |
| **volume \<value>** | Sets the player volume |
| **volume up** | Increases volume by 10% |
| **volume down** | Lowers volume by 10% |
| **lyrics** | Displays song lyrics |
| **queue** | Displays the current song queue |
| **shuffle** | Randomizes the current order of tracks in the queue |
| **loop (loop all)** | Starts looping your current queue |
| **loop 1** | Starts looping your currently playing track |
| **loop none** | Stops looping |
| **eq [flat, metal, boost, piano]** | Adjusts equalizer to current preset |
| **adveq \<band> \<gain>** | Adjusts current band to current gain |
| **np** | Displays currently playing song and additional information |
| **seek <time>** | Skips to the specified timestamp in the currently playing track |
  
  
### Leveling module  
> Samurai module responsible for the level system on the server. Allows you to create a competitive environment and a pumping system in your company.  
  
| command | description |  
| --- | --- |  
| **level_help** | Displays help for leveling-related commands |  
| **level_add \<role> \<xp>** | Creates level with ***role*** and ***xp*** to get it |  
| **level_update \<role> \<xp>** | Updates the ***role*** level to ***xp*** |  
| **level_delete** | Removes the role from the database |  
| **level_show** | Lists all levels of the server and the amount of experience to get them |  
| **level** | Displays an embed about your level |  
| **level_dashboard** | Displays the top members of the server |  
  
### Birthdays module  
> Samurai module responsible for birthdays.  
Creates a database of birthdays of participants, where everyone can enter their data. The bot will congratulate the participant on this wonderful day.  
  
| command | description |  
| --- | --- |  
| **bd_help** | Displays help for birthday commands |  
| **bd_set_chat \<chat>** | Specifying the congratulations chat |  
| **bd_up_chat \<chat>** | Updates congratulations chat |  
| **bd_del_chat** | Deletes congratulations chat, **you will not receive Samurai congratulations** |  
| **bd_show_chat** | Displays congratulations chat |  
| **bd_add \<year> \<month> \<day>** | Initializes a new member to the database with the specified date |  
| **bd_update \<year> \<month> \<day>** | Updates the date of birth |  
| **bd_delete** | Removes the date of birth |  
| **bd** | Displays embed about you |  
| **bd_show** | Lists all provisioned users with birthday dates |  
  
  
### Tic Tac Toe  

---
Does not work in current release
---

> Samurai module responsible for tic-tac-toe.  
Allows participants to play tic-tac-toe. Participants can compete with each other or challenge their forces against a samurai, with an adaptive level of difficulty of the game and different types of strategies.  
It can help resolve disputes or train the brain.  
  
| command | description |  
| --- | --- |  
| **xo_help** | Displays help for tic-tac-toe commands |  
| **xo_rules** | Displays the rules of tic-tac-toe. |  
| **xo \<member1> \<member2>** | Initializes a new game for ***member1*** and ***member2*** |  
| **xo \<member1> \<Samurai> \<game type>** | Initializes a new game for ***member1*** and ***Samurai*** with bot strategy ***game type*** (game types: "*ai*", "*random*", **default game type** = "*ai*"). |  
| **xo_place \<number>** | Places the required chip in the cage at ***number***. |  
| **xo_lose** | The current player will surrender. |  
  
### Connect Four  

---
Does not work in current release
---

> Samurai module, responsible for "connect four".  
Allows participants to play connect four.  
Will help you kill time while waiting for a friend or lobby, compete with your friends and find the **true champion**.  
  
| command | description |  
| --- | --- |  
| **c4_help** | Displays help for commands related to connect four. |  
| **c4_rules** | Displays the rules of the game in connect four. |  
| **c4 \<member1> \<member2>** | Initializes a new game for ***member1*** and ***member2***. |  
| **c4_place \<number>** | Throw in the column ***number*** the desired chip. |  
| **c4_lose** | The current player will surrender. |  
  
### Translator  
> Samurai module responsible for foreign languages.  
Always at hand, something needs to be translated - Samurai is right there, you don't know what language the message is written in - Samurai will always help. When bored, you can try to guess the language of the message. In general, a miracle, not a module!  
  
| command | description |  
| --- | --- |  
| **tr_help** | Displays help for commands related to the translator module |  
| **tr_list** | Displays a list of language abbreviations |  
| **tr_trans \<source lang> \<target lang> \<message>** | Translates ***message*** from ***source lang*** to ***target lang*** |  
| **tr_trans \<target lang> \<message>** | Determines the language of the original message and translates ***message*** into ***target lang*** |  
| **tr_detect_lang \<message>** | Displays language ***message*** |  
| **tr_game** | Starts the game ***"guess the language"*** |  
  
### Useful modules  
> Modules that I haven't been able to categorize, but they're still just as cool.  
Weather forecast around the world, inspiration for the coming day, stories about your future and decision of fate with a coin toss. Yes, everything is in this module.  
  
| command | description |  
| --- | --- |
| **mini_help** | Displays help for mini modules |
| **toss** | Tosses a coin. |  
| **8ball \<message>** | Ask the magic ball a question and it will tell you the fate. |  
| **forecast \<place>** | Returns the weather forecast at the selected location. |  
| **inspire** | Inspires you to great achievements. |  
  
## License  
  
[![GitHub](https://img.shields.io/github/license/ParzivalEugene/Samurai)](https://github.com/ParzivalEugene/Samurai/blob/master/LICENSE.md)  

