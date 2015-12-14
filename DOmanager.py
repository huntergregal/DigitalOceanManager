#!/usr/bin/python

'''
Author: Hunter Gregal

A menu-based manager for a Digital Ocean Account. Manages droplets via account API token and uses the services built-in API. 

Requires: python-digitalocean
pip install -U python-digitalocean

To Suppress SSL Errors:
pip install pyopenssl ndg-httpsclient pyasn1
'''

import argparse
import digitalocean as do
import os, sys
#debug only
#from IPython import embed

#function init
def initManager():
    #get api token from file
    f = open("token.conf", "r")
    secretToken = f.readline()
    f.close()
    try:
        manager = do.Manager(token=secretToken)
    except do.Error as e:
        print "ERROR: %s" % e
        return
    #return token and socket session
    return manager,secretToken

#function setup
def setup():
    #let user add api token to file
    print "Please paste your Digital Ocean API token below"
    token = raw_input("API Token: ")
    config = open("token.conf", "w")
    config.write(token)
    config.close
    print "Digital Ocean API Token Succesfully setup!"
    return

#function setupcheck
def checkSetup():
    #check for token (empty file)
    if (os.stat("token.conf").st_size == 0):
        print "Digital Ocean API Token Not Configured."
        choice = raw_input("Would you like to configure your API token now? [y/n]: ")
        if (choice == "y" or choice == "Y"):
            setup()
        else:
            print "Please setup your Digital Ocean API token to continue..."
            sys.exit(0)
    return

#function for droplets submenu
def listDropletsMenu():
    #choose which droplets to list
    print "#################################"
    print "1) Show All Droplets"
    print "2) Show Active Droplets"
    print "3) Show Off Droplets"
    choice = raw_input("Choice: ")
    if (choice == "1"):
        listDroplets("all")
    elif (choice == "2"):
        listDroplets("active")
    elif (choice == "3"):
        listDroplets("off")
    else:  
        print "\nInvalid Choice!"
        return
    return

#function to list droplet info
def listDroplets(status,droplets=False):
    if droplets == False:
        try:
            droplets = manager.get_all_droplets()
        except do.Error as e:
            print "ERROR: %s" % e
            return
    #return droplets specified by status
    if (status == "all"):
        for droplet in droplets:
                print "#################################"
                print "Name:", droplet.name
                print "Image:", droplet.image.get("name")
                print "Region:", droplet.region.get("name")
                print "Disk:", droplet.size.get("disk")
                print "Memory:", droplet.size.get("memory")
                print "Backups:", str(droplet.backups)
                print "STATUS:", droplet.status
    elif (status == "active"):
        for droplet in droplets:
            if "active" in droplet.status:
                print "#################################"
                print "Name:", droplet.name
                print "Image:", droplet.image.get("name")
                print "Region:", droplet.region.get("name")
                print "Disk:", droplet.size.get("disk")
                print "Memory:", droplet.size.get("memory")
                print "Backups:", str(droplet.backups)
                print "STATUS:", droplet.status
    elif (status == "off"):
        for droplet in droplets:
            if "off" in droplet.status:
                print "#################################"
                print "Name:", droplet.name
                print "Image:", droplet.image.get("name")
                print "Region:", droplet.region.get("name")
                print "Disk:", droplet.size.get("disk")
                print "Memory:", droplet.size.get("memory")
                print "Backups:", str(droplet.backups)
                print "STATUS:", droplet.status
    elif (status == "backupsEnabled"):
        for droplet in droplets:
            if droplet.backups:
                print "#################################"
                print "Name:", droplet.name
                print "Image:", droplet.image.get("name")
                print "Region:", droplet.region.get("name")
                print "Disk:", droplet.size.get("disk")
                print "Memory:", droplet.size.get("memory")
                print "Backups:", str(droplet.backups)
                print "STATUS:", droplet.status
    elif (status == "backupsDisabled"):
        for droplet in droplets:
            if not droplet.backups:
                print "#################################"
                print "Name:", droplet.name
                print "Image:", droplet.image.get("name")
                print "Region:", droplet.region.get("name")
                print "Disk:", droplet.size.get("disk")
                print "Memory:", droplet.size.get("memory")
                print "Backups:", str(droplet.backups)
                print "STATUS:", droplet.status
    return

