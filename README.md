# CrocomireBot

This is a Discord bot written in Python for the Ridleycord server. It holds Smash Ultimate matchup notes,
keeps track of the server's boosters, posts memes, and lets admins add their own commands without touching
the code. The data is stored in SQLite databases. Every command starts with `?`.

![](https://github.com/is386/crocomire-bot/blob/master/demo.png?raw=true)

## Features

### Custom Commands

`?addcmd <name> <text>` creates a text command, and `?addcmd embed <name> <fields>` creates an embed
command. Running `?addcmd` on a command that already exists will update it, and `?removecmd <name>` will
delete it. Custom commands are checked before the built in ones, so they work the same way. Both of these
commands are admin only.

### Matchups

`?mu` lists every character that has matchup data. `?mu <character>` sends an embed with the notes for that
character: an overview, critical tips, counterpicks, stage bans, an image, and a link to the full doc.
Character names are run through a synonyms database, so nicknames and abbreviations work too. Admins can use
`?addmu` to add or update a character's data, and `?removemu <character>` to delete it.

### Boosts

`?boosters` sends a top 10 leaderboard of the users who have been boosting the server the longest. There is
also a background task that updates a leaderboard message in the booster channel every hour. `?boost` gives
boosters a shoutout, and everyone else gets dabbed on.

### Roles

`?alts` ranks Ridley's alt roles by how many users have each one. `?removerole <role>` takes a role away
from every user who has it. It asks for a confirmation reaction first, and it only works on the JMU role.
This command is admin only.

### Fun

`?meme` and `?tubes` send a random image from their respective lists. `?addmeme <url>` adds a new meme, but
only if the url actually points to an image. `?fact` grabs a random useless fact from an API. `?mash` sends
a bunch of random letters, and `?power` rolls some joke stats for you.

### Help

`?info` sends a list of every command, grouped by category. `?info <command>` sends the description, usage,
and examples for that command.

Note: The server id, booster channel id, and leaderboard message id are hardcoded in `crocomire/cogs/boost.py`,
so you will need to change those if you want to run this on another server.

## Setup

This bot requires a file named `secret.py` in the root folder with the following content:

```
token = "PASTE_YOUR_BOT_TOKEN_HERE"
```

## Dependencies

- `python 3.8`

### Python Dependencies

- `discord.py`
- `requests`

To use the `requirements.txt` file, just run `pip3 install -r requirements.txt`.

## Build

`docker build -t crocbot .`

## Run

`docker run --rm -d crocbot`
