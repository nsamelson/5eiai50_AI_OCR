import os
import shutil

# source directory
src_dir = "backend/input/testDigits/"

# destination directory
dst_dir = "backend/input/testAllTogether/"

# prefix to be added to the new filenames
# prefix = "2"

# number of files to copy
num_files = 20

# loop through the range of numbers
for i in range(num_files):
    # construct the full filepaths of the source and destination files
    src_file = os.path.join(src_dir, f"{i+1}.png")
    dst_file = os.path.join(dst_dir, f"{i+41}.png")

    # copy the file from the source to the destination
    shutil.copy(src_file, dst_file)