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
	
	# Minipage Header
	begMinipage = "\\begin{minipage}[c][][t]{.75\\textwidth}\n"
	outfile_write.write(begMinipage)
	
	# Budget Header
	Header = "\\subsection{Budget: }\n\n\\noindent\n\\begin{longtable}{l|l|l|l|l}\n\n"
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
	budget = abs(budget)
	budget = "{0:.2f}".format(budget)
	budget_spend = abs(budget_spend)
	budget_spend = "{0:.2f}".format(budget_spend)	
	budget_diff = "{0:.2f}".format(budget_diff)	
	income = "{0:.2f}".format(income)	
	budget_cFinal = budget_final #used for calculations later
	budget_final = "{0:.2f}".format(budget_final)	
	budget_write = "Expense Budget: " + str(budget)
	#Table = "Expense Budget: " + str(budget) + " & Budget Spending: " + str(budget_spend) + " & Budget Diff: " + str(budget_diff) + " & Income: " + str(income) + " & Total Outcome: " + str(budget_final) + " \\\\ \n\n" 
	Table = "Expense Budget: \$" + str(budget) + " \\\\ \n Budget Spending: \$" + str(budget_spend) + " \\\\ \n Budget Diff: \$" + str(budget_diff) + " \\\\ \n Income: \$" + str(income) + " \\\\ \n Total Outcome: \$" + str(budget_final) + " \\\\ \n\n" 
	
	# Set next minipage
	midMinipage = "\\end{minipage}\n\\hspace{0mm}\n\\begin{minipage}[c][][t]{.23\\textwidth}\n"
	endMinipage = "\\end{minipage}\n"

	# Table closing statements
	#Calc_bTable = "\\noindent\n\\begin{longtable}{l|l|l|l|l}\n\n"
	Calc_bTable = "\\noindent\n\\begin{longtable}{l}\n\n"
	Calc_eTable = "\\end{longtable}\n\n"
	
	# Write out calculations
	outfile_write.write(midMinipage)
	outfile_write.write(Calc_bTable)
	outfile_write.write(Table)
	outfile_write.write(Calc_eTable)
	outfile_write.write(endMinipage)

	# Close files
	outfile_write.close()
	csvDataFile.close()

	# Log debug for budget report completion
	LOG.debug('Budget report completed')
	
	
	# Create null lists
	liBudget = [] # List of budget categories for filtering
	liStatistics = [] # List of statistics categories for filtering
	fullStatistics = [] # Full list of statistics
	
	# Update budget files to have spaces in the : separators to match statistics files
	
	# Create lists for budget categories
	with open(budgetFile) as csvBudgetFile:
		csvBudget = csv.reader(csvBudgetFile, delimiter=';')
		for row in csvBudget:
			liBudget.append(row[0])
			
	# Create lists for statistics categories and full statistics info
	with open(statisticsFile) as csvStatisticsFile:
		csvStatistics = csv.reader(csvStatisticsFile, delimiter=';')
		for row in csvStatistics:
			liStatistics.append(row[0])
			fullStatistics.append(row)
	
	# Filter list of budget categories from statistics 
	nonBudgetList = (list(set(liStatistics) - set(liBudget))) 
	nonBudgetList.sort()
	
	# Open the outfile and write header information
	outfile_write = open(outfile,"a")
	Header = "\\subsection{Statistics: " + month + ", " + year + "}\n\n\\begin{minipage}[c][][t]{.65\\textwidth}\n\\begin{longtable}{l|l|l|l}\n\n"
	outfile_write.write(Header)
	
	print(f"Writing Statistics: {month}, {year}")
	
	# Null values for calculations
	total_spend = 0
	outsideBudget = 0
	
	# Write out nonbudget table
	for i in nonBudgetList:
		if i[:30] != "Credit Card Payments/Transfers" and i != "Result" and i != "Credit Card Payment Received" and i[:11] != "Job Expense":
			for x in fullStatistics:
				if i == x[0]:
					outsideBudget = outsideBudget + float(x[3])
					Table = (f"{x[0]} & {x[3]}")
					Table = Table + " \\\\ \n"
					outfile_write.write(Table)

	# Calculate the monthly final amount
	monthlyFinal = budget_cFinal - outsideBudget
	
	# Format the calculations
	outsideBudget = "{0:.2f}".format(outsideBudget)
	monthlyFinal = "{0:.2f}".format(monthlyFinal)
	
	# Output variable to write calculations
	outsideTable = "Spending Outside Budget: \$" + str(outsideBudget) + "\\\\ \n Total Monthly Spending: \$ " + monthlyFinal + " \\\\ \n\n" 

	# Write output to outfile
	Footer = "\n\\end{longtable}\n\n"
	outfile_write.write(Footer)
	outfile_write.write(midMinipage)
	outfile_write.write(Calc_bTable)
	outfile_write.write(outsideTable)
	outfile_write.write(Calc_eTable)
	outfile_write.write(endMinipage)

	# Close files
	outfile_write.close()
	csvBudgetFile.close()    
	csvStatisticsFile.close()    

	LOG.debug('Statistics report completed')

	
	LOG.info('!!! Script Completed !!!')
	
	os.chdir("report")	
	#subprocess.call("pdflatex report; pdflatex report",shell=True)
	subprocess.call("pdflatex report",shell=True)
	
	LOG.info('!!! Report Compiled !!!')

	# END
	'''

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
				
				edit


# Python code t get difference of two lists 
# Using set() 
def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 
  
# Driver Code 
li1 = [10, 15, 20, 25, 30, 35, 40] 
li2 = [25, 40, 35] 
print(Diff(li1, li2)) 
				
				
				
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
