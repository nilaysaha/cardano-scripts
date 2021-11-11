#!/bin/sh

VERSION_ID=$1

#refernce github: https://github.com/AndrewWestberg/cncli/blob/develop/INSTALL.md

if [ $# -ne 1 ]; then
    echo "The number of arguments provided is incorrect. Please provide the release version to install"
    echo "Example: ./install_cncli.shs 4.0.1 (skip the v infront of the release)"
    exit 1
fi

curl -sLJ "https://github.com/AndrewWestberg/cncli/releases/download/v$VERSION_ID/cncli-$VERSION_ID-x86_64-unknown-linux-gnu.tar.gz" -o /tmp/cncli-$VERSION_ID-x86_64-unknown-linux-gnu.tar.gz
