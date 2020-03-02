#!/bin/bash
 
# Argument 1: file name (example: music.mp3)
 
#APIKEY="o.UhzqdgL1bswz77nXOk5SGuSqFojZISDt"
#APIKEY="o.RNbyIs5Twa0gmXB4fasUNLYsqW1WIVcZ"
APIKEY="o.n5kMUyS6ewQUU3IOx0DTb3WV2sJFxki5"

FILENAME=$(basename ${1})
FILEDIR=$(dirname ${1})
CUDIR=$(pwd)
FILETYPE=$(file -bi ${1} | cut -d';' -f1)
 
echo File: ${1}, Type: ${FILETYPE}

echo body: ${3}

echo title: ${2}
 
cd ${FILEDIR}
 
echo Getting permission...
 
eval $(curl -s -u ${APIKEY}: https://api.pushbullet.com/v2/upload-request -d \
                             file_name=${FILENAME} -d file_type=${FILETYPE} | python -m json.tool | \
                             sed 's/": /=/g' | tr -d ' ' | sed 's/,$//g' | sed 's/^"//g' | \
                             tr -d '}' | tr -d '{' | sed 's/data=//g' | sed '/^$/d' | \
                             sed 's/^/export /g'  | sed 's/content-type/content_type/g')
 
echo Uploading file ...
 
curl -O --progress-bar -i ${upload_url} \
  -F awsaccesskeyid=${awsaccesskeyid} \
  -F acl=${acl} \
  -F key=${key} \
  -F signature=${signature} \
  -F policy=${policy} \
  -F content-type=${content_type} \
  -F file=@${FILENAME} \
 
echo Sending Notification ...
curl -u ${APIKEY}: https://api.pushbullet.com/v2/pushes -d type=file -d file_name=${FILENAME} -d file_type=${FILETYPE} -d file_url=${file_url}  -d type=note -d title=${2} -d body=${3}
echo
 
cd ${CURDIR}
