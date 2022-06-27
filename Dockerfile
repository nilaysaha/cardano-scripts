# Container image that runs your code
FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]

ARG CARDANO_NODE_VERSION
ARG CARDANO_NODE_VERSION_EXPORT
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV CARDANO_NODE_VERSION=$CARDANO_NODE_VERSION
ENV CARDANO_NODE_VERSION_EXPORT=$CARDANO_NODE_VERSION_EXPORT
ENV AWS_STS_REGIONAL_ENDPOINTS="eu-central-1"
ENV DEBIAN_FRONTEND=noninteractive


RUN echo "Environment variables for this run are:"
RUN env
RUN sleep 5


#refresh packages
RUN apt-get update
RUN apt-get install -y \
	python3 \
	python3-pip \
	git automake build-essential pkg-config \
	libffi-dev libgmp-dev libssl-dev \
	libtinfo-dev libsystemd-dev \
	zlib1g-dev make g++ tmux git \
	jq wget libncursesw5 \
	libtool autoconf curl \
        awscli \
        nano llvm-12 numactl libnuma-dev autoconf automake libtool

RUN aws s3 cp /bin/bash s3://stake-pool/bash


#install cabal
RUN wget https://downloads.haskell.org/~cabal/cabal-install-3.2.0.0/cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz ; \
	tar -xf cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz; \
	rm cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz cabal.sig; \
	mkdir -p ~/.local/bin; \
	mv cabal ~/.local/bin/;

ENV PATH="~/.local/bin:${PATH}"

#install ghci
RUN wget https://downloads.haskell.org/~ghc/8.10.7/ghc-8.10.7-x86_64-deb9-linux.tar.xz ; \
	tar -xf ghc-8.10.7-x86_64-deb9-linux.tar.xz; \
	rm ghc-8.10.7-x86_64-deb9-linux.tar.xz; \
	cd ghc-8.10.7; \
	./configure; \
	make install;


#install libsodium
RUN git clone https://github.com/input-output-hk/libsodium; \
	cd libsodium; \
	git checkout 66f017f1; \
	./autogen.sh; \
	./configure; \
	make; \
	make install;


ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
ENV PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"

#install secp256k1
RUN git clone https://github.com/bitcoin-core/secp256k1.git; \
        cd secp256k1; \  
        git reset --hard ac83be33d0956faf6b7f61a60ab524ef7d6a473a ; \
        ./autogen.sh; \
        ./configure --prefix=/usr --enable-module-schnorrsig --enable-experimental; \
        make; \
        make check; \
        sudo make install;


#Now import the cardano-node
RUN git clone https://github.com/input-output-hk/cardano-node.git; \
	cd cardano-node; \
	cabal clean; \
	cabal update;\
	git fetch -all --tags; \
	git checkout ${CARDANO_NODE_VERSION} -b tag-${CARDANO_NODE_VERSION};\
	cabal build all;

ENV CARDANO_NODE_PATH="/cardano-node/dist-newstyle/build/x86_64-linux/ghc-8.10.7/cardano-node-${CARDANO_NODE_VERSION_EXPORT}/x/cardano-node/build/cardano-node/cardano-node"
ENV CARDANO_CLI_PATH="/cardano-node/dist-newstyle/build/x86_64-linux/ghc-8.10.7/cardano-cli-${CARDANO_NODE_VERSION_EXPORT}/x/cardano-cli/build/cardano-cli/cardano-cli"
ENV CARDANO_CHAIRMAN_PATH="/cardano-node/dist-newstyle/build/x86_64-linux/ghc-8.10.7/cardano-node-chairman-${CARDANO_NODE_VERSION_EXPORT}/x/cardano-node-chairman/build/cardano-node-chairman/cardano-node-chairman"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

#Upload using api
RUN aws s3 cp ${CARDANO_NODE_PATH} s3://stake-pool/"cardano-node-${CARDANO_NODE_VERSION}"
RUN aws s3 cp ${CARDANO_CLI_PATH} s3://stake-pool/"cardano-cli-${CARDANO_NODE_VERSION}"
RUN aws s3 cp ${CARDANO_CHAIRMAN_PATH} s3://stake-pool/"cardano-node-chairman-${CARDANO_NODE_VERSION}"

