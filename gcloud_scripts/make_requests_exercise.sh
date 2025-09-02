#!/bin/bash

ADDR=$(kubectl get gateway log-output-gateway -n exercises -o jsonpath='{.status.addresses[*].value}')

echo -e "##### ##### request to /pingpong/ ##### #####\n"
curl "http://$ADDR/pingpong"
echo -e "\n##### ##### request to /pingpong/pings ##### #####\n"
curl "http://$ADDR/pingpong/pings"
echo -e "\n##### ##### request to /pingpong/pong ##### #####\n"
curl "http://$ADDR/pingpong/pong"

echo -e "\n##### ##### request to /logs/ ##### #####\n"
curl "http://$ADDR/logs"
echo -e "\n##### ##### request to /logs/all ##### #####\n"
curl "http://$ADDR/logs/all"
echo -e "\n##### ##### request to /logs/ping ##### #####\n"
curl "http://$ADDR/logs/ping"