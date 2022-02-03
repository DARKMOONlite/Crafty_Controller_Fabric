# Dev Testing Set Up Notes

## Prerequisites:

1. Docker: [Download](https://docs.docker.com/compose/install/) and set up Docker for your machine
   - [New Start Up Guide](https://www.docker.com/get-started)
   - Optionally, directly install the latest version of [docker-compose](https://github.com/docker/compose)
  
    - If you have issues installing Docker on Windows relating to WSL2:
      - Re-run the install manually from [here](https://docs.microsoft.com/en-gb/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
<br/><br/>     

2. `git` installed on your system: [Link](https://git-scm.com/downloads)
    - A GitHub account is needed if you wish to contribute 

---
## Download:

  * Pull the code locally with command-line with `git clone https://github.com/DARKMOONlite/Crafty_Controller_Fabric.git "destination folder" `
  * There are currently no build, docs, or test actions to run. This is pretty bare bones.
---
## Setting up the dev' environment 

The main set up is getting docker running and running compose. Run it in headless via the command-line with


```bash
cd "location of directory"

docker-compose up -d
```

Next, put your minecraft server JAR's into `docker/minecraft_servers`. 
Once that is done, run the container

Then just access crafty as you normally would. When specifying the minecraft server directory, please use `/minecraft_servers`