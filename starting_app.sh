#!/bin/bash

aws deploy push --application-name ApiFlat --s3-location s3://app-projet-coloc/ApiFlat.zip
aws deploy create-deployment --application-name ApiFlat --deployment-config-name CodeDeployDefault.OneAtATime --deployment-group-name ApiFlat_DepGroup --s3-location bucket=app-projet-coloc,bundleType=zip,key=ApiFlat.zip
