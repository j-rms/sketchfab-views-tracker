#!/bin/bash
# SKETCHFAB VIEWS TRACKER: tracks the number of views for model pages on Sketchfab

# 2 VARIABLES THAT YOU MUST CONFIGURE:
pages_to_watch="/home/joel/projects/sketchfab-views-tracker/pages-to-watch.txt" # the location of the pages_to_watch file
data_dir="/home/joel/projects/sketchfab-views-tracker/data/"                    # the location where you want the data to end up:

# touch "$pages_to_watch" # create the pages_to_watch file, in case it does not already exist
mkdir -p $data_dir  # make the data directory, if it does not already exist.
date=$(date +%F-%R) # get exact date in format YYYY-MM-DD-HH:SS

function get_viewcount_from_page {
    page_to_dl=$1                                    # store the input passed to the script in the variable $page_to_dl
    wget -q $page_to_dl -O temp_page.html            # download the given page, and name it temp_page.html. Use -q to perform this silently.
    sed -i 's/<div/\n/g' temp_page.html              # chop the page up into greppable lines by replacing all instances of "<div" with "\n<div" (i.e. <div preceded by a newline):
    grep 'icon-eye-icon' temp_page.html > views_line # get the line that includes the phrase "icon-eye-icon" and spit it out into its own file, which will contain something like: class="icon custom-icons icon-eye-icon"></div><span class="count">3.2k</span>
    sed -i 's/.*"count">//g' views_line              # cut everything before "count"> in that file. This gives you something like: 3.2k</span>
    sed -i 's/<\/span>//g' views_line                # cut the word “</span>” (you need to escape / with \), to give just the view count:
    number_of_views=$(cat views_line)                # store the view count in a global variable:
    rm views_line                                    # finally, delete the temporary files.
    rm temp_page.html
}

function write_updated_viewcount {
    page_to_update=$1
    file_to_update=$(echo "$page_to_update" | sed -e 's/https:\/\/sketchfab.com\/3d-models\///g')  # turn the page_to_update into a usable file name
    file_to_update=${file_to_update}.txt
    touch $file_to_update  # create the file if it doesn't exist:
    get_viewcount_from_page $page_to_update
    line_to_add="$date $number_of_views"
    echo "$line_to_add    $file_to_update"
    echo $line_to_add >> $file_to_update
}

cd $data_dir
while read line; do write_updated_viewcount "$line"; done < $pages_to_watch

# generate daily view counts org file:
python3 /home/joel/projects/sketchfab-views-tracker/data-reading.py > /home/joel/projects/sketchfab-views-tracker/daily-views-report.org
ex -s -c '5,$ sort|x' /home/joel/projects/sketchfab-views-tracker/daily-views-report.org # sort the relevant portion of the report (from line 5 onward) in alphabetical order
