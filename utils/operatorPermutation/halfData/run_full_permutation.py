import psycopg2
import glob
import time
import subprocess
import os
import pickle
import time 



def get_files_by_file_size(dirname, reverse=False):
    """ Return list of file paths in directory sorted by file size """

    # Get list of files
    filepaths = []
    for basename in os.listdir(dirname):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename):
            filepaths.append(filename)

    # Re-populate list with filename, size tuples
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(filepaths[i]))

    # Sort list by file size
    # If reverse=True sort from largest to smallestcursor.execute("SET statement_timeout = '20s';")

    # If reverse=False sort from smallest to largest
    filepaths.sort(key=lambda filename: filename[1], reverse=reverse)

    # Re-populate list with just filenames
    for i in range(len(filepaths)):
        filepaths[i] = filepaths[i][0]

    return filepaths


query_list = get_files_by_file_size("./fullEnumQueries")

print(query_list)
#exit()

connection = psycopg2.connect(host='localhost', database='half_imdb', user='postgres',port = 5432)
cursor = connection.cursor()
cursor.execute("LOAD \'pg_hint_plan\';")
cursor.execute("SET search_path TO public;")
cursor.execute("SET pg_hint_plan.debug_print TO on;")
cursor.execute("SET client_min_messages TO LOG;")
cursor.execute("SET pg_hint_plan.enable_hint TO on;")
cursor.execute("set enable_nestloop to false;")
cursor.execute("set join_collapse_limit to 1;")
cursor.execute("SET statement_timeout = '20s';")


total_time = time.time()
for n,query in enumerate(query_list):

	if os.path.exists(query.replace("fullEnumQueries","result_pk_fk")):
		continue
	print("num",n,"query",query)

	cursor.execute("SET statement_timeout = '40s';")


	with open(query, "r") as file:
		query_string_full = file.read()

	best_time = 10000000000
	best_time_cold = 1000000000
	best_operator = ""
	time_string = "SET statement_timeout = '20s';"
	for qn, query_string in enumerate(query_string_full.split(";")[:-1]):

		filename = query.replace("fullEnumQueries","result_pk_fk")
		if qn == 1: 
			time_string = "SET statement_timeout = '{}s';".format(min(max(2*best_time,2), 10))
			cursor.execute(time_string)
		if os.path.exists(filename):
			append_write = 'a+' # append if already exists
		else:
			append_write = 'w' # make a new file if not
		with open(filename, append_write) as file:

			file.write(query_string.split("-------")[-1].split("*/")[0]+"*/")

		try:

			t0 = time.time()

			cursor.execute(query_string.split("-------")[-1] +";")
			exec_time_cold = time.time() - t0
			t1 = time.time()
			cursor.execute(query_string.split("-------")[-1] +";")
			exec_time = time.time()-t1
			filename = query.replace("fullEnumQueries","result_pk_fk")
			if os.path.exists(filename):
				append_write = 'a+' # append if already exists
			else:
				append_write = 'w' # make a new file if not
			if exec_time < best_time:
					best_time = exec_time
					best_time_cold = exec_time_cold
					best_operator = query_string.split("-------")[-1].split("*/")[0]+"*/"

			with open(filename, append_write) as file:

				file.write(" time: "+str(exec_time)+" / "+str(exec_time_cold))

		except:
			print("time out, continue ...")
			connection.rollback()
			cursor.execute(time_string)

			cursor.execute("SET join_collapse_limit = 1;")
			cursor.execute("SET enable_nestloop to false;")
			cursor.execute("LOAD \'pg_hint_plan\';")
			cursor.execute("SET search_path TO public;")
			cursor.execute("SET pg_hint_plan.debug_print TO on;")
			cursor.execute("SET client_min_messages TO LOG;")
			cursor.execute("SET pg_hint_plan.enable_hint TO on;")
			filename = query.replace("fullEnumQueries","result_pk_fk")
			if os.path.exists(filename):
				append_write = 'a+' # append if already exists
			else:
				append_write = 'w' # make a new file if not
			with open(filename, append_write) as file:
				file.write(" timed out")

	filename = query.replace("fullEnumQueries","result_pk_fk")
	with open(filename, "a+") as file:
		file.write(best_operator  + " best_time: " + str(best_time) + " / "+str(best_time_cold)+"\n")
		print(best_operator  + " best_time: " + str(best_time))

print("total_time", time.time()-total_time)

connection.close()


