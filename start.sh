while :
do
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi
bash -c "exec -a commbot ./node_modules/coffeescript/bin/coffee index.coffee"
pkill -f commbot
git pull
done
