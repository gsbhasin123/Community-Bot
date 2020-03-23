module.exports = 
  name: 'restart'
  description: 'Restarts the bot'
  required_roles: ["690279920080781495"]
  required_perms: []
  execute: (msg, args) ->
    message.channel.send "Restarting bot..."
    process.exit()