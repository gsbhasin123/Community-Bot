

<img src="https://cdn.discordapp.com/attachments/650009449951395841/690621644712181830/Untitled45_20200320180253.png" alt="drawing" width="200"/>

# Community Bot
A discord bot that anyone can modify and commit to! I want it to be as open-source as possible, so feel free to work on any feature you like!

## Features
You can invite the bot to your server by clicking [here](https://discordapp.com/oauth2/authorize?client_id=610225885093691467&scope=bot&permissions=8).
You can check out the bot by joining [this Discord Server](https://discord.gg/MAraSwm) too!

## Committing
### Languages
You can commit in CoffeeScript and JavaScript.

### Template for commands
This is the command structure for JavaScript
```javascript
module.exports = {
  name: 'command_name',
  description: 'Does blah.',
  required_roles: [],
  required_perms: [],
  execute(msg, args) {
    // some code, args is an array of arguments and msg is the actual message object
  }
};
```
And this is the command structure for CoffeeScript
```coffeescript
module.exports = 
  name: 'command_name'
  description: 'Does blah.'
  required_roles: []
  required_perms: []
  execute: (msg, args) -> 
     # some code, args is an array of arguments and msg is the actual message object
 ```

## Note


Contributors, please put your name by the feature you have added, it would be easier to contact the creator for a certain command if it breaks ToS or something, Also make sure you join the community discord so you can help people.

## Acknowledgements
**Ubuntu#5055**: - The actual host for the bot

**codic#3754**: - Just a good guy all around

**Me, Proxy#0294**: - For actually wanting to do something productive.
