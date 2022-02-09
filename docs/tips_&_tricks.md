# Tips and Tricks for getting the docker and server to run



##

---
## Accessing the image file structure
### Have you every wanted to see what your system actually looks like? To see if a file is there or not. Worry not, Now you can!
1. Ensure docker is up
2. Find the Container ID with the command 
```
    docker ps
```
3. Then all you need to do to view the file structure or run files is
```bash
docker exec -t -i "Container ID" /bin/bash
```
---
## Server Jar won't run in the web server
### This is the case if the server is "On" but none of the server files have been created.
1. Access the file structure via the method above
2. find the folder with the server jar file, by default this should be
```bash
ls server/server_1
```
3. From here manually run the server.jar file with
```bash
Java -jar server.jar
```
if any errors come up... good luck