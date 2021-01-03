#!/usr/bin/env python
# title           :organize_media_files.py
# description     :This will organize images/videos datewise.
# author          :abid.khan
# date            :20210103
# version         :1.0
# usage           :python organize_media_files.py d:\path\to\folder-containing-images-and-videos
# notes           :
# python_version  :3.7.3
# ==============================================================================

import sys
import os
import re
from PIL import Image
from PIL.ExifTags import TAGS
import shutil

# Destination path as an argument
dest = sys.argv[0]

image_file_pattern = r'(?:PANO|IMG)_(\d{4})(\d{2})(\d{2})_.*.jpg'
video_file_pattern = r'.VID_(\d{4})(\d{2})(\d{2})_.*.mp4'


def moveTo(src, dest):
    """
    This method will src & dest and move the src file to dest folder.
    Note: 'file' param has been removed from this method

    :param src:
    :param dest:
    :return:
    """
    if not os.path.exists(dest):
        # os.mkdir(dest)
        # For recursively creating directory
        os.makedirs(dest, exist_ok=True)
        print('Created destination : ', dest)

    print(src, dest)
    try:
        shutil.move(src, dest)
        # shutil.move(src, dest + "\\" + file)
        # shutil.move(src, dest, copy_function=shutil.copy2)
        # os.rename(src, dest + "/" + file)
        # os.replace(src, dest + "/" + file)
    except:
        print("Couldn't move the file. It is maybe being used by some other process.")

for subdir, dirs, files in os.walk(dest):
    for file in files:
        if file.endswith('.jpg'):
            result = re.match(image_file_pattern, file)
            if result:
                # Get the file date
                date = result.group(1) + "-" + result.group(2) + "-" + result.group(3)

                # Create image instance
                image = Image.open(os.path.join(subdir, file))
                # extract EXIF data
                exif_data = image.getexif()

                # Loop over exif data to fetch Make: property of an image
                for tag_id in exif_data:
                    # get the tag name, instead of human unreadable tag id
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'Make':
                        make_data = exif_data.get(tag_id)
                        break

                # Close image instance
                image.close()

                image_src = os.path.join(subdir, file)
                image_dest = os.path.join(subdir, make_data + "\\" + date)

                moveTo(image_src, image_dest)

        elif file.endswith('.mp4'):
            result = re.match(video_file_pattern, file)
            if result:
                # Get the file date
                date = result.group(1) + "-" + result.group(2) + "-" + result.group(3)
                video_src = os.path.join(subdir, file)
                video_dest = os.path.join(subdir, make_data + "\\vid\\" + date)

                moveTo(file, video_src, video_dest)


# reference links:
# - https://www.thepythoncode.com/article/extracting-image-metadata-in-python
# - https://www.geeksforgeeks.org/python-move-or-copy-files-and-directories/
# - https://stackoverflow.com/questions/19587118/iterating-through-directories-with-python

