# Samurai Discord Bot

## Description
An incredible discord bot named Samurai. It is simply irreplaceable on any server. A samurai can create a level system, moderate participants, wish them a happy birthday. Also, a samurai can play simple games (tic-tac-toe and connect four) with different tactics. It can play songs from YouTube, create queues and playlists. Reacts amazingly accurately to appeals to him and will always keep up the conversation. Recommended for installation on each server.

## Commands
Samurai is very clever bot that tries its best to be alive.

> **help** - Main command, will display a description of the bot with commands and rules for their use.

### Music module
> Samurai module responsible for music.
Allows you to create playlists, listen, pause videos from [youtube](https://www.youtube.com/).
Great for hanging out with friends or helping you tune in to the right wave.

| command | description |
| --- | --- |
| **player_help** | Displays help for music module-related commands. |
| **join** | The bot will enter the current voice channel of the author of the message. |
| **leave** | The bot will leave the voice channel. |
| **queue** | Displays the queue of tracks. |
| **queue \<url>** | Add ***url*** to the queue. |
| **remove \<number>** | Delete track at number ***number***. |
| **play** | Will start playing music. |
| **pause** | Will stop playing music. |
| **resume** | Will resume playing music. |
| **stop** | Remove the track from the queue and stop playing music. |


### Leveling module
> Samurai module responsible for the level system on the server. 
Allows you to create a competitive environment and a pumping system in your company.

| command | description |
| --- | --- |
| **level_help** | Displays help for leveling-related commands. |
| **level_add \<role> \<xp>** | Will create a level with ***role*** and ***xp*** to get it. |
| **level_update \<role> \<xp>** | Updates the ***role*** level to ***xp***. |
| **level_delete** | Will remove the role from the database. |
| **level_show** | Lists all levels of the server and the amount of experience to get them. |
| **level** | Displays an embed about your level. |
| **level_dashboard** | Will display the top members of the server. |

### Birthdays module
> Samurai module responsible for birthdays.
Creates a database of birthdays of participants, where everyone can enter their data. The bot will congratulate the participant on this wonderful day.

| command | description |
| --- | --- |
| **bd_help** | Displays help for birthday commands. |
| **bd_set_chat \<chat>** | Specifying the chat where congratulations will be sent. |
| **bd_up_chat \<chat>** | Chat update for congratulations. |
| **bd_del_chat** | Delete chat for congratulations, **you will not receive Samurai congratulations**. |
| **bd_show_chat** | Conclusion of the chat, where congratulations will go. |
| **bd_add \<year> \<month> \<day>** | Initializes a new member to the database with the specified date. |
| **bd_update \<year> \<month> \<day>** | Will update the date of birth. |
| **bd_delete** | Will remove the date of birth. |
| **bd** | Will display embed about you. |
| **bd_show** | Lists all provisioned users with birthday dates. |


### Tic Tac Toe
> Samurai module responsible for tic-tac-toe.
Allows participants to play tic-tac-toe. Participants can compete with each other or challenge their forces against a samurai, with an adaptive level of difficulty of the game and different types of strategies.
It can help resolve disputes or train the brain.

| command | description |
| --- | --- |
| **xo_help** | Displays help for tic-tac-toe commands. |
| **xo_rules** | Displays the rules of tic-tac-toe. |
| **xo \<member1> \<member2>** | Initializes a new game for ***member1*** and ***member2***. |
| **xo \<member1> \<Samurai> \<game type>** | Initializes a new game for ***member1*** and ***Samurai*** with bot strategy ***game type*** (game types: "*ai*", "*random*", **default game type** = "*ai*"). |
| **xo_place \<number>** | Places the required chip in the cage at ***number***. |
| **xo_lose** | The current player will surrender. |

### Connect Four
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
| **tr_help** | Displays help for commands related to the translator module. |
| **tr_list** | Displays a list of language abbreviations. |
| **tr_trans \<source lang> \<target lang> \<message>** | Translate ***message*** from ***source lang*** to ***target lang***. |
| **tr_trans \<target lang> \<message>** | Determines the language of the original message and translates ***message*** into ***target lang***. |
| **tr_detect_lang \<message>** | Displays language ***message***. |
| **tr_game** | Start the game ***"guess the language"***. |

### Useful modules
> Modules that I haven't been able to categorize, but they're still just as cool.
Weather forecast around the world, inspiration for the coming day, stories about your future and decision of fate with a coin toss. Yes, everything is in this module.

| command | description |
| --- | --- |
| **toss** | Toss a coin. |
| **8ball \<message>** | Ask the magic ball a question and it will tell you the fate. |
| **forecast \<place>** | Returns the weather forecast at the selected location. |
| **inspire** | Will inspire you to great achievements. |

## History of creation
> First start - Samurai's birthday - **March 24, 2021**

At the age of fifteen, having my own discord server (at that time the server had an audience of <100 people), I began to think about developing my own bot. I knew about other bots, and it amazed me how cool they can be. The wonderful [Groovy](https://groovy.bot/), the handy [Carl](https://carl.gg/) and the irreplaceable [KD](https://top.gg/bot/414925323197612032) were an integral part of my server. But over time, a subscription system came to each of these bots, and we, being schoolchildren, could not give even $5 for groovy.
Having a little programming skills in [python](https://en.wikipedia.org/wiki/Python_ (programming_language)), I wanted to create my first large-scale project in which I could link everything I can. In my vision, this was supposed to be a project where I can fully realize my potential: use a database and [SQL](https://ru.wikipedia.org/wiki/SQL), handle https requests, write beautiful and structured code , use different api and modules. In this regard, WEB applications are the most cost-effective, because they are multifaceted and can carry any function. I became interested in bots and sites, tried to create bots in [telegram](https://tlgrm.ru/), but this did not drag me out at all, I did not see how I could develop my bot on this platform. But one evening, sitting with a friend in discord, I thought how cool it would be if the bot responded to my messages. For example, I write how sad I am, and he will cheer me up. It sounded like a dream, but it became a goal for me. After digging in [Discord Api](https://discordpy.readthedocs.io/en/latest/api.html) for a week and looking at a bunch of tutorials, I wrote the simplest version of the bot. He reacted to a couple of messages with just one phrase and could send stickers. But after spending a month coding, my bot has learned a lot, as you can see from the function chapter. For me, this is only the first step, and I plan to further develop the bot.

> It was written on April 22nd, 2021.

## Author
The author of this kid is me - [Parzival](https://github.com/ParzivalEugene), 15-year-old man from Moscow. I am fond of programming in the [python](https://en.wikipedia.org/wiki/Python_ (programming_language)), I can create a desktop application on [PyQT](https://en.wikipedia.org/wiki/PyQt), write a game on [pygame](https://en.wikipedia.org/wiki/Pygame), I know the basics of [html](https://en.wikipedia.org/wiki/HTML) and [css](https://en.wikipedia.org/wiki/CSS), in short, the most basic knowledge of a pythonist. My [discord server](https://discord.gg/WuTaFrker6).

## License
At the moment, I'm not really looking at how my code can be used, but so far it is open to everyone for non-commercial use.