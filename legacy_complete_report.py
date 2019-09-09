# Function to create the complete monthly report #
def Complete_Report_NEW():
	
	import glob
	import datetime
	import os
	import csv
	import subprocess
	
	# Scan folder for all current files
	workingpath = "raw"
	file_list = glob.glob(workingpath + "/*")
	working_list = []
	month_list = ["01january","02february","03march","04april","05may","06june","07july","08august","09september","10october","11november","12december"]
	month_list.sort()
	budget_list = ["Automobile : Car Payment","Automobile : Gasoline","Utilities : Electricity","Utilities : Internet Service","Utilities : Mobile Phone","Utilities : Natural Gas","Utilities : Sewage","Utilities : Water","Education : Student Loans","Entertainment : Netflix","Mortgage : Mortgage Payment","Insurance	: Life Insurance","Mortgage : Line of Credit","Food : Groceries","Household : General Goods","Food : Dining Out","Food : School Lunch","Home Improvement : Storage Shed","Children : Daycare","Wage and Salary : Ampco-Pittsburgh","Wage and Salary : Carnegie Presbyterian Church","Wage and Salary : Club-Z"]
	
	yearly_savings_filter = ["Savings Account : Automobile Insurance","Savings Account : Christmas Gifts","Savings Account : Debt Reduction","Savings Account : Emergency Fund","Savings Account : Gifts","Savings Account : Miscellaneous","Savings Account : Vacation and Travel"]
	
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

		## Create yearly summaries

		#Open the infile
		infile = (f'raw/{working_year}_summary.csv')
		#print(infile)
		
		# Create Statistics Yearly Summary
		if os.path.isfile(infile):
			outfile_write = open(outfile,"a")
			
			#Month = month.capitalize()
			#Year = str(working_year)
			Header = "\\subsection{Statistics: " + Year + "}\n\n\\begin{longtable}{l|l|l|l}\n\n"
			outfile_write.write(Header)
			
			print(f"Writing Statistics: {Year}")
			
			total_spend = 0
			
			with open(infile) as csvDataFile:
				csvReader = csv.reader(csvDataFile, delimiter=';')
				for row in csvReader:
					
					row_list = list(row)
					category = row_list[0]
					
					#if category != "Result" and category not in budget_list:
					if category != "Result":
						
						total_spend = total_spend + float(row_list[3])
					
						Table = " & ".join(row )
						Table = Table + " \\\\ \n"
						print(Table)
						outfile_write.write(Table)

			total_spend = "{0:.2f}".format(total_spend)	
			#tspend_write = "Total Spend: & " + str(total_spend) + " & & \\\\ \n\n \\newpage"
			outfile_write.write(tspend_write)

			Footer = "\n\\end{longtable}\n\n"
			outfile_write.write(Footer)

			outfile_write.close()
			csvDataFile.close()    
			
				
		# Create the Savings Summary	
		if os.path.isfile(infile):
			outfile_write = open(outfile,"a")
			#print("Infile Opened")
			
			#Month = month.capitalize()
			#Year = str(working_year)
			Header = "\\subsection{Yearly Savings: " + Year + "}\n\n\\begin{longtable}{l|l|l|l}\n\n"
			outfile_write.write(Header)
			
			total_spend = 0
			
			with open(infile) as csvDataFile:
				csvReader = csv.reader(csvDataFile, delimiter=';')
				for row in csvReader:
					
					row_list = list(row)
					category = row_list[0]
					
					if category != "Result" and category in yearly_savings_filter:
						
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
		#else:
		#	continue

		working_year = working_year + 1
		print(f"Working Year {working_year}")
		
	subprocess.call("pdflatex reports; pdflatex reports",shell=True)
