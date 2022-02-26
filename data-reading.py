import os

data_directory = '/home/joel/projects/sketchfab-views-tracker/data/'
os.chdir(data_directory)

def make_object_dictionary(filename):
    "receive local views data filename; return object dictionary"
    # local functions:
    def read_viewnums_file(filename):
        "receive local filename containing views data; return a list of the file's lines"
        file_data = open(filename, 'r')
        lines = file_data.readlines()
        return lines
    def rewrite_viewnums_list(viewnums_lines):
        "receive output of read_viewnums_file; return a list of items having the format [[year,month,day,time],views]"
        rewritten_viewnums_list = []
        for item in viewnums_lines:
            separate_date_from_viewnums = item.split()
            separate_date_from_viewnums[0] = separate_date_from_viewnums[0].split('-')
            rewritten_viewnums_list.append(separate_date_from_viewnums)
        return rewritten_viewnums_list
    def get_object_name(filename):
        "receive local data filename; return name of the object"
        split_filename = filename.split('-')
        object_name_without_hash_dot_txt = split_filename[:-1]
        rejoined_object_name = " ".join(object_name_without_hash_dot_txt)
        return rejoined_object_name
    # building the object dictionary using the local functions:
    object_views_by_date = rewrite_viewnums_list(read_viewnums_file(filename))
    object_name = get_object_name(filename)
    object_dictionary = {'name': object_name, 'views_by_date': object_views_by_date}
    return object_dictionary

def make_daily_object_dictionary(object_dictionary):
    "take an object dictionary; return a daily object dictionary (i.e. one with one view count per day)"
    daily_views_list=[]
    # local functions:
    def make_number(number_string):
        "take a views number string; return an integer, interpretating the k abbreviation correctly"
        if 'k' in number_string:
            number_string = number_string.replace('k','')
            number = int(float(number_string) * 1000)
        else:
            number = int(number_string)
        return number

    def date_as_number(date_string):
        "take a date string; return an integer"
        return int(''.join(date_string.split('-')))
    # operations:
    for entry in object_dictionary['views_by_date']:
        day_date = '-'.join(entry[0][:-1])
        views = entry[1]
        daily_views_list.append([day_date, make_number(views)])

    cleaned_daily_views_list = []
    last_date = daily_views_list[0][0]
    last_date_as_number = date_as_number(daily_views_list[0][0])
    last_viewcount = daily_views_list[0][1]
    for entry in daily_views_list[1:]:
        this_date_as_number = date_as_number(entry[0])
        if this_date_as_number > last_date_as_number:
            cleaned_daily_views_list.append([last_date, last_viewcount])
        last_date_as_number = this_date_as_number
        last_date = entry[0]
        last_viewcount = entry[1]

    new_dictionary = {'name': object_dictionary['name'],
                      'views_by_date': cleaned_daily_views_list}
    return new_dictionary




tracked_pages=os.listdir('.') # read the local directory's contents into a list.
list_of_object_dictionaries = []
for page in tracked_pages:
    list_of_object_dictionaries.append(make_object_dictionary(page))


daily_object_dictionaries = []
for object in list_of_object_dictionaries:
    daily_object_dictionaries.append(make_daily_object_dictionary(object))

print("#+title: Daily report of LivAncWorlds' Sketchfab models' view count", end='\n')
print("NOTE: VIEW COUNTS OVER 1000 ARE ACCURATE TO 2 SIGNIFICANT FIGURES", end='\n')
print("", end='\n')
print("| *object* | *view counts* |")
for object in daily_object_dictionaries:
    pretty_views = ""
    for view in reversed(object['views_by_date']):
        pretty_views = pretty_views + view[0] + ": " + str(view[1]) + "   "
    print("|", object['name'], "|", pretty_views, "|")
