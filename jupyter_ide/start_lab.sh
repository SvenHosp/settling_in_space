#!/bin/bash
echo "Enter git user E-Mail:"
read -s gituseremail
echo "Enter git user name:"
read -s gitusername
git config --global user.email $gituseremail
git config --global user.name $gitusername
git config --global credential.helper store

echo "JupyterLab is now running. Go to localhost:8888 and enter 'hallo'"
conda run -n jupyter jupyter lab --ip=* --port=8888