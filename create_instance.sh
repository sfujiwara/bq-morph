#!/usr/bin/env bash

# DATE="20160721"
# DATE="20160726"
# DATE="20160731"
# DATE="20160804"
DATE="20160810"

PROJECT="bigdata-topgate"
INSTANCE_NAME="tmp${DATE}"
TWEET_FILE="t${DATE}.json"
TABLE_NAME="morph_${DATE}"

gsutil cp create_dic.py gs://${PROJECT}.appspot.com/tmp/
gsutil cp morph.py gs://${PROJECT}.appspot.com/tmp/
gsutil cp schema.json gs://${PROJECT}.appspot.com/tmp/

# Create Compute Engine instance
gcloud compute --project ${PROJECT} instances create ${INSTANCE_NAME} \
  --zone "asia-east1-b" \
  --machine-type "n1-standard-1" \
  --network "default" \
  --maintenance-policy "MIGRATE" \
  --scopes default="https://www.googleapis.com/auth/cloud-platform" \
  --tags "http-server","https-server" \
  --image "/ubuntu-os-cloud/ubuntu-1604-xenial-v20160516a" \
  --boot-disk-size "200" \
  --boot-disk-type "pd-standard" \
  --boot-disk-device-name ${INSTANCE_NAME} \
  --metadata-from-file startup-script=startup.sh \
  --metadata "tweet-file=${TWEET_FILE},table-name=${TABLE_NAME}"
