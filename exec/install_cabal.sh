#!/bin/sh

#install cabal

INSTALL_DIR=$HOME/opt/install_code
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR


sudo apt-get install -y \
        python3 \
        python3-pip \
        git automake build-essential pkg-config \
        libffi-dev libgmp-dev libssl-dev \
        libtinfo-dev libsystemd-dev \
        zlib1g-dev make g++ tmux git \
        jq wget libncursesw5 \
        libtool autoconf curl


wget https://downloads.haskell.org/~cabal/cabal-install-3.2.0.0/cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz ; \
    tar -xf cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz; \
    rm cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz cabal.sig; \
    mkdir -p ~/.local/bin; \
    mv cabal ~/.local/bin/;
    
export PATH="~/.local/bin:${PATH}"

#install ghci                                                                                                                                                                                                                                                                                                                                                               
wget https://downloads.haskell.org/ghc/8.10.2/ghc-8.10.2-x86_64-deb9-linux.tar.xz; \
    tar -xf ghc-8.10.2-x86_64-deb9-linux.tar.xz; \
    rm ghc-8.10.2-x86_64-deb9-linux.tar.xz; \
    cd ghc-8.10.2; \
    ./configure; \
    sudo make install;


#install libsodium                                                                                                                                                                                                                                                                                                                                                          
git clone https://github.com/input-output-hk/libsodium; \
    cd libsodium; \
    git checkout 66f017f1; \
    ./autogen.sh; \
    ./configure; \
    make; \
    make install;
