#!/bin/sh

#We assume the nftmain.tgz is stored in /tmp directory
EXPORT_FILE="/tmp/nftmain.tgz"
DIR_NAME=$(dirname $EXPORT_FILE)
FNAME=$(basename $EXPORT_FILE)

cd $DIR_NAME
tar xvfz $FNAME
cd -

BASE_DIR="/tmp/Users/nilaysaha/Documents/nftmain"


mv ./index.html ./index.html.last
cp  $BASE_DIR/index.html .

mv ./page1.html ./page1.html.last
cp  $BASE_DIR/page1.html .

rm -rf ./assets.last
mv assets assets.last
cp -R  $BASE_DIR/assets .


echo "Following steps required to do now"
echo "Step 1: Except for the navbar, footer remove the <body> component to app/introduction/introduction.component.html"
echo "Step 2: Change the links in header replacing index.html with introduction"
echo "Step 3: Introduce this for routing:  <base href="/"> inside the <head>...</head> section."
