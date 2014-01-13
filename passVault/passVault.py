#! /usr/bin/python

""" file must be in the format account:pass """

# TODO use configparser to get the path for the cyphertext
# TODO convert to python 3 using 2to3
# TODO see if you need to make the options mutually exclusive or you can run them together

import subprocess
import argparse
from sys import exit
import os
import re
from os import SEEK_SET
import pyperclip
import signal
import ConfigParser

a='gpg encryption failed:please try again'
location = None
user = None

try:
    config = ConfigParser.RawConfigParser()
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '../lib/Vault.conf')
    config.read(file_path)
    location = config.get('directory', 'encrypt-dir')
    user = config.get('directory', 'user')
except Exception as e:
    exit("ensure password file location is present in PassVault/lib/Vault.conf (encrypt-dir: location)")

parser=argparse.ArgumentParser()
parser.add_argument('-a', help="view account details, copy password to clipboard", metavar='account', dest='account')
parser.add_argument('-s', help="see all account names", dest='see', action='store_true')
parser.add_argument('-n', help="add new account record. Add a '.' to leave a parameter blank and quotes to allow spaces between an argument", dest='new', metavar=('account', 'username', 'password'), nargs=3)
parser.add_argument('-d', help="delete account record(s)", dest='remove', metavar='account', nargs='+')
parser.add_argument('-m', help="modify account record. Arguments should be: account [a=new_account] [u=new_user] [p=new_password]", dest='change', metavar=('account', 'a=new_account', 'u=new_user', 'p=new_password'), nargs=4)
args=parser.parse_args()

def decrypt():
    try:
        global a
        out = subprocess.Popen(['gpg', '-a', '-d', location], stdout=subprocess.PIPE)
        a = out.communicate()[0]
    except Exception as e:
        print e

def decryptToFile():            # decrypt to file tmp
    try:
        subprocess.call(['gpg', '-ao', 'tmp', '-d', location])
    except Exception as e:
        print e

def encrypt():
    try:
        subprocess.call(['gpg', '-ao', location, '-esr', user, 'tmp'])
    except Exception as e:
        print e

def delete():
    try:
        os.remove('tmp')
    except OSError:
        exit()

def add():
    for i,val in enumerate(args.new):                   # you can enter a '.' as a placeholder for a blank value
        if val.rstrip() == '.':
            args.new[i] = ''
    line = ' '.join(args.new).replace(' ', ':').rstrip()
    # print line
    decryptToFile()
    with open('tmp', 'a+') as f:
        f.seek(0, SEEK_SET)
        for l in f.readlines():
            if l.split(':')[0].rstrip() == args.new[0]:
                f.close()
                delete()
                exit("account %s already present" % args.new[0])
        f.write(line + "\n")
    encrypt()
    delete()

def remove():
    try:
        decryptToFile()
        with open('tmp') as f:          # open file for reading
            lines = f.readlines()
        for removable in args.remove:
            for i,line in enumerate(lines):
                if line.split(':')[0].rstrip() == removable:
                    del lines[i]
                    break

        with open('tmp', 'w') as f:     # write to new file excluding deleted line
            for newline in lines:
                f.write(newline)
        encrypt()
        delete()
    except Exception as e:
        print e

def confirm():
    response = raw_input("continue (y/n)? ")
    if response.lower() != "y":
        delete()
        exit("aborting")
    else:
        return True

def modify(m, byte):
    linelist=None
    try:
        decryptToFile()
        with open('tmp') as f:                                  # save decrypted file
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.split(':')[0].rstrip() == m.group(1).rstrip():      # change to: if input = password etc, current record = ...
                linelist = line.split(':')
                if byte == 1:
                    print "changing account %s to: %s" % (linelist[0], m.group(3))
                    if confirm():
                        linelist[0] = m.group(3)
                        lines[i] = ':'.join(linelist)
                elif byte == 2:
                    print "changing user %s to: %s" % (linelist[1], m.group(5))
                    if confirm():
                        linelist[1] = m.group(5)
                        lines[i] = ':'.join(linelist)
                elif byte == 3:
                    print "changing account %s to: %s" % (linelist[0], m.group(3))
                    print "changing user %s to: %s" % (linelist[1], m.group(5))
                    if confirm():
                        linelist[0] = m.group(3)
                        linelist[1] = m.group(5)
                        lines[i] = ':'.join(linelist)
                elif byte == 4:
                    print "changing password %s to: %s" % (linelist[2], m.group(7))
                    if confirm():
                        linelist[2] = m.group(7)
                        lines[i] = ':'.join(linelist)
                elif byte == 5:
                    print "changing account %s to: %s" % (linelist[0], m.group(3))
                    print "changing password %s to: %s" % (linelist[2], m.group(7))
                    if confirm():
                        linelist[0] = m.group(3)
                        linelist[2] = m.group(7)
                        lines[i] = ':'.join(linelist)
                elif byte == 6:
                    print "changing user %s to: %s" % (linelist[1], m.group(5))
                    print "changing password %s to: %s" % (linelist[2], m.group(7))
                    if confirm():
                        linelist[1] = m.group(5)
                        linelist[2] = m.group(7)
                        lines[i] = ':'.join(linelist)
                elif byte == 7:
                    print "changing account %s to: %s" % (linelist[0], m.group(3))
                    print "changing user %s to: %s" % (linelist[1], m.group(5))
                    print "changing password %s to: %s" % (linelist[2], m.group(7))
                    if confirm():
                        linelist[0] = m.group(3)
                        linelist[1] = m.group(5)
                        linelist[2] = m.group(7)
                        lines[i] = ':'.join(linelist)
                else:
                    delete()
                    exit("error in modification")
        if not linelist:                                               # if account to modify is not in vault, exit
            delete()
            exit("%s not found in vault" % m.group(1))

        with open('tmp', 'w') as f:                             # persist changes to tmp file to be re-encrypted
            for newline in lines:
                f.write(newline)
        encrypt()
        delete()
    except Exception as e:
        print e

def main():
    if args.new:
        add()

    if args.remove:
        remove()

    if args.change:
        byte = 0
        comp = re.compile("(\S+)(\sa=(?P<a>\S+))?(\su=(?P<u>\S+))?(\sp=(?P<p>\S+))?")       # this regex matches modification args in the format account a=account u=user p=password. The account user and password values are all stored in groups named a, u and p. if a user enters a= a= twice it will only take the first match
        if comp.match(' '.join(args.change)).group(0):
            m = comp.match(' '.join(args.change))
            if m.group(2): byte += 1
            if m.group(4): byte += 2
            if m.group(6): byte += 4
            if byte == 0: exit("invalid format for modification: account a=account u=user p=password")   # if the user does not specify values for account user or password input should be rejected
        else: exit("invalid format for modification: account a=account u=user p=password")
        modify(m, byte)

    if args.see:
        decrypt()
        print "\n\033[4maccounts:\033[m"
        sorted = [s for s in a.rstrip().split('\n')]
        sorted.sort()
        for acc in sorted:
            print acc.split(':')[0]

    if args.account:
        decrypt()
        for line in a.rstrip().split('\n'):
            tmpline = line.split(':')
            if args.account == tmpline[0]:
                try:
                    if line.split(':')[1] != '':
                        print "\naccount: %s\nusername: %s" % (args.account, line.split(':')[1])
                    else:
                        print "\naccount: %s\nusername: -" % args.account
                    pyperclip.copy(line.split(':')[2])
                except Exception as e:
                    print e

def interupt(signal, frame):
    delete()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, interupt)
    main()
