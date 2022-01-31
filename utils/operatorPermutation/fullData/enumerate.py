import psycopg2
import glob
import time
import subprocess
import os
import pickle
import time 



def per(n):
	ret_list = []
	for i in range(1<<n):
		s=bin(i)[2:]
		s='0'*(n-len(s))+s
		ret_list.append(list(map(int,list(s))))
	return ret_list

query_list_expl = glob.glob("./explicit/*.sql")
query_list_adorn = []

for file in query_list_expl:
	query_list_adorn.append(file.replace("explicit","adorn"))




failed = []

for n,query in enumerate(query_list_expl):


	query_string_full_enum = ""

	with open(query, "r") as file:
		query_string = file.read()
	adorn_file = query.replace("explicit","adorn")
	with open(adorn_file,"r") as adorn:
		adorn_string = adorn.read()

	print(adorn_string.split("NestLoop"))

	for seq in per(len(adorn_string.split("NestLoop"))-1):
		next_string =adorn_string.split("NestLoop")[0]
		for j,s in enumerate(seq):
			if s == 1:
				next_string+="NestLoop"+adorn_string.split("NestLoop")[j+1]
			else:
				next_string+="HashJoin"+adorn_string.split("NestLoop")[j+1]
		


		
		query_string_full_enum += "\n----query "+ query+ "-------\n" +next_string+"\n"+query_string
	with open(query.replace("explicit","fullEnumQueries"),"w") as qf:
		qf.write(query_string_full_enum)
	

print(set(failed), len(set(failed)))