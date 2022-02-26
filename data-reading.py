import os

data_directory = '/home/joel/projects/sketchfab-views-tracker/data/'
os.chdir(data_directory)

def make_object_dictionary(filename):
    "receives local views data filename; returns object dictionary"
    # local functions:
    def read_viewnums_file(filename):
        "receives local filename containing views data; returns a list of the file's lines"
        file_data = open(filename, 'r')
        lines = file_data.readlines()
        return lines
    def rewrite_viewnums_list(viewnums_lines):
        "receives output of read_viewnums_file; returns a list of items having the format [[year,month,day,time],views]"
        rewritten_viewnums_list = []
        for item in viewnums_lines:
            separate_date_from_viewnums = item.split()
            separate_date_from_viewnums[0] = separate_date_from_viewnums[0].split('-')
            rewritten_viewnums_list.append(separate_date_from_viewnums)
        return rewritten_viewnums_list
    def get_object_name(filename):
        "receives local data filename; returns name of the object"
        split_filename = filename.split('-')
        object_name_without_hash_dot_txt = split_filename[:-1]
        rejoined_object_name = " ".join(object_name_without_hash_dot_txt)
        return rejoined_object_name
    # building the object dictionary using the local functions:
    object_views_by_date = rewrite_viewnums_list(read_viewnums_file(filename))
    object_name = get_object_name(filename)
    object_dictionary = {'name': object_name, 'views_by_date': object_views_by_date}
    return object_dictionary
    
make_object_dictionary('uilleann-pipes-personal-objects-11821955acb54aa38c5ec14ae5c1eba2.txt')
