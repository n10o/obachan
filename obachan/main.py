#!/usr/bin/python
from subprocess import call
import os
import sys
import argparse
import json
#from passlib.hash import sha512_crypt
import string
import random
from getpass import getpass

LISTFILE = "userlist.json"
ANSIBLE = ["ansible-playbook", "-i", "hosts", "task.yml"]
TOPELEM = "userlist"

### User attribute definition
NAME = "name"
UID = "uid"
GROUP = "group"
GROUPS = "groups"

def add(args):
    user = makeUserDict(args)
    # TODO makepwd("pwd") pattern
#    pwds = makePwd()
    #password = getpass()

#    print pwds

    userjson = {}
    if os.path.exists(LISTFILE):
       # if exist file, append it
       with open(LISTFILE) as f:
           userjson = json.load(f)
           # TODO save order
           # if use add command and exist same name, it means modify
           if existName(user["name"], userjson):
               modify(args)
               return 0
           else:
               userjson["userlist"].append(user)
    else:
        # if NOT exist file, create new one
        userjson["userlist"] = [user]
    dumpJson(userjson, LISTFILE)
    print "added:" + args.name[0]

# if argument is None, make random password
def makePwd(pwd=None):
    if pwd is None:
        pwd = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
    return {"pwd" : pwd, "encryptpwd" : sha512_crypt.encrypt(pwd)}

def makeUserDict(args):
    name = args.name[0]
    user = {"name" : name}
    if args.uid: user["uid"] = args.uid[0]
    if args.group: user["group"] = args.group
    if args.groups: user["groups"] = args.groups
    return user

def existName(name, json):
    for user in json["userlist"]:
        if user["name"] == name:
            return True
    return False

def list(args):
    with open(LISTFILE) as f:
        userjson = json.load(f)
        for info in userjson["userlist"]:
            # TODO use ordereddict
            output = "name:" + info["name"]
            if info.get("uid"): output += " uid:" + str(info["uid"])
            if info.get("group"): output += " group:" + info["group"]
            if info.get("groups"): output += " groups:" + info["groups"]
            print output

def modify(args):
    name = args.name[0]
    userlist = []
    with open(LISTFILE) as f:
        userjson = json.load(f)
        isExist = False
        for user in userjson["userlist"]:
            if user["name"] == name:
                ## Can use createDict
                if args.uid: user["uid"] = args.uid[0]
                if args.group: user["group"] = args.group
                if args.groups: user["groups"] = args.groups
                print "modified:" + name
                isExist = True
            userlist.append(user)
        userjson = {"userlist":userlist}
        if isExist is False:
            return 1
        dumpJson(userjson, LISTFILE)

def remove(args):
    with open(LISTFILE) as f:
        userjson = json.load(f)
        isDelete = False 
        for user in userjson["userlist"]:
            name = args.name[0]
            if user["name"] == name:
                print "deleted:" + name
                isDelete = True
                break
        # Remove target user
        userlist = [u for u in userjson["userlist"] if u.get('name') != name]
        userjson = {"userlist" : userlist}
        dumpJson(userjson, LISTFILE)
        if isDelete is False:
            return 1

def execute(args):
    ANSIBLE.append("--check") # TODO Remove this
    call(ANSIBLE)

def check(args):
    call(ANSIBLE + ["--check"])

def dumpJson(content, filename):
    with open(filename, 'w') as f:
        json.dump(content, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='User manage CUI tool for multiple hosts')
    subparsers = parser.add_subparsers(help='Available sub commands')
    parser_add = subparsers.add_parser('add', help='Add user')
    parser_add.add_argument('name', help='Set name', nargs=1)
    parser_add.add_argument('-u', '--uid', nargs=1, type=int, help='Set User ID')
    parser_add.add_argument('-g', '--group', help='Group')
    parser_add.add_argument('-G', '--groups', help='Groups')
    parser_add.set_defaults(func=add)
    
    parser_list = subparsers.add_parser('list', help='List users')
    parser_list.set_defaults(func=list)
    
    parser_modify = subparsers.add_parser('modify', help='Modify user info')
    parser_modify.add_argument('name', help='Set name', nargs=1)
    parser_modify.add_argument('-u', '--uid', nargs=1, type=int, help='Set User ID')
    parser_modify.add_argument('-g', '--group', help='Group')
    parser_modify.add_argument('-G', '--groups', help='Groups')
    parser_modify.set_defaults(func=modify)
    
    parser_remove = subparsers.add_parser('remove', help='Remove user')
    parser_remove.add_argument('name', help='Set name', nargs=1)
    parser_remove.set_defaults(func=remove)
    
    parser_check = subparsers.add_parser('check', help='Check result')
    parser_check.set_defaults(func=check)
    
    parser_exec = subparsers.add_parser('exec', help='Execute user manage')
    parser_exec.set_defaults(func=execute)
    
    args = parser.parse_args()
    return args.func(args)

if __name__ == '__main__':
    sys.exit(main())
