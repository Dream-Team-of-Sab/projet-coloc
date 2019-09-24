#!/bin/bash

curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
./awscli-bundle/install -b ~/bin/aws
export PATH=~/bin:$PATH
aws configure set $AWS_ACCESS_KEY_ID
aws configure set $AWS_SECRET_ACCESS_KEY
aws configure set default.region eu-west-3
aws configure set default.output text

aws deploy push --application-name ApiFlat --s3-location s3://app-projet-coloc/ApiFlat.zip
aws deploy create-deployment --application-name ApiFlat --deployment-config-name CodeDeployDefault.OneAtATime --deployment-group-name ApiFlat_DepGroup --s3-location bucket=app-projet-coloc,bundleType=zip,key=ApiFlat.zip
