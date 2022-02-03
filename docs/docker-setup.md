# Dev Testing Set Up Notes

## Prerequisites

1. [Download](https://docs.docker.com/compose/install/) and set up Docker for your machine
  * [New Start Up Guide](https://www.docker.com/get-started)
  * Optionally, directly install the latest version of [docker-compose](https://github.com/docker/compose)
2. `git` installed on your system
  * A GitHub account if you wish to contribute 
  * Pull the code locally as typical with `git clone https://github.com/DARKMOONlite/Crafty_Controller_Fabric.git`
  * There are currently no build, docs, or test actions to run. This is pretty bare bones.

## Setting up the dev' environment 

The main set up is getting docker running and running compose. Run it in headless via the command-line with

```bash
docker-compose up -d
```

Next, put your minecraft server JAR's into `docker/minecraft_servers`. 
Once that is done, run the container

Then just access crafty as you normally would. When specifying the minecraft server directory, please use `/minecraft_servers`