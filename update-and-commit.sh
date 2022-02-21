#!/bin/bash
# Get the data for all the Sketchfab model pages being tracked, then commit and push.

# set the project directory:
project_directory="/home/joel/projects/sketchfab-views-tracker/"

cd $project_directory
./sketchfab-views-tracker.sh
cd data
git add *.txt
cd ..
git commit -a -m "Automated fetch and commit of views data."
git push
