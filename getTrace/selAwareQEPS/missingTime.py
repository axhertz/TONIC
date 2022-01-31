import psycopg2
import time

def get_missing_time(query_stm):
	connection = psycopg2.connect(host='localhost', database='imdb_full', user='postgres',port = 5432)
	cursor = connection.cursor()
	cursor.execute("LOAD \'pg_hint_plan\';")
	cursor.execute("SET search_path TO public;")
	cursor.execute("SET pg_hint_plan.debug_print TO on;")
	cursor.execute("SET client_min_messages TO LOG;")
	cursor.execute("SET pg_hint_plan.enable_hint TO on;")
	cursor.execute("set enable_nestloop to false;")
	cursor.execute("set join_collapse_limit to 1;")
	cursor.execute("SET statement_timeout = '40s';")
	t1 = time.time()
	try:
		cursor.execute(query_stm)
		time.sleep(2)
	except:
		print("time out")
		connection.rollback()
		print("return", time.time()- t1)
		return time.time()- t1
	t1 = time.time()
	cursor.execute(query_stm)
	print("return", time.time()-t1)
	return time.time()- t1
