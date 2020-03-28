#!/bin/bash
echo "JupyterLab is now running. Go to localhost:8888 and enter 'hallo'"
conda run -n jupyter jupyter lab --ip=* --port=8888