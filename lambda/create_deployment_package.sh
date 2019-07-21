#!/bin/bash

#gets current directory, concatenates with lambda/ride
#cds there
ORIGINAL_DIR=$(pwd)
cd "$ORIGINAL_DIR/lambda/ride"

###############################
#ride lambda function deployment package
#--target installing the python dependency locally
#to deploy for lambda
#
#-9 = full size encryption
#-j ignore directories between current working directory
# and where the files are stores
#(dont include lambda/ride in the zip)
###############################

pip install --target ./lambda/ride requests
zip -9rj ride.zip lambda/ride/*
mv ride.zip $ORIGINAL_DIR
cd $ORIGINAL_DIR
