ID=$1
START_T=$(date +%s)
source .env
HERE=/work/$USER/midjourney
${HERE}/dist/test $ID 1000000
touch ${HERE}/${ID}.flag
cp ./test.key ${HERE}/ > /dev/null 2>&1
END_T=$(date +%s)
DIFF_T=$(( $END_T - $START_T ))
echo "Total code time (secs): ${DIFF_T}"

