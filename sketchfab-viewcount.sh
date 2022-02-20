#!/bin/bash
# counts the number of views on a single Sketchfab page

temp_dir='/tmp/' # set a temporary directory to store the downloaded page

page_to_dl=$1 # store the input passed to the script in the variable $page_to_dl

cd $temp_dir # move into the temporary directory (to keep things tidy)
wget -q $page_to_dl -O temp_page.html # download the given page, and name it temp_page.html . We use -q to perform this silently.

# replace all instance of "<div" with "\n<div" (<div preceded by a newline):
sed -i 's/<div/\n/g' temp_page.html

# get the line that includes the phrase "icon-eye-icon" and spit it out into its own file:
grep 'icon-eye-icon' temp_page.html > views_line

# this gives you something like this:
# class="icon custom-icons icon-eye-icon"></div><span class="count">3.2k</span>

# now cut everything before "count"> in that file:
sed -i 's/.*"count">//g' views_line

# this gives you something like this: 3.2k</span>

# now cut the word “</span>” (you need to escape / with \):
sed -i 's/<\/span>//g' views_line

# finally, we cat views_line to standard out:
cat views_line

# and delete the temporary files.
rm views_line
rm temp_page.html
