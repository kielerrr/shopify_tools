# Add hints to every .liquid page indicating where template starts and ends
# Place in root directory of theme
# Creates own backup in parent directory of project
# Create your own backups before using this tool!
# add = 1 //add hint lines
# remove = 1 //remove hint lines
# 2021 Ryan Kiel
# https://github.com/kielerrr/shopify_tools

import os
import zipfile
import random
import re

SEARCH_DIR = '.'
BACKUP_DIR = '../'
add = 1
remove = 0


def get_list_of_files(starting_dir):
    list_of_files = os.listdir(starting_dir)
    all_files = []
    for entry in list_of_files:
        full_path = os.path.join(starting_dir, entry)
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            if '.liquid' in full_path:
                all_files.append(full_path)

    return all_files


def remove_lines(file_before):
    file = open(file_before, 'r')
    file_text = file.read()
    text_fixed = re.sub('#####KV.*#####KV<br \/>', '', file_text)
    file.close()
    file_fixed = open(file_before, 'w')
    file_fixed.write(text_fixed)
    file_fixed.close()


def add_lines(file_before):
    colors = ['red', 'blue', 'green', 'purple']
    text_color = random.choice(colors)
    start = f'\n#####KV <div style="color: {text_color}">##### START {str(file_before)} START #####</div>#####KV<br />\n'
    end = f'\n#####KV <div style="color: {text_color}">##### END {str(file_before)} END #####</div>#####KV<br />\n'
    loaded_file = open(file_before, 'r')
    loaded_file_content = loaded_file.read()
    loaded_file.close()
    file_fixed = open(file_before, 'w')
    text_fixed = start + loaded_file_content + end
    file_fixed.write(text_fixed)
    file_fixed.close()

    return bool(file_fixed)


def main():
    zf = zipfile.ZipFile(f'{BACKUP_DIR}theme_backup.zip', 'w')
    list_of_files = []
    for (dirpath, dirnames, filenames) in os.walk(SEARCH_DIR):
        list_of_files += [os.path.join(dirpath, file) for file in filenames]

    # Print the files
    for elem in list_of_files:
        zf.write(elem)
        print(elem)
    zf.close()

    list_of__liquid_files = get_list_of_files(SEARCH_DIR)
    # Print the files
    for elem in list_of__liquid_files:
        try:
            if add:
                add_lines(elem)
            if remove:
                remove_lines(elem)
        except:
            print('not a text file')


if __name__ == '__main__':
    main()
    
   
