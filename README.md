# bloc_energy
Hackaton at imaguru in Madrid

[Building a Block Energy] 

## Installation

1. Make sure [Python 3.6+](https://www.python.org/downloads/) is installed. 

# Docker

Building One BlockChain

For running and scale this blockchain program is to use Docker. Follow the instructions below to create a local Docker container:

Clone this repository
Build the docker container

$ docker build -t blockchain .

Run the container


```
$ docker run --rm -p 80:5000 blockchain
```

To add more instances, vary the public port number before the colon:

```
$ docker run --rm -p 81:5000 blockchain
```
```
$ docker run --rm -p 82:5000 blockchain
```
```
$ docker run --rm -p 83:5000 blockchain
```