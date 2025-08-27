#!/bin/bash

ADDR=$(kubectl get ing ping-log-shared-ingress -n exercises -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo -e "request to /pingpong : \n"
curl "http://$ADDR/pingpong"
echo -e "request to /logs/all : \n"
curl "http://$ADDR/logs/all"
echo -e "request to /logs/ping : \n"
curl "http://$ADDR/logs/ping"