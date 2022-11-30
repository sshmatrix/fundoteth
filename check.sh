#!/bin/bash
set -u
short=0
source .env

while [[ "$short" == "0" ]]; do
 if [ -f test.key ]; then
  echo "match found; terminating jobs"
  condor_rm $USER
  short=1
 fi	
done
