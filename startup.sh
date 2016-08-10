#!/usr/bin/env bash
apt-get update
apt-get -y install curl
apt-get -y install mecab mecab-ipadic-utf8 python-mecab libmecab-dev
apt-get -y install python-pip
apt-get -y install python-pandas
apt-get -y install python-requests
PROJECT=`curl "http://metadata.google.internal/computeMetadata/v1/project/project-id" -H "Metadata-Flavor: Google"`
gsutil cp gs://${PROJECT}.appspot.com/tmp/create_dic.py /tmp/
cd /tmp
python create_dic.py
TWEET_FILE=`curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/tweet-file" -H "Metadata-Flavor: Google"`
gsutil cp gs://${PROJECT}.appspot.com/tmp/morph.py /tmp/
gsutil cp gs://${PROJECT}.appspot.com/tmp/schema.json /tmp/
gsutil cp gs://cp300demo1.appspot.com/twitter/${TWEET_FILE} /tmp/
python morph.py
gsutil cp /tmp/morph_${TWEET_FILE} gs://${PROJECT}.appspot.com/twitter/
TABLE_NAME=`curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/table-name" -H "Metadata-Flavor: Google"`
bq load \
  --source_format=NEWLINE_DELIMITED_JSON  \
  --schema=/tmp/schema.json \
  --max_bad_records=1000 \
  --replace=true ${PROJECT}:twitter.${TABLE_NAME} gs://${PROJECT}.appspot.com/twitter/morph_${TWEET_FILE}
