#!/usr/bin/python
import os, re, sys

delete = re.escape(input("Regex for album art to delete (press Enter to skip): "))
rename_find = re.escape(input("Regex for album art to rename: "))
rename_to = input("Rename album art to: ")

if delete == "":
	delete = False

# Process all files by directory
for i in range(1, len(sys.argv)):
	# Process passed argument
	if os.path.isdir(sys.argv[i]):
		this_dir = sys.argv[i]
		# Process all files by directory, if any, and recurse subdir
		for dirpath, dirnames, filenames in os.walk(this_dir):
			for filename in filenames:
				if delete:
					if re.search(delete, filename):
						os.unlink(os.path.normpath(dirpath + os.sep + filename))
				if re.search(rename_find, filename):
					os.rename(os.path.normpath(dirpath + os.sep + filename), os.path.normpath(dirpath + os.sep + rename_to))

sys.exit(0)