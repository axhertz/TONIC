
import os
import sys
import re
import glob
import pickle
import random
import psycopg2
import math


"""
CREATE FUNCTION count_estimate(query text) RETURNS integer AS
$func$
DECLARE
    rec   record;
    rows  integer;
BEGIN
    FOR rec IN EXECUTE 'EXPLAIN ' || query LOOP
        rows := substring(rec."QUERY PLAN" FROM ' rows=([[:digit:]]+)');
        EXIT WHEN rows IS NOT NULL;
    END LOOP;
    RETURN rows;
END
$func$ LANGUAGE plpgsql;
"""


pks = ["at.id","cct1.id","cct2.id","cc.id", "mc.id", "mc1.id", "mc2.id", "ct.id","cn.id","cn1.id",\
		 "cn2.id", "ml.id", "t.id", "t1.id", "t2.id","mk.id", "k.id", "lt.id", "kt.id", "kt1.id",\
		  "kt2.id","chn.id", "mi.id", "ci.id","mi_idx.id", "mi_idx1.id", "mi_idx2.id", "rt.id",\
		  "an.id", "an1.id", "a1.id", "n.id", "n1.id", "pi.id", "it.id", "it1.id", "it2.id", "it3.id", "miidx.id"]

#Foreign keys of the join order benchmark.
fks = ["at.movie_id", "cc.subject_id", "cc.status_id", "cc.movie_id", "mc.movie_id", "mc1.movie_id", "mc2.movie_id",\
		"mc.company_type_id","mc1.company_type_id","mc2.company_type_id","mc.company_id","mc1.company_id","mc2.company_id",\
		"ml.movie_id", "ml.link_type_id", "ml.linked_movie_id", "t.kind_id","t1.kind_id", "t2.kind_id", "mk.movie_id",\
		"mk.keyword_id", "mi.movie_id", "mi.info_type_id",	"mi_idx.movie_id","mi_idx1.movie_id","mi_idx2.movie_id",\
		"mi_idx.info_type_id","mi_idx1.info_type_id", "mi_idx2.info_type_id","ci.movie_id", "ci.person_id",\
		"ci.role_id","ci.person_role_id","an.person_id", "an1.person_id", "a1.person_id","pi.person_id",\
		"pi.info_type_id","miidx.movie_id", "miidx.info_type_id", "it3.info", "cct1.kind", "cct2.kind"]

alias ={'kt':'kt','kt1':'kt','kt2':'kt',
		't':'t','t1':'t','t2':'t',
		'mk':'mk','mk1':'mk2','mk':'mk',
		'a':'an','a1':'an','a2':'an','an':'an','an1':'an',
		'mc':'mc','mc1':'mc','mc2':'mc',
		'at':'at',
		'cct':'cct','cct1':'cct','cct2':'cct',
		'rt':'rt',
		'mi_idx':'mi_idx','miidx':'mi_idx','mi_idx1':'mi_idx','mi_idx2':'mi_idx',
		'ct': 'ct',
		'n':'n','n1':'n','n2':'n',
		'cn':'cn', 'cn1':'cn', 'cn2':'cn', 
		'ci':'ci' , 
		'chn':'chn', 
		'cc':'cc',
		'k':'k',
		'mi':'mi',
		'pi':'pi',
		'it':'it', 'it1':'it','it2':'it',
		'lt':'lt',
		'ml':'ml'}

def get_selectivity_dict(data):
	from_clause = data.split("FROM")[1].split("WHERE")[0]

	rel_names =[]

	for relation_string in from_clause.split(","):
		rel_names.append(relation_string.split(" ")[-1].replace("\n",""))

	where_clause = data.split("WHERE")[-1]
	where_string = where_clause.split("\n")
	where_string = [s.replace("AND", "",1).replace("  "," ") for s in where_string if s != ""]
		
	dict_rel_filter = {}
	filters = []
	join_filters = []


	for w_r in where_string:
		test_rels = []
		for sub_string in w_r.split(" "):
			if "." in sub_string:
				test_rels.append(sub_string.split(".")[0]+".id")	
		if len(set(test_rels).intersection(set(pks)))==1:
			rel = w_r.lstrip().rstrip().split(".")
			rel[0] = rel[0].replace("(","").replace(")","")
			if not rel[0] in dict_rel_filter.keys():
				dict_rel_filter[rel[0]] = [w_r.lstrip().rstrip()]
			else:
				dict_rel_filter[rel[0]].append(w_r.lstrip().rstrip())
			filters.append(w_r.lstrip().rstrip())
		else:
			join_filters.append(w_r.lstrip().rstrip())

	select_smts = []

	for rel in dict_rel_filter.keys():
		for relation_string in from_clause.split(","):
			if len(set([rel]).intersection(set(relation_string.lstrip().rstrip().split(" ")))) == 1:
				select_smt = "select count(*) from "+ relation_string.lstrip() + " where "
				for num, fltr in enumerate(dict_rel_filter[rel]):
					if num == 0:
						select_smt += " "+fltr
					else:
					 select_smt += " AND "+fltr
				select_smts.append(select_smt+";")			
				break

	for rel in rel_names:
		if rel not in dict_rel_filter.keys():
			for relation_string in from_clause.split(","):
				if len(set([rel]).intersection(set(relation_string.lstrip().rstrip().split(" ")))) == 1:
					select_smts.append("select count(*) from "+ relation_string.lstrip() +";")
					break

	connection = psycopg2.connect(host='localhost', database='imdb', user='postgres', password='',port=5432)
	
	rel_dict = {}

	#get filter selectivity estimates
	cursor = connection.cursor()
	for stm in select_smts:
		if "where" in stm:
			stm = stm.split("where")[0]
		stm_est = stm.replace("count(*)","*").replace("\'","\'\'").replace(";","")
		stm_est = "select count_estimate(\'{}\');".format(stm_est)
		cursor.execute(stm_est)
		for query in cursor:
			for rel in rel_names:
				if " "+rel+ " " in stm or " " +rel+"\n" in stm or " "+rel+";"in stm:
					rel_dict[rel] =rel_dict[rel] /math.ceil(query[0])
	
	return rel_dict

	
