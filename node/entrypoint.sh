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

MULTICHAIN_DIR=~/.multichain
PARAMS_DAT=${MULTICHAIN_DIR}/${CHAIN_NAME}/params.dat
CHAIN_MULTICHAIN_CONF=${MULTICHAIN_DIR}/${CHAIN_NAME}/multichain.conf
MULTICHAIN_CONF=${MULTICHAIN_DIR}/multichain.conf
MULTICHAIND_OPTIONS="-printtoconsole -shrinkdebugfile=1 -shrinkdebugfilesize=1 -explorersupport=2"

if [ -n "${SEED_NODE_IP}" -a -n "${SEED_NODE_PORT}" ]; then
	echo "Wait for 30 seconds to ensure the master node is ready."
	sleep 3
	[ ! -d ${MULTICHAIN_DIR} ] && mkdir ${MULTICHAIN_DIR}
	cat <<EOF > ${MULTICHAIN_CONF}
rpcbind=0.0.0.0
rpcconnect=localhost
rpcuser=${RPC_USER}
rpcpassword=${RPC_PASSWORD}
rpcallowip=${RPC_ALLOW_IP}
rpcport=${RPC_PORT}
EOF
	exec multichaind ${MULTICHAIND_OPTIONS} "${CHAIN_NAME}@${SEED_NODE_IP}:${SEED_NODE_PORT}" $@
	exit 2
else
	echo "Starting Master node"
	if [ ! -d ~/.multichain/${CHAIN_NAME} ]; then
		CREATE_OPTIONS="-default-network-port=${NETWORK_PORT} -default-rpc-port=${RPC_PORT}"

		[ -n "${TARGET_BLOCK_TIME}" -a 15 -ne ${TARGET_BLOCK_TIME} ] && \
			CREATE_OPTIONS="${CREATE_OPTIONS} -target-block-time=${TARGET_BLOCK_TIME}"

		[ -n "${ANYONE_CAN_CONNECT}" -a "false" != "${ANYONE_CAN_CONNECT}" ] && \
			CREATE_OPTIONS="${CREATE_OPTIONS} -anyone-can-connect=${ANYONE_CAN_CONNECT}"

		[ -n "${ANYONE_CAN_MINE}" -a "false" != "${ANYONE_CAN_MINE}" ] && \
			CREATE_OPTIONS="${CREATE_OPTIONS} -anyone-can-mine=${ANYONE_CAN_MINE}"

		multichain-util create "${CHAIN_NAME}" ${CREATE_OPTIONS}

		echo "Configure Chain ${CHAIN_NAME}"
		cp ${CHAIN_MULTICHAIN_CONF}{,.bak}
		cat <<EOF > ${CHAIN_MULTICHAIN_CONF}
rpcbind=0.0.0.0
rpcconnect=localhost
rpcuser=${RPC_USER}
rpcpassword=${RPC_PASSWORD}
rpcallowip=${RPC_ALLOW_IP}
rpcport=${RPC_PORT}
EOF
	fi
	echo "Start chain ${CHAIN_NAME}"
	# Avvia chain
	# 	multichaind chain1
	exec multichaind $MULTICHAIND_OPTIONS "${CHAIN_NAME}" $@
	exit 3
fi
