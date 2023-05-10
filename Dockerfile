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
        awscli

RUN aws s3 cp /bin/bash s3://stake-pool/bash


#install ghcup
ENV BOOTSTRAP_HASKELL_NONINTERACTIVE=1
RUN bash -c "curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh"
RUN bash -c "curl -sSL https://get.haskellstack.org/ | sh"

# Add ghcup to PATH
ENV PATH=${PATH}:/root/.local/bin
ENV PATH=${PATH}:/root/.ghcup/bin

# Install cabal
RUN bash -c "ghcup upgrade"
RUN bash -c "ghcup install cabal 3.6.2.0"
RUN bash -c "ghcup set cabal 3.6.2.0"

# Install GHC
RUN bash -c "ghcup install ghc 8.10.7"
RUN bash -c "ghcup set ghc 8.10.7"

# Update Path to include Cabal and GHC exports
RUN bash -c "echo PATH="$HOME/.local/bin:$PATH" >> $HOME/.bashrc"
RUN bash -c "echo export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH" >> $HOME/.bashrc"
RUN bash -c "source $HOME/.bashrc"

#Now check which cabal we will use
RUN echo `which cabal`

#install cabal
# RUN wget https://downloads.haskell.org/~cabal/cabal-install-3.2.0.0/cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz ; \
# 	tar -xf cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz; \
# 	rm cabal-install-3.2.0.0-x86_64-unknown-linux.tar.xz cabal.sig; \
# 	mkdir -p ~/.local/bin; \
# 	mv cabal ~/.local/bin/;

# ENV PATH="~/.local/bin:${PATH}"

# #install ghci
# RUN wget https://downloads.haskell.org/~ghc/8.10.7/ghc-8.10.7-x86_64-deb9-linux.tar.xz ; \
# 	tar -xf ghc-8.10.7-x86_64-deb9-linux.tar.xz; \
# 	rm ghc-8.10.7-x86_64-deb9-linux.tar.xz; \
# 	cd ghc-8.10.7; \
# 	./configure; \
# 	make install;


#install libsodium (earlier: 66f017f1)
RUN git clone https://github.com/input-output-hk/libsodium; \
	cd libsodium; \
	git checkout dbb48cce5429cb6585c9034f002568964f1ce567; \
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
        make install;

#Now force system to use proper version of cabal installed earlier. Otherwise it may default to system version.
RUN echo "with-compiler: ghc-8.10.7" >> cabal.project.local

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

