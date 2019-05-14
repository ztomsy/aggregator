#!/bin/bash
while
cmd="python $@"
do
	echo "Keep alive $@"
	echo "Press [CTRL+C] to stop.."
	$cmd
	echo "Finished"
	sleep 1

done