#!/bin/sh


helpFunction()
{
   echo ""
   echo "Usage: $0 -v version_id"
   echo -e "\t-a Git version of the cardano-node to be built. Mainly follows the format 1.23.0 (https://github.com/input-output-hk/cardano-node/releases/tag/1.23.0)"
   exit 1 # Exit script after printing help
}


updateBuildEnv() {
    echo "--------------Install ghcup if needed--------------------"
    echo "Reference:https://forum.cardano.org/t/attention-spos-1-24-2-upgrade-guide-upgrade-now-for-the-upcoming-allegra-hard-fork-event/43094"
    ghcup --version
    curl --proto ‘=https’ --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh

    echo "-------------Update ghcup-------------------"
    ghcup upgrade
    ghcup install ghc 8.10.2
    ghcup set ghc 8.10.2      
}


Pullcode() {
    CARDANO_NODE_DIR="${HOME}/projects/cardano/cardano-node"
    
    if [ -d ${CARDANO_NODE_DIR} ] 
    then
	echo "Directory ${CARDANO_NODE_DIR} exists."
	echo "Now fetching locally new version of cardano-node:${CARDANO_NODE_VERSION}"
	cd ${CARDANO_NODE_DIR}
	echo "Do clean of earlier builds and update"
	cabal clean
	cabal update
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
	BACKUP_DIR="${CARDANO_NODE_DIR}/dist-newstyle_build_${CARDANO_NODE_VERSION}"
	if [ ! -d ${BACKUP_DIR} ]
	then
	    mv dist-newstyle ${BACKUP_DIR}
	fi
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
	mv cardno-node-chairman cardano-node-chairman.old
	ln -s ../store/ghc-8.6.5/cardano-cli-${CARDANO_NODE_VERSION}/x/cardano-cli/build/cardano-cli/cardano-cli
	ln -s ../store/ghc-8.6.5/cardano-node-${CARDANO_NODE_VERSION}/x/cardano-node/build/cardano-node/cardano-node
	ln -s ../store/ghc-8.6.5/cardano-node-chairman-${CARDANO_NODE_VERSION}/x/cardano-node-chairman/build/cardano-node-chairman/cardano-node-chairman
	ln -s ../store/ghc-8.6.5/cardano-node-chairman-1.24.2/x/cardano-node-chairman/build/cardano-node-chairman/cardano-node-chairman
	
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

exportBuild() {
    cd ${HOME}
    tar cvfz ${HOME}/temp/cabal-${CARDANO_NODE_VERSION}.tgz ${HOME}/.cabal
    scp -i ~/.ssh/id_rsa_node_1 ${HOME}/temp/cabal-${CARDANO_NODE_VERSION}.tgz  nsaha@10.0.0.3:.
}


installLibSodium() {
    cd ${HOME}/projects/cardano
    git clone https://github.com/input-output-hk/libsodium
    cd libsodium
    git checkout 66f017f1
    ./autogen.sh
    ./configure
    make
    sudo make install    
}

while getopts "v:l" opt
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
    installLibSodium
    # Now execute the stuff
    # pullCode
<<<<<<< HEAD
    # buildNode   
    # linkNode
    # exportBuild
=======
    # buildNode
    #linkNode
    stopNode
    startNode
    exportBuild
>>>>>>> 28a76c94b7b8abfbe16e2872982476cd518a8ac3
fi

