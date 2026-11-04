import os
import subprocess
import logging
import datetime

MUSIC_INFO_FILE = "music_info.csv"
MUSIC_DIRECTORY = "music"
FILE_EXTENSION = "mp3"
CSV_SEPARATOR = ";"
LOG_FILE = "music_downloader.log"

def init_logging ():
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.INFO)
	stream_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
	logger.addHandler(stream_handler)

	log_file_handler = logging.FileHandler(LOG_FILE)
	log_file_handler.setLevel(logging.DEBUG)
	log_file_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
	logger.addHandler(log_file_handler)

	return logger

def program_start ():
	start_time = datetime.datetime.now()
	logger.info(f"Programm started on {start_time}")

	return start_time

def program_stop (start_time):
	stop_time = datetime.datetime.now()

	time_taken = stop_time - start_time
	time_taken_in_seconds = time_taken.total_seconds()
	(hours, minutes, seconds) = get_time_hour_minute_second(time_taken_in_seconds)

	logger.info(f"Programm stopped ! It took {hours}h, {minutes}m, {seconds}s")

def get_time_hour_minute_second (seconds):
	seconds = int(seconds)
	(hours, seconds) = divmod(seconds, 3600)
	(minutes, seconds) = divmod(seconds, 60)

	return (hours, minutes, seconds)

def line_is_valid (line):
	return (line.count(CSV_SEPARATOR) == 3)

def line_is_blank_or_comment (line):
	if (len(line.strip()) == 0):
		return True

	if (line[0] == "#"):
		return True
	
	return False

def music_info_file_is_valid (music_file_name):
	with open(music_file_name) as f:
		f.readline()	# Skip the header line
	
		for line in f:
			if (line_is_blank_or_comment(line)):
				continue

			if (not line_is_valid(line)):
				logger.critical(f"Invalid number of CSV separator (4 needed) in line: {line}")
				return False
	
	return True

def download_report (failed_download):
	print("")

	if failed_download == []:
		logger.info("All files have been downloaded !")
	else:
		logger.warning(f"Some download ({len(failed_download)}) have failed :")
		for music in failed_download:
			logger.warning(f"Download fail: {music}")

def run_command (command_list):
	logger.debug(f"Executing: {' '.join(command_list)}")
	# check=True is used to raise exception if the command fail
	subprocess.run(command_list, check=True)

def parse_line (line):
	line = line.strip()
	logger.debug(f"Parsing line: {line}")

	(url, artist, title, album) = line.split(CSV_SEPARATOR)

	logger.debug(f"Extracted data: url: {url}, artist: {artist}, title: {title}, album: {album}")

	return (url, artist, title, album)

def clean_file_name (file_name):
	characters_remplacement_list = (
		("/", "_"),
		("é", "e"), ("É", "E"), ("è", "e"), ("È", "E"),
		("ê", "e"), ("Ê", "E"), ("ë", "e"), ("Ë", "E"),
		("à", "a"), ("À", "A"), ("â", "a"), ("Â", "A"), ("ä", "a"), ("Ä", "A"),
		("î", "i"), ("Î", "I"), ("ï", "i"), ("Ï", "I"),
		("ô", "o"), ("Ô", "O"), ("ö", "o"), ("Ö", "O"),
		("ù", "u"), ("Ù", "U"), ("û", "u"), ("Û", "U"), ("ü", "u"), ("Ü", "U"),
		("ç", "c"), ("Ç", "C"),
		("ñ", "n"), ("Ñ", "N")
	)
	for character_couple in characters_remplacement_list:
		file_name = file_name.replace(character_couple[0], character_couple[1])

	forbidden_characters = """*"/:<>?\\|"""
	for character in forbidden_characters:
		file_name = file_name.replace(character, "")

	file_name = file_name.strip()

	return (file_name)

def get_music_file_name (artist, title):
	file_name = f"{artist} - {title}"
	file_name = clean_file_name(file_name)

	return (file_name)

def apply_metadata (file_name, artist, title, album):
	logger.info(f"Applying metadata on: {file_name}")
	
	try:
		run_command(["id3v2", "-D", file_name])	# Delete all metadata
		run_command(["id3v2", "-a", artist, "-t", title, "-A", album, file_name])	# Set artist, title and album
		return True
	except Exception as e:
		logger.critical(f"Could not apply metadata to {file_name}: {e}")

	return False

def apply_gain (file_name):
	logger.info(f"Applying gain on: {file_name}")

	try:
		run_command(["mp3gain", "-r", "-k", file_name])	# Apply gain
		return True
	except Exception as e:
		logger.critical(f"Could not apply gain to {file_name}: {e}")
	
	return False

def download_music (url, file_name):
	command_list = [
		"yt-dlp",
		"-f", "bestaudio", # Format selection
		"-x", # Extract audio
		"--audio-format", "mp3",
		"--audio-quality", "192K",
		"-o", file_name,
		url
	]

	logger.info(f"Downloading from: {url}")
	try:
		run_command(command_list)
		return True
	except Exception as e:
		logger.error(f"Could not download from {url}: {e}")
	
	return False

def main():
	# Create the output directory if it doesn't exist
	try:
		run_command(["mkdir", "-p", MUSIC_DIRECTORY])
	except Exception as e:
		logger.ciritcal(f"Could not create the output directory {MUSIC_DIRECTORY}: {e}")
		return

	logger.info("Verifying the music info file...")
	if (not music_info_file_is_valid(MUSIC_INFO_FILE)):
		return
	logger.info("Music info file is valid!")

	failed_download = []
	with open(MUSIC_INFO_FILE) as f:
		f.readline()	# Skip the header line

		music_index = 0
		for line in f:
			if (line_is_blank_or_comment(line)):
				continue

			music_index += 1
			print("")
			logger.info(f"Processing music number {music_index}")

			(url, artist, title, album) = parse_line(line)

			music_file_name = get_music_file_name(artist, title)
			music_file_name_no_extension = f"{MUSIC_DIRECTORY}/{music_file_name}"
			music_file_name_with_extension = f"{music_file_name_no_extension}.{FILE_EXTENSION}"

			logger.info(f"Currently working on {music_file_name}")

			if (os.path.exists(music_file_name_with_extension)):
				logger.info(f"{music_file_name} detected, skipping this file")
				continue

			success = download_music(url, music_file_name_no_extension)

			if not success:
				failed_download.append(f"{artist} - {title}")

			if (not os.path.exists(music_file_name_with_extension)):
				logger.error(f"Could not download from {url}. Skipping to the next file")
				continue

			success = apply_metadata(music_file_name_with_extension, artist, title, album)
			if not success:
				return

			success = apply_gain(music_file_name_with_extension)
			if not success:
				return

	download_report(failed_download)

logger = init_logging()

if (__name__ == "__main__"):
	start_time = program_start()

	main()

	program_stop(start_time)
