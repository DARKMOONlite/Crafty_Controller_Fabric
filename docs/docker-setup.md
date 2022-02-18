# Dev Testing Set Up Notes

## Prerequisites

1. [Download](https://docs.docker.com/compose/install/) and set up Docker for your machine
  * [New Start Up Guide](https://www.docker.com/get-started)
  * Optionally, directly install the latest version of [docker-compose](https://github.com/docker/compose)
  
#### If you have issues installing Docker on Windows relating to WSL2:
  1. Re-run the install manually from [here](https://docs.microsoft.com/en-gb/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)

1. `git` installed on your system
  * A GitHub account if you wish to contribute 
  * Pull the code locally as typical with `git clone https://github.com/**DARKMOONlite**/Crafty_Controller_Fabric.git`
  * There are currently no build, docs, or test actions to run. This is pretty bare bones.

## Setting up the dev' environment 

### Setting Up a Local Python Dev Environment

If you prefer to test Python code without running the full Docker stack, you will need the following set up,

1. Install and set up a virtual env
    1. Install virtualenv: `python -m pip install virtualenv --user`;
    2. Create a virtualenv in the cwd: `python -m virtualenv .`;
2. Activate/Source the virtualenv scripts: `Scripts\activate` or `source venv/bin/activate`;
3. Install the dev dependencies: `pip3 install --upgrade pip --no-cache-dir -r requirements.txt`
4. Done!

### Building Docker and Running a "Fresh" Installation

> If you've previously messed with the installation or want to restart the process, you'll need to clean the `docker/db/` directory. Remove everything in this directory barring the ignore file.
2. Build the docker image by running (this will take a while)
    * If this gives you any issues, re-attempt and additionally include the `--no-cache` arg.

```bash
docker-compose build
```

4. Next, put your minecraft server JAR's into `docker/minecraft_servers`;
5. **OR** Then just access crafty as you normally would. When specifying the minecraft server directory, please use `/minecraft_servers`  (Web UI)
6. Once the image has built and you have optionally added the jar's, run it in headless via the command-line with

```bash
docker-compose up -d
```

5. Done!

6. Not Done!  if you want the MC server to run, run the server.jar file manually via the method described in tips and tricks
7. Then Run the minecraft Server.
8. Done!