#! /bin/bash

# this setup script is used to encrypt your plaintext password file using gpg encryption. The encrypted file will then be used along with the passVault application

echo "preparing setup to encrypt your passwords"
for i in $( seq 1 3); do echo -n "."; sleep 0.5; done; echo ""

# checking if gpg exists
which gpg 1>/dev/null
if [[ $? -ne 0 ]]; then
    echo "install gpg on your system before proceeding"
    exit 1
fi

echo "now generating gpg keys. note you may need to run this script as root if the generation fails - this is an issue that has been found on CENTOS"
echo "have you previously generated gpg keys in your home directory [y/n]? " 
read answer

if [[ ${answer} =~ [nN] ]]; then
    gpg --gen-key
fi

sleep 1
echo -e "please have prepared an initial plantext password file with the following format for each line:\n account:username:password"
sleep 1
echo -e "to leave entries blank, leave them out. e.g. not specifying a username:\naccount::password"
sleep 1
echo "if you wish to start off with an empty file press enter and a temporary file will be created"

echo "what is the fully qualified location of your password file?"
read file

if [[ -z ${file} ]]; then
    echo "creating 'pas' in home directory"
    file="${HOME}/pas"
    if [[ -e ${file} ]]; then
        echo "default file pas exists. please specify a relevant file name at the prompt"
        exit 1
    fi
    touch ${file}
elif [[ ! -f ${file} ]]; then
    echo "${file} does not exist"
    echo "creating ${file}"
    mkdir -p "$(dirname ${file})"
    touch ${file}
fi

echo "enter user for encryption - this username will be used in signing the cyphertext. The gpg keys must also be generated in this user's home directory"
echo "press enter to select the current user:"

read user
if  [[ -z ${user} ]]; then
    username=$(whoami)
else
    username=${user}
fi


echo "starting encyption..."
echo "enter fully qualified destination for encrypted file (leave blank to create in same directory as plaintext):"
read dest

if [[ -z ${dest} ]]; then
    destination="${file}-enc"
elif [[ -d ${dest} ]]; then
    destination="${dest}/${file##*/}-enc"
else
    echo "invalid destination"
    exit 1
fi

echo "encrypting ${file} to target destination ${destination}"
gpg -ao ${destination} -esr ${username} ${file}

if [[ $? -eq 0 ]]; then
    echo "encryption complete"
fi

echo "writing to config file at lib/Vault.conf"
(echo "[directory]" && echo "encrypt-dir: ${destination}" && echo "user: ${username}") > ../lib/Vault.conf
echo "you can store your original password file as a backup, as new account/password additions will now get added dynamically to the cyphertext"
