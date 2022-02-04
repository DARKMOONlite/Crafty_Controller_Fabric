# Crafty Controller Fork of the [Original GitLab Repo](https://gitlab.com/crafty-controller/crafty-web)

> Python based Server Manager / Web Portal for your Minecraft Server

# Important: Latest Changes

## What is Crafty?

Crafty is a Minecraft Server Wrapper / Controller / Launcher. The purpose 
of Crafty is to launch a Minecraft server in the background and present 
a web interface for the admin to use to interact with their server. Crafty 
is compatible with Windows (7, 8, 10) and Linux (via Python). 

## Features
- [Tornado](https://www.tornadoweb.org/en/stable/) webserver used as a backend for the web side.
- [Argon2](https://pypi.org/project/argon2-cffi/) used for password hashing
- [SQLite DB](https://www.sqlite.org/index.html) used for settings.
- [Adminlte](https://adminlte.io/themes/AdminLTE/index2.html) used for web templating
- [Font Awesome 5](https://fontawesome.com/) used for Buttons 

## How does it work?

Crafty is launched via the command line, normally via a bat or sh script. 
Crafty will then automatically start a Tornado web server on the back end, 
as well as your Minecraft server if auto-start is enabled. You can remotely 
manage your server via the web interface, either on a PC, or on your phone. 
Logins are secure and use the most advanced web security models available.

## Supported OS'

Make your life simple and just run this vis a vis Docker. However if you insist....

- Linux - we run this on 20.04 but any distro that supports Python 3 and JDK 8 will do.
- Windows (7, 8, 10) via a compiled Executable, no need for Python installation.

## Installation
~Install documentation is available here on GitLab via the [wiki](https://gitlab.com/crafty-controller/crafty-web/wikis/Install-Guides).~

^^ This is bound to change as we mess with the build chain and add testing.

## Documentation
~Check out our shiny new documentation [right on GitLab](https://gitlab.com/crafty-controller/crafty-web/wikis/home).~

^^ Likewise, this will probs be replaced by a different wiki.

## Meta

[Original GitLab Repo](https://gitlab.com/crafty-controller/crafty-web)
[Forked Git Repo](https://github.com/DARKMOONlite/Crafty_Controller_Fabric)

[Crafty Controller Website - Project Homepage](https://craftycontrol.com/)

[Discord Channel Invite Link](https://discord.gg/9VJPhCE)
