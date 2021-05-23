#!/bin/sh

netstat -tupn | cut -c45-59,85- | grep cardano-nod
