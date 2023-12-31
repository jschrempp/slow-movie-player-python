#!/bin/bash
# script to make running the slow movie player easier
#
# EDIT THIS FILE to 
#    1. replace {your user}  and  {your slow movie location}
#    2. put command line arguments to suit your intent
#
# Remember to give this file execute permission
#    chmod +x smp.sh
#
cd /home/{your user}/{your slow movie location}
source /home/{your user}/{your slow movie location}/.venv/bin/activate
python slow-movie.py Test-2s.mp4 --debug --delay 1