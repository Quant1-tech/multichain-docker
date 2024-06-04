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

ARG DEFAULT_LISTEN_PORT=4444
ARG RPC_DEFAULT_PORT=6478
ARG RPC_DEFAULT_PASSWORD="AjAoAutxA8yoRZHHn9nPsQo6346oMsATzZrhrwZzBbu8"

LABEL org.label-schema.maintainer="brunopelaia@5minformatica.it"
LABEL org.label-schema.vendor="5 EMME Informatica S.p.A."

LABEL org.label-schema.url="https://github.com/MultiChain/multichain-explorer-2"
LABEL org.label-schema.name="MultiChain Explorer 2"
LABEL org.label-schema.version="2"
LABEL org.label-schema.description="First docker image for running MultiChain Explorer 2"
LABEL org.label-schema.schema-version = "1.0"

ENV DEBIAN_FRONTEND=noninteractive RPC_PASSWORD=${RPC_DEFAULT_PASSWORD}
ENV CHAIN_NAME="DockerChain" RPC_PORT=${RPC_DEFAULT_PORT} RPC_USER="multichainrpc"
ENV SEED_NODE_IP="" LISTEN_PORT=${DEFAULT_LISTEN_PORT}

EXPOSE ${DEFAULT_LISTEN_PORT}

RUN apt-get update \
        && apt-get upgrade -q -y \
        && apt-get dist-upgrade -q -y \
        && apt-get install -q -y \
#           curl \
#           file \
           git \
#           less \
#           lsof \
#           iputils-ping \
#           net-tools \
#           netcat \
#           psmisc \
           python3 \
#           screen \
#           telnet \
#           vim-tiny \
#           wget \
#        && update-alternatives --install /usr/bin/vim vim /usr/bin/vim.tiny 10 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && useradd -c "MultiChain user" -d /home/multichain -m -u 4000 -U multichain \
        && echo 'root:multichain' | chpasswd \
	&& echo 'multichain:multichain' | chpasswd \
	&& git clone --depth 1 -b master https://github.com/MultiChain/multichain-explorer-2.git /home/multichain/explorer-2 \
	&& rm -rf /home/multichain/explorer-2/.git* /home/multichain/explorer-2/tmp.out \
	&& chown -R multichain:multichain /home/multichain/explorer-2

WORKDIR /home/multichain/explorer-2

COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER multichain

ENTRYPOINT [ "entrypoint.sh" ]
