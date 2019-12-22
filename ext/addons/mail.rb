require 'discordrb'
require 'fileutils'
require 'dotenv'
Dotenv.load
spool = ARGV[0].to_s
token = ENV['TOKEN']
bot = Discordrb::Commands::CommandBot.new token: token, prefix: '/' # Make a bot constructor with the right settings
bot.command :inbox do |event|
  if File.exists? File.join(spool, event.author.id.to_s)
     files = Dir.entries(File.join(spool, event.author.id.to_s))
     files = files - %w[. ..]
     event.send_embed do |embed|
         embed.title = "Your inbox. Emails: "
         embed.description = files.join("\n")
         embed.color = "d98209"
     end
  else
      FileUtils.mkdir_p(File.join(spool, event.author.id.to_s))
      event.send_embed do |embed|
         embed.title = "I set up your brand-new mail account! Have fun!"
         embed.color = "d98209"
      end
  end
end

bot.command :viewmail do |event, mailname|
   if File.exists? File.join(spool, event.author.id.to_s, mailname)
      event.send_embed do |embed|
         embed.title = mailname + ":"
         embed.color = "d98209"
         embed.description = File.read(File.join(spool, event.author.id.to_s, mailname))
      end
   else
		event.send_embed do |embed|
         embed.title = "Either that email doesn't exist, was deleted, or does not belong to you. Check the spelling and try again!"
         embed.color = "db271a"
      end
   end
end

bot.command :rmmail do |event, mailname|
   if File.exists? File.join(spool, event.author.id.to_s, mailname)
       File.delete(File.join(spool, event.author.id.to_s, mailname))
       nil
   else
		event.send_embed do |embed|
         embed.title = "That email does not exist. It might not be yours. Check the spelling and try again, please."
         embed.color = "db271a"
      end
   end
end

bot.command :writemail do |event, uname, mailname, *content|
   un = uname
   uname = bot.parse_mention(uname)
   content = content.join(' ')
   content = "\n" + content + "\nFROM: " + un + "\n"
   File.write(File.join(spool, uname.id.to_s, mailname), content)
   nil
end

bot.run