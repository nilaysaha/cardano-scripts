# Container image that runs your code
FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]

ARG CARDANO_NODE_VERSION=1.25.1
ARG CLOUDSMITH_API_KEY="727cdfad6176676bc9a3289e3ebf0b643a9e2362"

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
	libtool autoconf curl

RUN pip3 install --upgrade cloudsmith-cli


#install cabal
RUN wget https://downloads.haskell.org/~cabal/cabal-install-3.2.0.0/cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz ; \
	tar -xf cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz; \
	rm cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz cabal.sig; \
	mkdir -p ~/.local/bin; \
	mv cabal ~/.local/bin/;

ENV PATH="~/.local/bin:${PATH}"

#install ghci
RUN wget https://downloads.haskell.org/ghc/8.10.2/ghc-8.10.2-x86_64-deb9-linux.tar.xz; \
	tar -xf ghc-8.10.2-x86_64-deb9-linux.tar.xz; \
	rm ghc-8.10.2-x86_64-deb9-linux.tar.xz; \
	cd ghc-8.10.2; \
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
ENV CARDANO_NODE_VERSION="1.25.1"

#Now import the cardano-node
RUN git clone https://github.com/input-output-hk/cardano-node.git; \
	cd cardano-node; \
	cabal clean; \
	cabal update;\
	git fetch -all --tags; \
	git checkout ${CARDANO_NODE_VERSION} -b tag-${CARDANO_NODE_VERSION};\
	cabal build all;

ENV CARDANO_NODE_PATH="/cardano-node/dist-newstyle/build/x86_64-linux/ghc-8.10.2/cardano-node-1.25.1/x/cardano-node/build/cardano-node/cardano-node"
ENV CARDANO_CLI_PATH="/cardano-node/dist-newstyle/build/x86_64-linux/ghc-8.10.2/cardano-cli-${CARDANO_NODE_VERSION}/x/cardano-cli/build/cardano-cli/cardano-cli"
ENV CARDANO_CHAIRMAN_PATH="/cardano-node/dist-newstyle/build/x86_64-linux/ghc-8.10.2/cardano-node-chairman-${CARDANO_NODE_VERSION}/x/cardano-node-chairman/build/cardano-node-chairman/cardano-node-chairman"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

#Upload using api
RUN cloudsmith push raw lkbhpool/cardano ${CARDANO_NODE_PATH} --tags ${CARDANO_NODE_VERSION} --version ${CARDANO_NODE_VERSION}
RUN cloudsmith push raw lkbhpool/cardano ${CARDANO_CLI_PATH} --tags ${CARDANO_NODE_VERSION} --version ${CARDANO_NODE_VERSION}
RUN cloudsmith push raw lkbhpool/cardano ${CARDANO_CHAIRMAN_PATH} --tags ${CARDANO_NODE_VERSION} --version ${CARDANO_NODE_VERSION}
