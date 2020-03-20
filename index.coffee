fs = require 'fs'
Discord = require 'discord.js'
require('dotenv').config()
path=require 'path'

client = new Discord.Client()
client.commands = new Discord.Collection()

for file in fs.readdirSync(path.join('.', 'cogs', 'djs')) 
  if file.endsWith('.coffee') or file.endsWith('.js')
    cmd = require "./cmds/#{file}" 
    client.commands.set(cmd.name, cmd)

client.on 'message', (message) ->
  return unless message.content.startsWith(process.env.PREFIX) or not message.author.bot # if a bot runs the command or if the command doesnt start with a prefix ignore it
  args = message.content.slice(process.env.PREFIX.length).split(" ")
  command = args.shift().toLowerCase()
  return unless client.commands.has(command)
  try
    client.commands.get(command).execute(message, args)
  catch err
    console.log "bot errored out with #{err}"

client.login process.env.TOKEN
 