#function for powering droplets
def powerControlDroplets():
    try:
        droplets = manager.get_all_droplets()
    except do.Error as e:
        print "ERROR: %s" % e
        return
    #Power options
    print "#################################"
    print "1) Shutdown Droplets"
    print "2) Restart (PowerCycle) Droplets"
    print "3) Boot Droplets"
    choice = raw_input("Choice: ")
    #makes action on droplet
    #error checks for empty names
    if (choice == "1"):
        listDroplets("active",droplets)
        print "#################################"
        name = raw_input("Name of Droplet to Shutdown: ")
        if not name.strip():
            print "Can't Have Empty Name!"
            return
        print "Shutting down", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                try:
                    droplet.shutdown()
                except do.Error as e:
                    print "ERROR: %s" % e
                    return
                print "Droplet", name, "successfully shutdown"
    elif (choice == "2"):
        listDroplets("active",droplets)
        print "#################################"
        name = raw_input("Name of Droplet to Restart: ")
        if not name.strip():
            print "Can't Have Empty Name!"
            return
        print "Restarting", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                try:
                    droplet.power_cycle()
                except do.Error as e:
                    print "ERROR: %s" % e
                    return
                print "Droplet", name,"succesfully restarted"
    elif (choice == "3"):
        listDroplets("off",droplets)
        print "#################################"
        name = raw_input("Name of Droplet to Boot: ")
        if not name.strip():
            print "Can't Have Empty Name!"
            return
        print "Booting", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                try:
                    droplet.power_on()
                except do.Error as e:
                    print "ERROR: %s" % e
                    return
                print "Droplet", name, "successfully booted"
    else:  
        print "\nInvalid Choice!"
        return
    return

#fucntion for creating droplets submenu
def createDropletsMenu(secretToken):
    #how many droplets?
    print "#################################"
    number = raw_input("Number of Droplets to Create: ")
    if number.isdigit() == False:
        print "Please input a real number!"
        return
    #if one get its name
    name = False
    prefix = False
    if number == "1":
        name = raw_input("Name of Droplet: ")
        if not name.strip():
            print "Can't Have Empty Name!"
            return
    #if more than 1, get a suffix
    elif number > 1:
        prefix = raw_input("Prefix of droplets: ")
    #derp out
    else:
        print "Invalid number!"
        return
    #select region to use
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
    elif region == "2":
        region = "ams3"
    elif region == "3":
        region = "sfo1"
    elif region == "4":
        region = "sgp1"
    elif region == "5":
        region = "lon1"
    elif region == "6":
        region = "fra1"
    elif region == "7":
        region = "tor1"
    else:
        print "Invalid Option!"
        return
    #select image to use
    print "#################################"
    print "Images"
    print "1) Ubuntu 14 x32"
    print "2) Ubuntu 14 x64"
    print "3) FreeBSD 10 x64"
    print "4) Fedora 22 x64"
    print "5) Debian 8 x32"
    print "6) Debian 8 x64"
    print "7) CoreOS 877 beta"
    print "8) CentOS 7 x64"
    image = raw_input("Image to Use: ")
    if image == "1":
        image = "ubuntu-14-04-x32"
    elif image == "2":
        image = "ubuntu-14-04-x64"
    elif image == "3":
        image = "freebsd-10-2-x64"
    elif image == "4":
        image = "fedora-22-x64"
    elif image == "5":
        image = "debian-8-x32"
    elif image == "6":
        image = "debian-8-x64"
    elif image == "7":
        image = "coreos-beta"
    elif image == "8":
        image = "centos-7-0-x64"
    else:
        print "Invalid Option!"
        return

    #select slug_size
    print "#################################"
    print "Droplet Size"
    print "1) 512mb"
    print "2) 1gb"
    print "3) 2gb"
    print "4) 4gb"
    print "5) 8gb"
    print "6) 16gb"
    print "7) 32gb"
    print "8) 48gb"
    print "9) 64gb"
    size = raw_input("Droplet Size to Use: ")
    if size == "1":
        size = "512mb"
    elif size == "2":
        size = "1gb"
    elif size == "3":
        size = "2gb"
    elif size == "4":
        size = "4gb"
    elif size == "5":
        size = "8gb"
    elif size == "6":
        size = "16gb"
    elif size == "7":
        size = "32gb"
    elif size == "8":
        size = "48gb"
    elif size == "9":
        size = "64gb"
    else:
        print "Invalid Option!"
        return

    #backups yes/no
    print "#################################"
    print "Would you like backups enabled?"
    backups = raw_input("y/n: ")
    if backups == "y" or backups == "Y":
        backups = True
    elif backups == "n" or backups == "N":
        backups = False
    else:
        print "Invalid Option!"
        return

    #Final Confirmation
    print "#################################"
    print "!! WARNING !! ACCOUNT WILL BE CHARGED !!"
    print "#################################"
    print "You are about to create", number, "droplet(s) with the name/suffix of", name, "with the following specs:"
    print "Region:", region
    print "Image:", image
    print "Size:", size
    print "Backups:", str(backups)
    print "#################################"
    confirm = raw_input("Are you sure you want to continue? [y/n]: ")
    #if no backout
    if confirm == "n" or confirm == "N":
        return
    #if yes launch it
    elif confirm == "y" or confirm == "Y":
        #if multiple, use suffix
        if prefix:
            number = int(number)
            i = 1
            while i <= number:
                droplet = do.Droplet(token=secretToken,
                        name = prefix + "-" + str(i),
                        region = region,
                        image = image,
                        size_slug = size,
                        backups = backups)
                try:
                    droplet.create()
                except do.Error as e:
                    print "ERROR: %s" % e
                    return
                print "Droplet", str(i), "Created"
                i = i + 1
            print "Droplets successfully created!"
        if name:
            droplet = do.Droplet(token=secretToken,
                    name = name,
                    region = region,
                    image = image,
                    size_slug = size,
                    backups = backups)
            try:
                droplet.create()
            except do.Error as e:
                print "ERROR: %s" % e
                return
            print "Droplet successfully created!"
    return

