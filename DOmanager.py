#!/usr/bin/python

'''
Author: Hunter Gregal

Requires: python-digitalocean
pip install -U python-digitalocean

To Suppress SSL Errors:
pip install pyopenssl ndg-httpsclient pyasn1
'''
import argparse
import digitalocean as do
import os, sys

#Debug
from IPython import embed

def initManager():
    f = open("token.conf", "r")
    secretToken = f.readline()
    f.close()
    manager = do.Manager(token=secretToken)
    return manager

def setup():
    print "Please paste your Digital Ocean API token below"
    token = raw_input("API Token: ")
    config = open("token.conf", "w")
    config.write(token)
    config.close
    print "Digital Ocean API Token Succesfully setup!"

def checkSetup():
    if (os.stat("token.conf").st_size == 0):
        print "Digital Ocean API Token Not Configured."
        choice = raw_input("Would you like to configure your API token now? [y/n]: ")
        if (choice == "y" or choice == "Y"):
            setup()
        else:
            print "Please setup your Digital Ocean API token to continue..."
            sys.exit(0)

def menu(manager):
    os.system("clear")
    print "\n#################################"
    print "Welcome to the Digital Ocean Manager!\n Please choose an option number below\n"
    print "#################################\n"

    print "1) List Droplets (All, Running, Off)"
    print "2) Droplets Power Control (Shutdown, Restart, Boot)"
    print "3) Create Droplets (Single, Multi)"
    print "4) Destroy Droplets (Single, Multi)"
    print "5) List Images (Snapshots, Backups)"
    print "6) Advanced Droplet Management (Snapshots, Backups, Reset Root Password)"
    print "7) Exit"
    print "#################################\n"
    processOptions(manager)

def processOptions(manager):
    choice = raw_input("Choice: ")
    if (choice == "1"):
        listDroplets(manager)
    elif (choice == "2"):
        powerControlDroplets(manager)
    elif (choice == "3"):
        createDroplets()
    elif (choice == "4"):
        destroyDroplets()
    elif (choice == "5"):
        listImages()
    elif (choice == "6"):
        advancedMenu()
    elif (choice == "7"):
        sys.exit(0)
    else:
        print "\nInvalid Choice!"

    raw_input("Press Enter to Continue...")

def listDroplets(manager):
    droplets = manager.get_all_droplets()
    print "\n#################################\n"
    print "1) Show All Droplets"
    print "2) Show Active Droplets"
    print "3) Show Off Droplets"
    choice = raw_input("Choice: ")
    if (choice == "1"):
        for droplet in droplets:
            droplet_info(droplet)
    elif (choice == "2"):
        for droplet in droplets:
            if "active" in droplet.status:
                droplet_info(droplet)
    elif (choice == "3"):
        for droplet in droplets:
            if "off" in droplet.status:
                droplet_info(droplet)
    else:  
        print "\nInvalid Choice!"
    
    raw_input("Press Enter to Continue...")
    menu(manager)

def droplet_info(droplet):
    print "#################################"
    print "Name:", droplet.name
    print "Image:", droplet.image.get("name")
    print "Region:", droplet.region.get("name")
    print "Disk:", droplet.size.get("disk")
    print "Memory:", droplet.size.get("memory")
    print "STATUS:", droplet.status

def powerControlDroplets(manager):
    droplets = manager.get_all_droplets()
    print "\n#################################\n"
    print "1) Shutdown Droplets"
    print "2) Restart (PowerCycle) Droplets"
    print "3) Boot Droplets"
    choice = raw_input("Choice: ")

    if (choice == "1"):
        for droplet in droplets:
            if "active" in droplet.status:
                droplet_info(droplet)
        print "#################################"
        name = raw_input("Name of Droplet to Shutdown: ")
        print "Shutting down", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                droplet.shutdown()
                print "Droplet", name, "successfully shutdown"
                
    elif (choice == "2"):
        for droplet in droplets:
            if "active" in droplet.status:
                droplet_info(droplet)
        print "#################################"
        name = raw_input("Name of Droplet to Restart: ")
        print "Restarting", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                droplet.power_cycle()
                print "Droplet", name,"succesfully restarted"

    elif (choice == "3"):
        for droplet in droplets:
            if "off" in droplet.status:
                droplet_info(droplet)
        print "#################################"
        name = raw_input("Name of Droplet to Boot: ")
        print "Booting", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                droplet.power_on()
                print "Droplet", name, "successfully booted"
                print "Droplet", name," succesfully restarted"
    else:  
        print "\nInvalid Choice!"
    
    raw_input("Press Enter to Continue...")
    menu(manager)

def createDroplets():
    createDropletsMenu(droplets)

def createDropletsMenu():
    print "\n#################################\n"
    choice = raw_input("Number of Droplets to Create: ")
    if choice == "1":
        name = raw_input("Name of Droplet: ")
        print "#################################"
        print "Regions"
        print "1) New York"
        print "2) Amsterdam"
        print "3) San Francisco"
        print "4) Singapore"
        print "5) London"
        print "6) Frankfurt"
        print "7) Toronto"
        region = raw_input("Region to Use: ")
        if region == "1":
            region = "nyc3"
        if region == "2":
            region = "ams3"
        if region == "3":
            region = "sfo1"
        if region == "4":
            region = "sgp1"
        if region == "5":
            region = "lon1"
        if region == "6":
            region = "fra1"
        if region == "7":
            region = "tor1"
        print "#################################"
        print "Images"
        print "1) Ubuntu 14 x32"
        print "2) Ubuntu 14 x64"
        print "3) FreeBSD 10.2"
        print "4) Fedora 23 x64"
        print "5) Debian 8.2 x32"
        print "6) Debian 8.2 x64"
        print "7) CoreOS 884"
        print "8) CentOS 7.1 x64"
        image = raw_input("Image to Use: ")
        if image == "1"):
        if image == "1"):
        if image == "1"):
        if image == "1"):
        if image == "1"):
        if image == "1"):
        if image == "1"):
        if image == "1"):
def destroyDroplets(manager):
    0
def listImages(manager):
    0
def advancedMenu(manager):
    0

if __name__ == "__main__":
    checkSetup()
    manager = initManager()
    menu(manager)

