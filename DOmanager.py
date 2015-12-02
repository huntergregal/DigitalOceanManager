#!/usr/bin/python

'''
Author: Hunter Gregal

Requires: python-digitalocean
pip install -U python-digitalocean
'''
import argparse
import digitalocean as do
import os, sys

#Define argument options
parser = argparse.ArgumentParser(description="A Digital Ocean Droplet Manager.")
parser.add_argument('-n', '--number', nargs=1, default=False, help='number of droplets to create')

parser.add_argument('-d', '--destroy', action='store_true', help='destroy all droplets created by this manager')
args = parser.parse_args()

def initManager(secretToken):
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
            print "Please setup your Digital Ocean API token to continue...")
            sys.exit(0)
def menu():
    print "\n#################################\n"
    print "Welcome to the Digital Ocean Manager!\n Please choose an option number below\n"
    print "#################################\n"

    print "1) List Droplets (All, Running, Off)\n"
    print "2) Droplets Power Control (Shutdown, Restart, Boot)\n"
    print "3) Create Droplets (Single, Multi)\n"
    print "4) Destroy Droplets (Single, Multi)\n"
    print "5) List Images (Snapshots, Backups)\n"
    print "6) Advanced Droplet Management (Snapshots, Backups, Reset Root Password)\n"
    print "#################################\n"