#function for destroing droplets
def destroyDroplets():
    try:
        droplets = manager.get_all_droplets()
    except do.Error as e:
        print "ERROR: %s" % e
        return
    #destroy options
    print "#################################"
    print "1) Destroy a single droplet"
    print "2) Destroy multiple droplets (suffix)"
    choice = raw_input("Choice: ")
    #destroy droplet specified
    if (choice == "1"):
        listDroplets("all",droplets)
        print "#################################"
        name = raw_input("Name of Droplet to Destroy: ")
        if not name.strip():
            print "Can't Have Empty Name!"
            return
        print "!! ARE YOU SURE YOU WANT TO DESTROY DROPLET", name + "? !!"
        confirm = raw_input("[y/n]: ")
        if confirm == "y" or confirm == "Y":
            print "Destroying", name +"..."
            for droplet in droplets:
                if name == str(droplet.name):
                    try:
                        droplet.destroy()
                    except do.Error as e:
                        print "ERROR: %s" % e
                        return
                    print "Droplet", name, "successfully destroyed"
        elif confirm =="n" or confirm == "N":
            return
        else:
            print "\nInvalid Option!"
            return
    #destroy droplets with prefix
    elif (choice == "2"):
        listDroplets("all",droplets)
        print "#################################"
        name = raw_input("Suffix of Droplets to Destroy (do not include '-'): ")
        name = name + "-"
        print "!! ARE YOU SURE YOU WANT TO DESTROY DROPLETS LIKE", name + "? !!"
        confirm = raw_input("[y/n]: ")
        if confirm == "y" or confirm == "Y":
            print "Destroying Droplets LIKE", name +"..."
            for droplet in droplets:
                if name in str(droplet.name):
                    try:
                        droplet.destroy()
                    except do.Error as e:
                        print "ERROR: %s" % e
                        return
                    print "Droplet", str(droplet.name), "successfully destroyed"
        elif confirm =="n" or confirm == "N":
            return
        else:
            print "\nInvalid Option!"
            return
    else:
        print "\nInvalid Option!"
        return
    return

