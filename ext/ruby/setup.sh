export GEM_HOME=/home/runner/.gem
export PATH="$GEM_HOME/bin:$PATH"
gem install discordrb
gem install dotenv
ruby /home/runner/ext/ruby/addons/mail.rb /home/runner/ext/ruby/data/mail/spool
