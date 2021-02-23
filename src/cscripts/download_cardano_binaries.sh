#!/bin/sh

#Prerequisite to running this program to download the cardano binaries is a cloudsmith env file containing:
#ACCOUNT=<value of cloudsmith account>
#REPOSITORY=<value of repository>
#TOKEN=<value of api token>


OUTPUT_DIR="${HOME}/.local/bin"
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "$OUTPUT_DIR does not exists. Hence creating this directory"
    mkdir -p ${OUTPUT_DIR}
fi


#check for the .cloudsmith_env file in the home directory
FILE="${HOME}/.cloudsmith_env"
if [ -f "$FILE" ]; then
    echo "$FILE exists. Now setting these as env variable"
fi

for i in `cat $FILE`; do
    echo "Now exporting $i"
    export $i
done

echo "Current env of this file is:"
echo ${ACCOUNT}/${REPOSITORY}
echo `env`

urls=$(cloudsmith ls pkgs ${ACCOUNT}/${REPOSITORY} -F json |jq -r '.data[].cdn_url')
echo $urls

for url in $urls; do
    current_binary=${url##*/}
    echo "now downloading to a file:${current_binary}"
    curl $url -o ${OUTPUT_DIR}/${current_binary}
done