#function to list images
def listImages():
    try:
        images = manager.get_my_images()
    except do.Error as e:
        print "ERROR: %s" % e
        return
    i = 1
    for image in images:
        print "Image " + str(i) + ":", image.name
        i = i + 1
    return

#function to destroy images
def destroyImages():
    listImages()
    print "#################################"
    name = raw_input("Name of Image to Destroy: ")
    if not name.strip():
        print "Can't Have Empty Name!"
        return
    print "!! ARE YOU SURE YOU WANT TO DESTROY IMAGE", name + "? !!"
    confirm = raw_input("[y/n]: ")
    if confirm == "y" or confirm == "Y":
        images = manager.get_my_images()
        print "Destroying", name +"..."
        for  image in images:
            if name == str(image.name):
                try:
                    image.destroy()
                except do.Error as e:
                    print "ERROR: %s" % e
                    return
                print "Image", name, "successfully destroyed"
    elif confirm =="n" or confirm == "N":
        return
    else:
        print "\nInvalid Option!"
        return
    return

#functions to reset root of droplet
def rootReset():
    try:
        droplets = manager.get_all_droplets()
    except do.Error as e:
        print "ERROR: %s" % e
        return
    #reset options
    print "#################################"
    print "Sends new root password to email!"
    print "#################################"
    print "1) Reset Root Password on a single droplet"
    print "2) Reset Root Password on multiple droplets (suffix)"
    choice = raw_input("Choice: ")
    if (choice == "1"):
        listDroplets("all",droplets)
        print "#################################"
        name = raw_input("Name of Droplet to Root Reset: ")
        if not name.strip():
            print "Can't Have Empty Name!"
            return
        print "!! ARE YOU SURE YOU WANT TO RESET THE ROOT PASSWORD ON DROPLET", name + "? !!"
        confirm = raw_input("[y/n]: ")
        if confirm == "y" or confirm == "Y":
            print "Resetting Root on", name +"..."
            for droplet in droplets:
                if name == str(droplet.name):
                    try:
                        droplet.reset_root_password()
                    except do.Error as e:
                        print "ERROR: %s" % e
                        return
                    print "Droplet", name, "root successfully reset"
        elif confirm =="n" or confirm == "N":
            return
        else:
            print "\nInvalid Option!"
            return
    #reset root on droplets with suffix
    elif (choice == "2"):
        listDroplets("all",droplets)
        print "#################################"
        name = raw_input("Suffix of Droplets to Root Reset (do not include '-'): ")
        name = name + "-"
        print "!! ARE YOU SURE YOU WANT TO RESET THE ROOT PASSWORD ON DROPLETS LIKE", name + "? !!"
        confirm = raw_input("[y/n]: ")
        if confirm == "y" or confirm == "Y":
            print "Resetting Root on Droplets LIKE", name +"..."
            for droplet in droplets:
                if name in str(droplet.name):
                    try:
                        droplet.reset_root_password()
                    except do.Error as e:
                        print "ERROR: %s" % e
                        return
                    print "Droplet", str(droplet.name), "root successfully reset"
        elif confirm =="n" or confirm == "N":
            return
        else:
            print "\nInvalid Option!"
            return
    else:
        print "\nInvalid Option!"
        return
    return

