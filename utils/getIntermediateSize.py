import psycopg2
import glob
import time
import subprocess
import os
import pickle
import time 
import re

def getSubqueries(query):
	pattern = re.compile("""(\(select (.|\n)*?\)\) as t_)""")
	match = pattern.findall(query)
	list_of_subqueries = []
	for m in match:
		list_of_subqueries.append(m[0].replace(" as t_",""))
	return list_of_subqueries

def matchAliasWithQuery(subquery, adorn):
	pattern = re.compile("""(\((.)*?\))""")
	match = pattern.findall(adorn)
	adorn_list = []
	for m in match:
		adorn_list.append(m[0])
	current_match = []
	for a in adorn_list:
		a_list = a.replace("(","").replace(")","").split()
		hit = True
		for alias in a_list:
			if "AS "+alias +" " not in subquery:
				hit = False
				break
		if hit and len(a_list) > len(current_match):
			current_match = a_list
	return(current_match)

def replaceSelect(query):
	split = query.split("from")
	return "(select count(*) from "+ split[-1]+";"

def getRows(query_file, adorn_file):
	with open(query_file,"r") as file:
		query = file.read()

	with open(adorn_file, "r") as file:
		adorn = file.read()

	row_dict = {}

	def getNextRow(subq):
		if not "count(*)" in subq:
			cursor.execute(replaceSelect(subq))
		else:
			cursor.execute(subq)
		result = None
		for res in cursor:
			result = res[0]
			break
		next_row = "Rows("
		for alias in matchAliasWithQuery(subq,adorn):
			next_row += alias +" "
		
		row_dict[next_row.replace("Rows(","")[:-1]] = int(result)
		next_row += "#"+str(result)+")"

		return next_row

	subqueries = getSubqueries(query)

	connection = psycopg2.connect(host="localhost", database="imdb", user="postgres", port = "5432")
	cursor = connection.cursor()

	rows = ""


	for subq in subqueries:

		rows += getNextRow(subq)
		if len(subq.split("join")) > 2:
			subqc = replaceSelect(subq).replace("(select","select")
			subqce = subqc.split("join")[0]
			for i in range(1,len(subq.split("join"))-1,1):
				subqce += "join " + subq.split("join")[i]
				rows += getNextRow(subqce)

	part_query = ""
	with open(query_file,"r") as file:
		for line in file:
			in_sub = False
			for sub in subqueries:
				if line.split(" as t_")[0] in sub:
					part_query += line
					in_sub = True
					break
			if in_sub: continue
			if " on " in line and "join " in line and " AS " in line:
				part_query += line

				rows += getNextRow(part_query)

			elif "on(" in line and not "join " in line and not " AS " in line:
	
				part_query += line
				rows += getNextRow(part_query)

			else:
				part_query += line
	connection.close()


	return rows, row_dict

def main():
	query_list = glob.glob("./explicit/*.sql")
	for num, query_file in enumerate(query_list):
		print(query_file, num)
		adorn_file = query_file.replace("explicit","adorn")
		theRows, row_dict = getRows(query_file,adorn_file)
		print(row_dict)
		#with open(query_file.replace("explicit_idx","Rows"),"w") as outfile:
		#	outfile.write(theRows)
		#with open(query_file.replace("explicit_idx","RowDict").replace(".sql",".pkl"),"wb") as of:
		#	pickle.dump(row_dict,of)


if __name__ == '__main__':

	main()