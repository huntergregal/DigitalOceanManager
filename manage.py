#!/usr/bin/python
'''
Author: Hunter Gregal

Requires "pip install dopy"

'''
from dopy.manager import DoManager
import argparse

#Configuration
api_token = ""
droplets_suffix = "CNIS-"
ssh_key_id = ""

#Define argument options
parser = argparse.ArgumentParser(description="A Digital Ocean Droplet Manager.")
parser.add_argument('-n', '--number', nargs=1, default=False, help='number of droplets to create')

parser.add_argument('-d', '--destroy', action='store_true', help='destroy all droplets created by this manager')
args = parser.parse_args()

#Prepare API
do = DoManager(None, api_token, api_version=2)

#If Both Arguments
if args.number and args.destroy:
    print "You cannot destroy and create droplets! Choose only -n OR -d"
    exit()

#If number specified, create droplets with ssh-key
if args.number:
    i = 0
    while i < int(args.number[0]):
        name = droplets_suffix + str(i)
        do.new_droplet(name, '512mb', 'lamp', 'nyc1', ssh_key_ids=ssh_key_id)
        i += 1

#If -d, destroy all droplets with suffix
if args.destroy:
    droplets = do.all_active_droplets()
    for droplet in droplets:
        name = droplet.get("name")
        if droplets_suffix in name:
            droplet_id = str(droplet.get("id"))
            do.destroy_droplet(droplet_id)

