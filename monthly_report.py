# -- Function to create a monthly report -- #
def Monthly_Report():
	
	# Imports #
	import glob
	import datetime
	import os
	import csv
	import subprocess
	import pwd
	import yaml
	
	import hb_log
	import file_dict

	# -- Test Config .yml File -- #
	USERNAME = pwd.getpwuid(os.getuid()).pw_name
	config_path = "/home/" + USERNAME + "/.config/hb_reports/config.yml"
  
	try:	
		config = yaml.safe_load(open(config_path))
	except:	
		print("Configuration file at: \n\n\t" + config_path + "\n\ndoes not exist!  \n\nExiting gracefully...\n")
		exit()
	
	# Variables #	
	LogFile = config['global']['logpath']
	WorkingPath = config['global']['raw_files']
	LOG = hb_log.log(LogFile)

	# Create import file list and month,year variables #
	
	year,month,budgetFile,statisticsFile = file_dict.file_list_choice(WorkingPath,LOG)
	LOG.debug('Budget and Statistic file selected')
	
	print(f"Creating report for {month}, {year}")
	
	# Create the LaTeX report outfile		
	outfile = "report/report_outfile.tex"
	
	# Create the budget report table
	print(f"Writing Budget: {month}, {year}")

	# Variables
	infile = budgetFile
	outfile_write = open(outfile,"w")
	
	# Report title	
	Section = "\\section{Report for: " + month + ", " + year + "}\n\n"
	outfile_write.write(Section)
	
	# Budget Header
	Header = "\\subsection{Budget: }\n\n\\begin{longtable}{l|l|l|l|l}\n\n"
	outfile_write.write(Header)
	
	# Null values
	budget = 0
	budget_spend = 0
	budget_diff = 0
	income = 0
	budget_final = 0

	# Read .csv file
	with open(infile) as csvDataFile:
		csvReader = csv.reader(csvDataFile, delimiter=';')
		for row in csvReader:
			
			row_list = list(row)
			category = row_list[0]
			if row_list[2] != "Budget" and category[:15] != "Wage and Salary":
				budget = budget + float(row_list[2])
			if category != "Category" and category[:15] != "Wage and Salary":
				budget_spend = budget_spend + float(row_list[1])
			if category[:15] == "Wage and Salary":
				income = income + float(row_list[1])
			if row_list[1] != "Spent":
				budget_final = budget_final + float(row_list[1])

			Table = " & ".join(row )
			Table = Table + " \\\\ \n"
			outfile_write.write(Table)
	
	# Write footer
	Footer = "\n\\end{longtable}\n\n"
	outfile_write.write(Footer)

	# Budget calculations
	budget_diff = budget - budget_spend

	# Create the calculations
	budget = "{0:.2f}".format(budget)	
	budget_spend = "{0:.2f}".format(budget_spend)	
	budget_diff = "{0:.2f}".format(budget_diff)	
	income = "{0:.2f}".format(income)	
	budget_final = "{0:.2f}".format(budget_final)	
	budget_write = "Expense Budget: " + str(budget)
	Table = "Expense Budget: " + str(budget) + " & Budget Spending: " + str(budget_spend) + " & Budget Diff: " + str(budget_diff) + " & Income: " + str(income) + " & Total Outcome: " + str(budget_final) + " \\\\ \n\n" 
	
	# Table closing statements
	Calc_bTable = "\\begin{longtable}{l|l|l|l|l}\n\n"
	Calc_eTable = "\\end{longtable}\n\n"
	
	# Write out calculations
	outfile_write.write(Calc_bTable)
	outfile_write.write(Table)
	outfile_write.write(Calc_eTable)

	# Close files
	outfile_write.close()
	csvDataFile.close()

	# Log debug for budget report completion
	LOG.debug('Budget report completed')
	
	
	
	LOG.info('!!! Script Completed !!!')
	
	os.chdir("report")	
	subprocess.call("pdflatex report; pdflatex report",shell=True)
	
	LOG.info('!!! Report Compiled !!!')

	# END
	'''

	# Pick month and year based on file name, sort and create reports
	now = datetime.datetime.now()
	year = now.year
	working_year = year - 1
	
	# Create the file		
	outfile = "contents/complete_report.tex"
	outfile_write = open(outfile,"w")
	initial_file = (f"%% File Creation: {now.month}/{now.day}/{now.year} %%\n\n")
	outfile_write.write(initial_file)
	outfile_write.close()
	
	while working_year <= year:
		for working_month in month_list:
			month = working_month[2:]

			#write out budget
			infile = (f'raw/{working_year}_{month}_budget.csv')
			
			if os.path.isfile(infile):
				outfile_write = open(outfile,"a")

				Month = month.capitalize()
				Year = str(working_year)
				
				print(f"Writing Budget: {Month}, {Year}")

				Section = "\\section{Report for: " + Month + ", " + Year + "}\n\n"
				outfile_write.write(Section)

				Header = "\\subsection{Budget: " + Month + ", " + Year + "}\n\n\\begin{longtable}{l|l|l|l|l}\n\n"
				outfile_write.write(Header)
				
				budget = 0
				budget_spend = 0
				budget_diff = 0
				income = 0
				budget_final = 0

				with open(infile) as csvDataFile:
					csvReader = csv.reader(csvDataFile, delimiter=';')
					for row in csvReader:
						
						row_list = list(row)
						category = row_list[0]
						if row_list[2] != "Budget" and category[:15] != "Wage and Salary":
							budget = budget + float(row_list[2])
						if category != "Category" and category[:15] != "Wage and Salary":
							budget_spend = budget_spend + float(row_list[1])
						if category[:15] == "Wage and Salary":
							income = income + float(row_list[1])
						if row_list[1] != "Spent":
							budget_final = budget_final + float(row_list[1])

						Table = " & ".join(row )
						Table = Table + " \\\\ \n"
						outfile_write.write(Table)
				
				Footer = "\n\\end{longtable}\n\n"
				outfile_write.write(Footer)

				budget_diff = budget - budget_spend

				budget = "{0:.2f}".format(budget)	
				budget_spend = "{0:.2f}".format(budget_spend)	
				budget_diff = "{0:.2f}".format(budget_diff)	
				income = "{0:.2f}".format(income)	
				budget_final = "{0:.2f}".format(budget_final)	
				budget_write = "Expense Budget: " + str(budget)
				Table = "Expense Budget: " + str(budget) + " & Budget Spending: " + str(budget_spend) + " & Budget Diff: " + str(budget_diff) + " & Income: " + str(income) + " & Total Outcome: " + str(budget_final) + " \\\\ \n\n" 
				#income_write = "\\\\ \n Budget Spend: & " + str(budget_spend) + " & & & \\\\ \n"
				#bspend_write = "\\\\ \n Budget Spend: & " + str(budget_spend) + " & & & \\\\ \n"
				#bfinal_write = "Budget Final Spend: & " + str(budget_final) + " & & & \\\\ \n\n"

				Calc_bTable = "\\begin{longtable}{l|l|l|l|l}\n\n"
				Calc_eTable = "\\end{longtable}\n\n"
				outfile_write.write(Calc_bTable)
				outfile_write.write(Table)
				#outfile_write.write(budget_write)
				#outfile_write.write(income_write)
				#outfile_write.write(bspend_write)
				#outfile_write.write(bfinal_write)
				outfile_write.write(Calc_eTable)


				outfile_write.close()
				csvDataFile.close()
			else:
				continue

			#write out statistics
			infile = (f'raw/{working_year}_{month}_statistics.csv')
			
			if os.path.isfile(infile):
				outfile_write = open(outfile,"a")
				
				#Month = month.capitalize()
				#Year = str(working_year)
				Header = "\\subsection{Statistics: " + Month + ", " + Year + "}\n\n\\begin{longtable}{l|l|l|l}\n\n"
				outfile_write.write(Header)
				
				print(f"Writing Statistics: {Month}, {Year}")
				
				total_spend = 0
				
				with open(infile) as csvDataFile:
					csvReader = csv.reader(csvDataFile, delimiter=';')
					for row in csvReader:
						
						row_list = list(row)
						category = row_list[0]
						
						if category != "Result" and category not in budget_list:
							
							total_spend = total_spend + float(row_list[3])
						
							Table = " & ".join(row )
							Table = Table + " \\\\ \n"
							print(Table)
							outfile_write.write(Table)

				total_spend = "{0:.2f}".format(total_spend)	
				tspend_write = "Total Spend: & " + str(total_spend) + " & & \\\\ \n\n \\newpage"
				outfile_write.write(tspend_write)

				Footer = "\n\\end{longtable}\n\n"
				outfile_write.write(Footer)

				outfile_write.close()
				csvDataFile.close()    
			else:
				continue

		
	subprocess.call("pdflatex reports; pdflatex reports",shell=True)


	'''
