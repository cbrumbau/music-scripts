#!/usr/bin/python
import os, re, subprocess, sys, time

copy_exe = r"C:\Program Files\TeraCopy\TeraCopy.exe"
copy_command = "Copy"
music_path = r"F:\MUSIC"
ignore_dirs = ["scans"]
ignore_extensions = [".jpg", ".jpeg", ".png"]
exception_files = ["AlbumArt.jpg"]
path_match_regex = re.escape("Music")
info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 6

for i in range(1, len(sys.argv)):
	filelist = []
	# Recursively check target directory for valid files to copy, generate file and destination array
	if os.path.isdir(sys.argv[i]):
		this_dir = sys.argv[i]
		# Process all files by directory, if any, and recurse subdir
		for dirpath, dirnames, filenames in os.walk(this_dir):
			this_dir = dirpath.split(os.sep)[-1]
			# Skip ignored directories
			if any(this_dir.lower() in ignored for ignored in ignore_dirs):
				continue
			# Locate path match regex to determine destination directory
			match_num = 0
			for (num, dirname) in enumerate(dirpath.split(os.sep)):
				if re.search(path_match_regex, dirname):
					match_num = num
					break
			retained_path = os.sep.join(dirpath.split(os.sep)[match_num+1:])
			# Check individual files
			for filename in filenames:
				# If not exception file, ignore by file extension
				if not any(filename in exception for exception in exception_files):
					if any(os.path.splitext(filename)[1].lower() == ignored for ignored in ignore_extensions):
						continue
				# Add file to push list, retain directory structure
				filelist.append((os.path.normpath(dirpath + os.sep + filename), music_path + os.sep + retained_path + os.sep))
	# Check if is a file
	elif os.path.isfile(sys.argv[i]):
		dirpath = os.path.dirname(sys.argv[i])
		filename = os.path.basename(sys.argv[i])
		# Locate path match regex to determine destination directory
		match_num = 0
		for (num, dirname) in enumerate(dirpath.split(os.sep)):
			if re.search(path_match_regex, dirname):
				match_num = num
				break
		retained_path = os.sep.join(dirpath.split(os.sep)[match_num+1:])
		# If not exception file, ignore by file extension
		if not any(sys.argv[i] in exception for exception in exception_files):
			if any(os.path.splitext(sys.argv[i])[1].lower() in ignored for ignored in ignore_extensions):
				continue
		# Add file to ADB push list, retain directory structure
		filelist.append((sys.argv[i], music_path + os.sep + retained_path + os.sep))
	# Check if folder(s) already exists, otherwise make new folder
	sys.stderr.write("Generating folders for files if required...\n")
	for (source, dest) in filelist:
		if not os.path.exists(dest):
			os.makedirs(dest)
	# Copy pushed files to device
	sys.stderr.write("Copying files to device...\n")
	if len(filelist) > 0:
		for (source, dest) in filelist:
			command = '"' + copy_exe + '" ' + copy_command + ' "' + source + '" "' + dest + '" /Close'
			# sys.stderr.write("\n" + " ".join(command) + "\n")
			# subprocess.Popen(command).communicate()
			subprocess.Popen(command, startupinfo=info)

sys.exit(0)
