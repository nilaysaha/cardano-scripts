#!/bin/sh

#install pre-req
sudo apt install build-essential
sudo apt-get install libtool
sudo apt-get install autoconf

sudo apt-get install -y \
	git automake build-essential pkg-config \
	libffi-dev libgmp-dev libssl-dev \
	libtinfo-dev libsystemd-dev \
	zlib1g-dev make g++ tmux git \
	jq wget libncursesw5 \
	libtool autoconf curl \
        awscli
    
git clone https://github.com/input-output-hk/libsodium; \
	cd libsodium; \
	git checkout 66f017f1; \
	./autogen.sh; \
	./configure; \
	make; \
	make install;

export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
export  PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"	

git clone https://github.com/bitcoin-core/secp256k1.git; \
        cd secp256k1; \  
        git reset --hard ac83be33d0956faf6b7f61a60ab524ef7d6a473a ; \
        ./autogen.sh; \
        ./configure --prefix=/usr --enable-module-schnorrsig --enable-experimental; \
        make; \
        make check; \
        sudo make install;

#cleanup
rm -rf libsodium secp256k1	
