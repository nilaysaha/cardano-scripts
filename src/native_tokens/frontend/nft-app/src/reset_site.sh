#!/bin/sh

BASE_DIR="/tmp/Users/nilaysaha/Documents/nftmain"

mv ./index.html ./index.html.last
cp  $BASE_DIR/index.html .
rm -f ./assets.last
mv ./assets assets.last
cp -R  $BASE_DIR/assets .


echo "Two steps required to do now"
echo "Step 1: Remove the <body> component to app/introduction/introduction.component.html"
echo "Step 2: Change the links in header replacing index.html with introduction"
