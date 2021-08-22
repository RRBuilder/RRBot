# RRBot
Source code for the RRBot discord bot project.

Created by RRBuilder#5922



Command usage:
Default prefix is $, you can also tag the bot to be given the set prefix.

Administrative tools:
$setchat {this or all} - "this" restricts the bot to only respond in the chat where this command was ran in. "all" lifts any chat restrictions.
$prefix {prefix} - sets a prefix.

User tools:
$Help - displays the help message
$CMP - displays the last session and 5 most recent games played.
$Pass {length} {1 or 2} - generates a password, messages the user and deletes the message 30 seconds later. 1 for Unicode, 0 for ASCII.



Dependancies:
discord.py
python-dotenv
python-decouple
