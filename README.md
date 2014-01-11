PassVault
=========

command line python tool for managing your passwords using pgp
encryption

Allows you to:
- create and store encrypted account/username/password combinations
- add, delete and modify entries
- view account details, with the password copied to your clipboard
  for privacy and usability

Platforms
----------

Linux / MacOS

Issues
-------

CentOS has problems generating pgp keys as a non-root user, you may have to generate keys and
use the application as root

Dependencies
-------------

python 2.x (not tested for python 3)

gpg

pyperclip (pip install pyperclip) - install pip using your system's
default package installer if not already present on your system

xclip (linux only)

Setup
-----
run 'git clone https://github.com/riklas/PassVault' to pull files from
github

1. cd to the bin dirctory

2. run passVaultSetup.sh to set up your environment 

3. The encypted version of your password file will have a suffix of -enc

Usage
-----

Run passVault.py -h for details on usage flags once you have been set
up.

Other files
-----------

a Vault.conf file will be created to hold config data for the vault.
Use this file to change the directory location of the encrypted password
file and the user who will be signing on encrpytion

Disclaimer
----------
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
