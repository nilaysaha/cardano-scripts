#!/bin/sh


helpFunction()
{
   echo ""
   echo "Usage: $0 -v version_id"
   echo -e "\t-a Git version of the cardano-node to be built. Mainly follows the format 1.23.0 (https://github.com/input-output-hk/cardano-node/releases/tag/1.23.0)"
   exit 1 # Exit script after printing help
}

installTools()
{
    echo "installing from scratch the toolchains"
    echo "-----------------------------------------------------------INSTALL THE BUILD ESSENTIALS--------------------------------------------------------------------------"
    sudo apt-get update -y
    sudo apt-get install automake build-essential pkg-config libffi-dev libncurses-dev  curl libtinfo5 libgmp-dev libssl-dev libtinfo-dev libsystemd-dev zlib1g-dev make g++ tmux git jq wget libncursesw5 libtool autoconf -y

    echo "-------------------------------------------------UNPACK, INSTALL AND UPDATE CABAL------------------------------------------------------"
    mkdir tmp
    cd tmp
    wget https://downloads.haskell.org/~cabal/cabal-install-3.2.0.0/cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz
    tar -xf cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz
    rm cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz cabal.sig
    mkdir -p ~/.local/bin
    mv cabal ~/.local/bin/
    export PATH="~/.local/bin:$PATH"

    echo "-------------------------------------------------UPDATE CABAL---------------------------------------------------------------------------"
    cabal update
    cabal --version


    echo "------------------------------------------------NOW INSTALL GHCUP-----------------------------------------------------------------------"
    curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
    export PATH="~/.ghcup/bin:$PATH"
    
    echo "-------------------------------------------------UPDATE GHCUP AND INSTALL GHC ----------------------------------------------------------"
    echo "Reference:https://forum.cardano.org/t/attention-spos-1-24-2-upgrade-guide-upgrade-now-for-the-upcoming-allegra-hard-fork-event/43094"
    ghcup upgrade
    ghcup install ghc 8.10.2
    ghcup set ghc 8.10.2      
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

	echo "---------------VERIFYING WHICH GIT TAG WE ARE ON NOW -------------------------"
	git describe --tags --abbrev=0
	
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

	echo "---------------------------------------UPDATE CABAL AND BUILD CARDANO-NODE------------------------------------------"
	cabal clean
	cabal update
	cabal build all

	echo "--------------------------------------INSTALL CARDANO-NODE INTO PROPER DIRECTORY------------------------------------"	
	cabal install all --bindir ~/.local/bin	
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
	mv ${HOME}/.cabal/store/ghc-8.10.2 /tmp/ghc-8.10.2-old
	cp -R ${CARDANO_NODE_DIR}/dist-newstyle/build/x86_64-linux/ghc-8.10.2 ${HOME}/.cabal/store/ghc-8.10.2
	
	echo "----------------------------Stopping Node for installing binaries------------------------------"
	stopNode

	echo "--------------------------- Linking new binaries version:${CARDANO_NODE_VERSION}---------------------------"
	cd ~/.cabal/bin
	mv cardano-node cardano-node.old
	mv cardano-cli cardano-cli.old
	mv cardno-node-chairman cardano-node-chairman.old
	ln -s ../store/ghc-8.10.2/cardano-cli-${CARDANO_NODE_VERSION}/x/cardano-cli/build/cardano-cli/cardano-cli
	ln -s ../store/ghc-8.10.2/cardano-node-${CARDANO_NODE_VERSION}/x/cardano-node/build/cardano-node/cardano-node
	ln -s ../store/ghc-8.10.2/cardano-node-chairman-${CARDANO_NODE_VERSION}/x/cardano-node-chairman/build/cardano-node-chairman/cardano-node-chairman	
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
    #installTools
    #installLibSodium
    # Now execute the stuff
    # Pullcode
    # buildNode   
    # linkNode
    exportBuild
fi

