def file_list_choice(working_directory,LOG):
	
	# Imports #
	import os
	import glob
	
	import hb_log

	# Null lists values #
	file_dict = {}		# null dictionary for file
	sort_dict = {}		# null dictionary for artist sort directories

	sort_list = []		# null list for artist sort directories
	budget_list = []
	statistics_list = []

	# Variables #
	increment = 1
	file_list = glob.glob(working_directory + "/*")

	# Create and sort budget file list #
	for i in file_list:
		if i[-10:] == "budget.csv":
			budget_list.append(i)
	
	budget_list.sort()
	
	# Choose the Month,Year for Report - Use the budget files as a sort list #
	for item in budget_list:
		year = item[59:63]
		month = item[67:-11]
		month = month.capitalize()
		print(f"{increment}: {month}, {year}") # This is the "menu" output for making a selection
		file_dict.update({increment:item})
		increment += 1

	# Make a selection to run report against #
	ch = input("Choose a number ")
	ch = int(ch)
	importFile = file_dict[ch]
	
	# Reset the chosen year and month #
	year = importFile[59:63]
	month = importFile[67:-11]
	month = month.capitalize()
	
	# Create the statFile #
	statFile = importFile.replace("budget", "statistics", 1)
	
	# Log the chosen files for debugging
	LOG.debug(f"Budget file chosen: {importFile}")	
	LOG.debug(f"Statistics file chosen: {statFile}")
	
	if os.path.isfile(importFile):
		LOG.debug(f"Budget file {importFile} is valid")
	else:
		LOG.info(f"Budget file {importFile} is invalid.  Exiting gracefully...")
		print(f"Budget file {importFile} is invalid.  Exiting gracefully...")
		exit()

	if os.path.isfile(statFile):
		LOG.debug(f"Budget file {statFile} is valid")
	else:
		LOG.info(f"Budget file {statFile} is invalid.  Exiting gracefully...")
		print(f"Budget file {statFile} is invalid.  Exiting gracefully...")
		exit()
			
	
	# Return the values #
	return year,month,importFile,statFile

