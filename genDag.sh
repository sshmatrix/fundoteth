#!/bin/bash
#pyinstaller --onefile --windowed test.py
source .env
HERE=/work/$USER/midjourney
DAG=${HERE}"/dag.dag"
cp ${HERE}"/htc.sub" ${HERE}"/sub.sub"
sed -i "s/user/$USER/g" ${HERE}"/sub.sub"
sed -i "s/tag/$TAG/g" ${HERE}"/sub.sub"
set -u
rm ${HERE}/*dag.* > /dev/null 2>&1
rm ${HERE}/*.flag > /dev/null 2>&1
for ID in $(seq 0 5000); do
  mkdir -p logs/${ID}/
  echo "JOB A${ID} ${HERE}/sub.sub"
  echo "VARS A${ID} ID=\"${ID}\""
  echo "RETRY A${ID} 0"
done > ${DAG}
head -n 6 ${DAG}
tail -n 6 ${DAG}
#condor_submit_dag -maxidle 500 sub.sub
