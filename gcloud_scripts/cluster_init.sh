#!/bin/bash

# `gcloud auth login` and then setup project first
# IT'S NOT `gcloud config set project <projectname>-<projectid>`
# THIS IS CORRECT `gcloud config set project <projectid>`
gcloud services enable container.googleapis.com

# This sets kubeconfig automatically
gcloud container clusters create dwk-cluster \
 --zone=europe-north1-b \
 --cluster-version=1.32 \
 --disk-size=32 \
 --num-nodes=3 \
 --machine-type=e2-micro \
 --no-enable-managed-prometheus \
 --logging=NONE

# The managed logger takes up all the resources in a e2-micro.
# This works too if the cluster is already running
# `gcloud container clusters update dwk-cluster --disable-managed-prometheus --zone=europe-north1-b --monitoring=NONE`

# Run this if it doesn't set kubeconfig automatically
# gcloud container clusters get-credentials dwk-cluster --zone=europe-north1-b