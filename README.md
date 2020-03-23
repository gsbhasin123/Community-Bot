# About Community bot
A discord bot that anyone can modify and commit to! I want it to be as open-source as possible, so feel free to work on any feature you like!

## Features
You can invite the bot to your server by clicking [here](https://discordapp.com/oauth2/authorize?client_id=610225885093691467&scope=bot&permissions=8).
You can check out the bot by joining [this Discord Server](https://discord.gg/QnUYBwX) too!

## Committing
### Languages
You can commit in CoffeeScript and JavaScript.

### Template for commands
This is the command structure for JavaScript
```javascript
module.exports = {
  name: 'ping',
  description: 'pong',
  required_roles: [],
  required_perms: [],
  execute(msg, args) {
    message.reply("Pong");
  }
};```
And this is the command structure for CoffeeScript
```coffeescript
module.exports = 
  name: 'ping'
  description: 'pong'
  required_roles: []
  required_perms: []
  execute: (msg, args) -> message.reply("Pong")```

## Note
People who want to run an instance of this bot, if you are using a Linux system, you are able to use the 'system' cog

Windows users, please use the `shell`, and make sure you use windows 10, otherwise some commands from the `system` cog might not work

Contributors, please put your name by the feature you have added, It would be easier to contact the creator for a certain command if it breaks ToS or something, Also make sure you join the community discord so you can help people.
https://discord.gg/zGFHQPM

## Acknowledgements
**Ubuntu#5055**: - The actual host for the bot

**codic#3754**: - Just a good guy all around

**Me, Proxy#0294**: - For actually wanting to do something productive.