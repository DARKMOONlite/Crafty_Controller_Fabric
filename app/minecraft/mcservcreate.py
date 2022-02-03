from ast import For
import  os
import urllib3
import  shutil
import time

version = ""
fabric_version = ""
path = ''
path_type = ''
eulapath = ''
mod_required = ""
mod_urls = [["https://www.curseforge.com/minecraft/mc-mods/fabric-api/download/3609610/file","fabric-api-0.46.1+1.18.jar"],
            ["https://www.curseforge.com/minecraft/mc-mods/sodium/download/3605309/file","lithium-fabric-mc1.18.1-0.7.7.jar"],
            ["https://www.curseforge.com/minecraft/mc-mods/sodium/download/3605275/file","sodium-fabric-mc1.18.1-0.4.0-alpha6+build.14.jar"],
            ["https://www.curseforge.com/minecraft/mc-mods/phosphor/download/3573395/file","phosphor-fabric-mc1.18.x-0.8.1.jar"],
            ["https://www.curseforge.com/minecraft/mc-mods/ferritecore-fabric/download/3550048/file","ferritecore-4.0.0-fabric.jar"],
            ["https://www.curseforge.com/minecraft/mc-mods/worldedit/download/3631606/file","worldedit-mod-7.2.9.jar"]
            ]

def getinfo():
    global version
    global path
    global eulapath
    global fabric_version
    global path_type
    
    if os.name == 'nt':
        path_type = "\\"
    else:
        path_type = "/"
    
    print("Please Choose A Server Version:")
    print("\t eg: (1.18.1, 1.17.1, 1.16.5, 1.15.2) \n") 
    version = str(input("Please Enter Your Choice: ")).strip
    
    print("Please Select the Fabric Version you want:")
    print("recommended: 0.13.0")
    fabric_version = str(input()).strip
    
    path = str(input('Please Enter The Path You Would Like Your Server To Be Located In: '))
    eulapath = path + path_type + 'eula.txt'
    
    jar()
    
def jar():#Downloads the server Jar File
    global version
    global path
    global fabric_version
    if os.path.exists(path) == False:
        os.makedirs(path)
    print("Downloading {} Server Jar".format(version))
    url = "https://meta.fabricmc.net/v2/versions/loader/{}/{}/0.10.2/server/jar".format(version, fabric_version)
    c = urllib3.PoolManager()
    filename = path + path_type + 'fabric.jar'
    with c.request('GET', url, preload_content=False) as res, open(filename, 'wb') as out_file:
        shutil.copyfileobj(res, out_file)
        out_file.close()
    #Store MC version and Fabric version in txt doc    
    file = open(path+path_type+"version_info.txt" , "w")
    file.write("Minecraft Version = {} \n Fabric Version = {}".format(version,fabric_version))
    file.close()
    
    mods()
    
    
def mods(): # Downloads mods for the server and places them within the mods folder
#? A better method to store plugins (because of their small size would be 
#?to store theme within a file and then copy them to the mod folder when needed)
    global path
    global modask
    global version
    global mod_urls
    global mod_required  
    custom =True # Custom Allows you to input multiple custom mod urls individually
    basic_done = False; # Triggers when basic mod packet is installed        
    
    print('What Mods would you like for your server?')
    print("\n For Basic performance mods type: \"BASIC\"")
    print("\n Basic Mods are for 1.18.1 only")
    print("\n or for custom mods, enter url of mods individually") 
    print("\n Once Required Mods are downloaded, \n or if no mods are desired type: \"DONE\"")   
    while custom == True:        
        mod_required = input()            
        if mod_required == "DONE":
            print("Mod Process Finished")
            custom = False
        elif mod_required == "BASIC":
            if basic_done==False:
                
                print("Downloading Basic Performance Mods")
                path = path + '{}mods'.format(path_type)
                if os.path.exists(path) == False:
                    os.makedirs(path)

                for x in range(len(mod_urls)):
                    print("Downloading: {}".format(mod_urls[x][1]))
                    c = urllib3.PoolManager()
                    filename = path + path_type + mod_urls[x][1]
                    with c.request('GET', mod_urls[x][0], preload_content=False) as res, open(filename, 'wb') as out_file:
                        shutil.copyfileobj(res, out_file)
                        out_file.close() 
                    time.sleep(2)
                    
                basic_done=True
                print("Basic Mods Downloaded")
            else:
                print("Basic Mods Already Installed, Type DONE or a Custom URL To Continue.")
            
        else: #? Runs if custom URL or anything else is entered  
            #! IDK if this works lol
            print("Trying to Download: {}".format(mod_required))
            c = urllib3.poolmanager()
            filename = path+path_type+mod_required.split("/")[-1]   
            with c.request('GET', mod_required, preload_content=False) as res, open(filename, 'wb') as out_file:
                shutil.copyfileobj(res, out_file)
                out_file.close()  
            time.sleep(2)
        
    eulagen()
                
def eulagen(): #Auto-completes the minecraft eula
    global eulapath
    file = open(eulapath , "w")
    file.write("eula=true")
    file.close()
    end()
    
def end():
    global path
    print("Please Enter The Following Info Into Crafty:")
    print("\t Path: " + path + "\n \t Server Jar: fabric.jar ")

getinfo()