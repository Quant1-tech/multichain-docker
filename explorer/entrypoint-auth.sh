#!/bin/bash

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
##

EXPLORER_DIR=~/explorer-2

if [ -z "${SEED_NODE_IP}" ]; then
	echo "SEED_NODE_IP environment variable is required."
	exit 2
else
  echo -ne "[main]\nhost=0.0.0.0\nport=${LISTEN_PORT}\nbase=/\n[auth]\nendpoint=${USERAPI_ENDPOINT}\nheader_key=${USERAPI_KEY}\nheader_value=${USERAPI_VALUE}\n[chains]\nchain1=on\n[chain1]\nname=${CHAIN_NAME}\nrpchost=http://${SEED_NODE_IP}\nrpcport=${RPC_PORT}\nrpcuser=${RPC_USER}\nrpcpassword=${RPC_PASSWORD}\n" > ${EXPLORER_DIR}/multichain.ini
  rm -f ${EXPLORER_DIR}/*.log ${EXPLORER_DIR}/*.pid || true
	exec /usr/bin/python3 -m explorer multichain.ini
fi
