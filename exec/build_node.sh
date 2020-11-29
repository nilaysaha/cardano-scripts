#!/bin/sh


helpFunction()
{
   echo ""
   echo "Usage: $0 -v version_id"
   echo -e "\t-a Git version of the cardano-node to be built. Mainly follows the format 1.23.0 (https://github.com/input-output-hk/cardano-node/releases/tag/1.23.0)"
   exit 1 # Exit script after printing help
}

pullCode() {
    CARDANO_NODE_DIR="${HOME}/projects/cardano/cardano-node"
    
    if [ -d ${CARDANO_NODE_DIR} ] 
    then
	echo "Directory ${CARDANO_NODE_DIR} exists."
	echo "Now fetching locally new version of cardano-node:${CARDANO_NODE_VERSION}"
	cd ${CARDANO_NODE_DIR}
	echo "Current working directory is:`pwd`"
	echo "-----------Fetching remote tags---------------"
	git fetch --all --tags
	tag=$(git describe --tags `git rev-list --tags --max-count=1`)
	echo  "latest tag is:${tag}"
	echo "-----------Checking out the ${CARDANO_NODE_VERSION}--------------"
	git checkout ${CARDANO_NODE_VERSION} -b tag-${CARDANO_NODE_VERSION}
	#git log --oneline --graph	
    else
	echo "Error: Directory ${CARDANO_NODE_DIR} does not exists. First get this repository installed"
    fi
}

buildNode() {
    CARDANO_NODE_DIR="${HOME}/projects/cardano/cardano-node"
    
    if [ -d ${CARDANO_NODE_DIR} ] 
    then
	echo "Directory ${CARDANO_NODE_DIR} exists."
	echo "Now building new version of cardano-node"
	cd ${CARDANO_NODE_DIR}
	cabal update
	cabal build all
    else
	echo "Error: Directory ${CARDANO_NODE_DIR} does not exists."
    fi
    
}


linkNode() {
    CARDANO_NODE_DIR="${HOME}/projects/cardano/cardano-node"
    
    if [ -d ${CARDANO_NODE_DIR} ] 
    then
	echo "Directory ${CARDANO_NODE_DIR} exists."
	echo "Now building new version of cardano-node"
	cd ${CARDANO_NODE_DIR}
	rm -rf /tmp/ghc-8.6.5-old
	mv ${HOME}/.cabal/store/ghc-8.6.5 /tmp/ghc-8.6.5-old
	cp -R ${CARDANO_NODE_DIR}/dist-newstyle/build/x86_64-linux/ghc-8.6.5 ${HOME}/.cabal/store/ghc-8.6.5
	
	echo "----------------------------Stopping Node for installing binaries------------------------------"
	stopNode

	echo "--------------------------- Linking new binaries version:${CARDANO_NODE_VERSION}---------------------------"
	cd ~/.cabal/bin
	mv cardano-node cardano-node.old
	mv cardano-cli cardano-cli.old
	mv chairman chairman.old
	ln -s ../store/ghc-8.6.5/cardano-cli-${CARDANO_NODE_VERSION}/x/cardano-cli/build/cardano-cli/cardano-cli
	ln -s ../store/ghc-8.6.5/cardano-node-${CARDANO_NODE_VERSION}/x/cardano-node/build/cardano-node/cardano-node
	ln -s ../store/ghc-8.6.5/cardano-node-chairman-${CARDANO_NODE_VERSION}/x/cardano-node-chairman/build/cardano-node-chairman/cardano-node-chairman

	echo "---------------------------Starting Node after relinking binaries------------------------------"
	startNode
    else
	echo "Error: Directory ${CARDANO_NODE_DIR} does not exists."
    fi
}

stopNode() {
    pkill -9 cardano-node
}

startNode() {
    sudo systemctl start shelly-cardano
}


while getopts "v:" opt
do
   case "$opt" in
      v ) CARDANO_NODE_VERSION="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$CARDANO_NODE_VERSION" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
else
    # Now execute the stuff
    pullCode
    buildNode
    linkNode
fi

