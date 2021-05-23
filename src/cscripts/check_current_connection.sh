#!/bin/sh

sudo netstat -enp | grep ":3001" | awk {'print $5'} | cut -d ':' -f 1 | sort | uniq -c | sort
