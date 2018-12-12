#!/bin/bash
current=""
while true; do
	latest=`ec2-metadata --public-ipv4`
	echo "public-ipv4=$latest"
	if [ "$current" == "$latest" ]
	then
		echo "ip not changed"
	else
		echo "ip has changed - updating"
		current=$latest
		echo url="https://www.duckdns.org/update?domains=computacionenred&token=895a08f6-29cc-48fe-84ae-2c73d159e272&ip=" | curl -k -o ~/duckdns/duck.log -K -
	fi
	sleep 5m
done
