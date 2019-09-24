#!/bin/bash

curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
./awscli-bundle/install -b ~/bin/aws
export PATH=~/bin:$PATH
aws configure set aws_access_key_id AKIAQLXGGKZWCNPWYCOA
aws configure set aws_secret_access_key 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
aws configure set default.region eu-west-3
aws configure set default.output text

aws deploy push --application-name ApiFlat --s3-location s3://app-projet-coloc/ApiFlat.zip
aws deploy create-deployment --application-name ApiFlat --deployment-config-name CodeDeployDefault.OneAtATime --deployment-group-name ApiFlat_DepGroup --s3-location bucket=app-projet-coloc,bundleType=zip,key=ApiFlat.zip
