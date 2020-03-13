#!/bin/bash

ID="E"
service_name="motionpub.service"
MQ_HOST="18.141.11.6"
topic_name="mr/motion/heartbeat"

if (systemctl -q is-active $service_name )
then
	echo "Up"
	exit
else
	echo "Down"
	sudo systemctl start $service_name
	sleep 3
	if (systemctl -q is-failed $service_name )
	then
		mosquitto_pub -h $MQ_HOST -t $topic_name -u iotcollabhuat --pw iott1t5 -m "[Unable to restart motion service in mr, ${ID}]"
		echo "Message sent"
	else
        mosquitto_pub -h $MQ_HOST -t $topic_name -u iotcollabhuat --pw iott1t5 -m "[Motion service restarted in mr, ${ID}]"
		echo "Restart successful"
	fi
fi
