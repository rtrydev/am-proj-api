pgcontainer=$(cat .containtername)

kill $(cat .flaskpid);
docker stop $pgcontainer && docker rm $pgcontainer;
