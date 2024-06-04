## This project is based on https://github.com/Kunstmaan/docker-multichain repository.
##
## This file is part of Multichain Docker Repository by 5 EMME Informatica
## Copyright (C) 2024 5 EMME Informatica
##
## Multichain Docker Repository by 5 EMME Informatica is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
FROM ubuntu:xenial

ARG MULTICHAIN_RELEASE=2.3.3
ARG MULTICHAIN_DOWNLOAD_URL=http://www.multichain.com/download/multichain-${MULTICHAIN_RELEASE}.tar.gz
ARG NETWORK_DEFAULT_PORT=6479
ARG RPC_DEFAULT_PORT=6478
ARG RPC_DEFAULT_PASSWORD="AjAoAutxA8yoRZHHn9nPsQo6346oMsATzZrhrwZzBbu8"

LABEL org.label-schema.maintainer="brunopelaia@5minformatica.it"
LABEL org.label-schema.vendor="5 EMME Informatica S.p.A."

LABEL org.label-schema.url="https://www.multichain.com/"
LABEL org.label-schema.name="MultiChain Node"
LABEL org.label-schema.version="${MULTICHAIN_RELEASE}"
LABEL org.label-schema.description="First docker image for running MultiChain node using release ${MULTICHAIN_RELEASE}"
LABEL org.label-schema.schema-version = "1.0"
LABEL org.label-schema.docker.cmd="docker run -d -p 6479:6479 -p 6478:6478 -v multichain_volume:/home/multichain/.multichain multichain-base:${MULTICHAIN_RELEASE}"

ENV DEBIAN_FRONTEND=noninteractive MULTICHAIN_RELEASE=${MULTICHAIN_RELEASE} RPC_PASSWORD=${RPC_DEFAULT_PASSWORD}
ENV CHAIN_NAME="DockerChain" NETWORK_PORT=${NETWORK_DEFAULT_PORT} RPC_PORT=${RPC_DEFAULT_PORT} RPC_USER="multichainrpc"
ENV RPC_ALLOW_IP="0.0.0.0/0" BLOCKNOTIFY_SCRIPT="" TARGET_BLOCK_TIME=15 ANYONE_CAN_CONNECT="false" ANYONE_CAN_MINE="false"
ENV SEED_NODE_IP="" SEED_NODE_PORT=""

EXPOSE ${RPC_DEFAULT_PORT}

RUN apt-get update \
        && apt-get upgrade -q -y \
        && apt-get dist-upgrade -q -y \
        && apt-get install -q -y \
#           curl \
#           file \
#           git \
#           less \
#           lsof \
#           iputils-ping \
#           net-tools \
#           netcat \
#           psmisc \
#           python3 \
#           screen \
#           telnet \
#           vim-tiny \
           wget \
#        && update-alternatives --install /usr/bin/vim vim /usr/bin/vim.tiny 10 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && mkdir /tmp/multichain \
        && wget -O /tmp/multichain/multichain.tgz ${MULTICHAIN_DOWNLOAD_URL} \
        && tar xzf /tmp/multichain/multichain.tgz -C /tmp/multichain/ --strip-components=1 \
        && mv /tmp/multichain/multichaind /tmp/multichain/multichaind-cold /tmp/multichain/multichain-util /tmp/multichain/multichain-cli /usr/local/bin \
        && rm -rf /tmp/multichain \
        && useradd -c "MultiChain user" -d /home/multichain -m -u 4000 -U multichain \
        && echo 'root:multichain' | chpasswd \
        && echo 'multichain:multichain' | chpasswd

WORKDIR /home/multichain

COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh \
	&& mkdir /home/multichain/.multichain \
	&& chown -R multichain:multichain /home/multichain/.multichain

USER multichain

VOLUME [ "/home/multichain/.multichain" ]

ENTRYPOINT [ "entrypoint.sh" ]
