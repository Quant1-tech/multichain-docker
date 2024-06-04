# Multichain Docker Compose with Explorer - v.2.3.3/2!

This `docker-compose.yml` shows how to start a **Docker Compose** controlled multi-node **MultiChain** infrastructure with one **Explorer** node attached on the MultiChain **master** node.

# Files

 - `docker-compose.yml`: define the infrastructure;
 - `node/Dockerfile`: define the multichain node base image that can be used as master or slave, depending on provided settings;
 - `node/entrypoint.sh`: it is the entrypoint that will be used for the node image, starting master or slave multichain daemon;
 - `explorer/Dockerfile`: define the base image that will be used to provide Multichain-Explorer-2 service;
 - `explorer/entrypoint.sh`: it is the entrypoint that will be used to start the explorer image using the provided parameters;

## Multichain node build arguments

To configure the multichain blockchain you can use the following argument at build stage:

 - `MULTICHAIN_RELEASE`: default value `2.3.3`, this value rapresents the Multichain release to use to build the image;
 - `MULTICHAIN_DOWNLOAD_URL` default value `https://www.multichain.com/download/multichain-2.3.3.tar.gz`, this value rapresents the Multichain archive to include in the built image.

To build the `node` image using the Community Edition binaries you can use the following command:

	$ docker build -t multichain-node:2.3.3 .

To build the `node` image using the Enterprise Demo binaries you can use the following command:

	$ docker build \
		--build-arg MULTICHAIN_RELEASE=2.3.3-enterprise-demo \
		--build-arg MULTICHAIN_DOWNLOAD_URL=https://www.multichain.com/download/enterprise/multichain-2.3.3-enterprise-demo.tar.gz \
		-t multichain-node:2.3.3-enterprise-demo .


## Multichain node configuration parameters

To configure the multichain blockchain you can use the following environment variables to defining the node behavior:

 - `CHAIN_NAME`: set the chain name, default value is set to `DockerChain`;
 - `NETWORK_PORT`: set the network port used by multichain daemon, default value is set to `6479`;
 - `RPC_PORT`: set the RPC port used by multichain daemon, default value is set to `6478`;
	 - the `explorer` image uses this parameter to connect to the given node;
 - `RPC_USER`: set the RPC username used by multichain daemon, default value is set to `multichainrpc`;
 - `RPC_PASSWORD`: set the RPC password used by multichain daemon, default value is set to `AjAoAutxA8yoRZHHn9nPsQo6346oMsATzZrhrwZzBbu8`;
 - `ENV RPC_ALLOW_IP`: set the ip/mask for the RPC sources allowed to connect to the multichain daemon, default value is set to `0.0.0.0/0`
 - `TARGET_BLOCK_TIME` : set the value for the `target-block-time` parameter used by multichain daemon, default value is set to `15`;
 - `ANYONE_CAN_CONNECT`: set the value for the `anyone-can-connect` used by multichain daemon, default value is set to `false`
 - `ANYONE_CAN_MINE`: set the value for the `anyone-can-mine` used by multichain daemon, default value is set to `false`;
 - `SEED_NODE_IP`: set the master node ip/dns reference, default value is not set;
 - `SEED_NODE_PORT`: set the master node network port to connect to, default value is not set;

**ATTENTION:**

 - *master* node **must** have both `SEED_NODE_IP` and `SEED_NODE_PORT` **not set**;
 - *slave* node **must** have both `SEED_NODE_IP` and `SEED_NODE_PORT` **set**;
 - *explorer* node **must** have `SEED_NODE_IP` and `RPC_PORT` **set**;

## Let's go!!

To start a new environment, please execute:

	docker compose up -d

this will start both the `master` and `slave` containers.
Execute:

	docker compose ps -a

You will see the `slave` container is not running. This is fine for the first execution: we have to provide authorization on the master node.
Look at `slave` container logs to find the required grant to provide on the master:

	$ docker compose logs slave | grep grant
	slave-1  | multichain-cli MyDockerChain grant 1... connect
	slave-1  | multichain-cli MyDockerChain grant 1... connect,send,receive

Execute the provided commands on the master node:

	$ docker exec -ti mc-master-1 multichain-cli MyDockerChain grant 1... connect
	$ docker exec -ti mc-master-1 multichain-cli MyDockerChain grant 1... connect,send,receive

Restart the `slave`:

	docker compose start slave

