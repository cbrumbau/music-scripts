#!/usr/bin/python
import os, re, subprocess, sys, time

adb = r"D:\Utilities\adb.exe"
ignore_dirs = ["scans"]
ignore_extensions = [".jpg", ".jpeg", ".png"]
exception_files = ["AlbumArt.jpg"]
path_match_regex = re.escape("Music")
music_path = "Music"
sd_card = "/storage/sdcard0"

# startupinfo = None
# if sys.platform == 'win32':
    # startupinfo = subprocess.STARTUPINFO()
    # startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Prepare and start ADB server
subprocess.Popen([adb, 'kill-server']).communicate()
subprocess.Popen([adb, 'start-server'])
time.sleep(5) # let the ADB server start

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
			retained_path = "/".join(dirpath.split(os.sep)[match_num+1:])
			# Check individual files
			for filename in filenames:
				# If not exception file, ignore by file extension
				if not any(filename in exception for exception in exception_files):
					if any(os.path.splitext(filename)[1].lower() == ignored for ignored in ignore_extensions):
						continue
				# Add file to ADB push list, retain directory structure
				filelist.append((os.path.normpath(dirpath + os.sep + filename), sd_card + "/" + music_path + "/" + retained_path + "/" + filename))
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
		retained_path = "/".join(dirpath.split(os.sep)[match_num+1:])
		# If not exception file, ignore by file extension
		if not any(sys.argv[i] in exception for exception in exception_files):
			if any(os.path.splitext(sys.argv[i])[1].lower() in ignored for ignored in ignore_extensions):
				continue
		# Add file to ADB push list, retain directory structure
		filelist.append((sys.argv[i], sd_card + "/" + music_path + "/" + retained_path + "/" + filename))
	# ADB push files to device
	if len(filelist) > 0:
		for (source, dest) in filelist:
			command = [adb, 'push', '"' + source + '"', '"' + dest + '"']
			sys.stderr.write("\n" + " ".join(command) + "\n")
			subprocess.Popen(' '.join(command)).communicate()

# Stop ADB server
subprocess.Popen([adb, 'kill-server']).communicate()
