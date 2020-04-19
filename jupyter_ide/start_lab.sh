#!/bin/bash
git config --global user.email $GITUSEREMAIL
git config --global user.name $GITUSERNAME
git config --global credential.helper store

echo "JupyterLab is now running. Go to localhost:8888 and enter 'hallo'"
conda run -n jupyter jupyter lab --ip=* --port=8888