#function to manage backups
def controlBackups():
    try:
        droplets = manager.get_all_droplets()
    except do.Error as e:
        print "ERROR: %s" % e
        return
    print "#################################"
    print "1) Enable Backups on a Droplet"
    print "2) Disable Backups on a Droplet"
    choice = raw_input("Choice: ")
    if (choice == "1"):
        listDroplets("backupsDisabled",droplets)
        print "#################################"
        name = raw_input("Name of Droplet to Enable Backups On: ")
        if not name.strip():
            print "Can't Have Empty Name!"
            return
        print "!! ARE YOU SURE YOU WANT TO ENABLE BACKUPS ON DROPLET", name + "? !!"
        confirm = raw_input("[y/n]: ")
        if confirm == "y" or confirm == "Y":
            print "Enabling backups on", name +"..."
            for droplet in droplets:
                if name == str(droplet.name):
                    try:
                        droplet.enable_backups()
                    except do.Error as e:
                        print "ERROR: %s" % e
                        return
                    print "Droplet", name, "backups successfully enabled"
        elif confirm =="n" or confirm == "N":
            return
        else:
            print "\nInvalid Option!"
            return

    elif (choice == "2"):
        listDroplets("backupsEnabled",droplets)
        print "#################################"
        name = raw_input("Name of Droplet to Disable Backups On: ")
        if not name.strip():
            print "Can't Have Empty Name!"
            return
        print "!! ARE YOU SURE YOU WANT TO DISABLE BACKUPS ON DROPLET", name + "? !!"
        confirm = raw_input("[y/n]: ")
        if confirm == "y" or confirm == "Y":
            print "Disabling backups on", name +"..."
            for droplet in droplets:
                if name == str(droplet.name):
                    try:
                        droplet.disable_backups()
                    except do.Error as e:
                        print "ERROR: %s" % e
                        return
                    print "Droplet", name, "backups successfully disabled"
        elif confirm =="n" or confirm == "N":
            return
        else:
            print "\nInvalid Option!"
            return
    else:
        print "\nInvalid Option!"
        return
    return

#function to take snpashot of droplets
def takeSnapshot():
    try:
        droplets = manager.get_all_droplets()
    except do.Error as e:
        print "ERROR: %s" % e
        return
    print "#################################"
    listDroplets("all",droplets)
    print "#################################"
    name = raw_input("Name of Droplet to Take Snapshot On: ")
    if not name.strip():
        print "Can't Have Empty Name!"
        return
    print "!! ARE YOU SURE YOU WANT TO TAKE SNAPSHOT OF DROPLET", name + "? !!"
    confirm = raw_input("[y/n]: ")
    if confirm == "y" or confirm == "Y":
        snapshotName = raw_input("Save Snapshot As The Name: ")
        print "Taking Snapshot", snapshotName, "of", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                try:
                    droplet.take_snapshot(snapshotName)
                except do.Error as e:
                    print "ERROR: %s" % e
                    return
                print "Droplet", name, "successfully Snapshotted as", snapshotName
    elif confirm =="n" or confirm == "N":
        return
    else:
        print "\nInvalid Option!"
        return
    return

#advances menu function
def advancedMenu():
    os.system("clear")
    print "#################################"
    print "Advanced Droplet Management" 
    print "#################################"
    print "1) Destroy Images"
    print "2) Reset Droplet Root Password"
    print "3) Enable/Disable Droplet Automated Backups"
    print "4) Snapshot a Droplet"
    print "5) Return to Main Menu"
    processAdvancedOptions()
    return

#process advanced menu function
def processAdvancedOptions():
    choice = ""
    choice = raw_input("Choice: ")
    if (choice == "1"):
        destroyImages()
    elif (choice == "2"):
        rootReset()
    elif (choice == "3"):
        controlBackups()
    elif (choice == "4"):
        takeSnapshot()
    elif (choice == "5"):
        return
    return

#menu function
def menu(secretToken):
    os.system("clear")
    print "#################################"
    print "Welcome to the Digital Ocean Manager!\nPlease choose an option number below"
    print "#################################"
    print "1) List Droplets (All, Running, Off)"
    print "2) Droplets Power Control (Shutdown, Restart, Boot)"
    print "3) Create Droplets (Single, Multi)"
    print "4) Destroy Droplets (Single, Multi)"
    print "5) List Images (Snapshots, Backups)"
    print "6) Advanced Droplet Management"
    print "7) Exit"
    print "#################################"
    processOptions(secretToken)
    return

#process menu function
def processOptions(secretToken):
    choice = ""
    choice = raw_input("Choice: ")
    if (choice == "1"):
        listDropletsMenu()
    elif (choice == "2"):
        powerControlDroplets()
    elif (choice == "3"):
        createDropletsMenu(secretToken)
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
    return

#manin function
if __name__ == "__main__":
    #Call checkstup function to check for api token
    checkSetup()
    #create an api session and grab the session object and token
    manager,secretToken = initManager()
    #debug mode only
    #embed()
    #loop main menu
    while True:
        menu(secretToken)
