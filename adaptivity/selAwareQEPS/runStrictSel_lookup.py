import re
import glob
import pickle
from node import Node
import psycopg2
from missingTime import get_missing_time 


contained_nodes = 0
time_lost = 0
time_out_cnt = 0


def printPlanCache(plan_cache):
	next_branch = plan_cache
	while len(next_branch.child_nodes.keys()):
		next_branch = next_branch.child_nodes[list(next_branch.child_nodes.keys())[0]][(0,1)]
		print(next_branch.key,"alt", next_branch.child_nodes.keys(),"id", next_branch.id )


def getKeyCount(plan_cache):
	key_cnt = 1
	for key in plan_cache.child_nodes.keys():
		for interval in plan_cache.child_nodes[key].keys():
			key_cnt += getKeyCount(plan_cache.child_nodes[key][interval])
	return key_cnt



plan_cache = Node("root")


with open("strict_sel_qeps.pkl","rb") as file:
	plan_cache = pickle.load(file)


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
		'it':'it', 'it1':'it','it2':'it','it3':'it',
		'lt':'lt',
		'ml':'ml'}

pattern = re.compile("""(\((.)*?\))""")
pre_out_cnt = 0
feedback_list = glob.glob("../../feedback/fullData/*.sql")

for file in feedback_list:

	with open("SelDict/"+file.split("/")[-1].replace("sql", "pkl"), "rb" ) as selFile:
		sel_dict = pickle.load(selFile)

	feedback = open(file,"r").read()
	best_time = feedback.split("best_time:")[-1].split(" ")[1]
	feedback = feedback.split("/*+")[-1].split("*/")[0]
	feedback_copy = feedback
	feedback_alt = feedback
	match = pattern.findall(feedback)


	rel_matches = []
	feedback_list = []
	skip_bound = False
	f_l = []

	reference_branch = plan_cache

	has_empty_result = False
	with open("RowDict/"+file.split("/")[-1].replace(".sql",".pkl"),"rb") as fb:
			row_dict = pickle.load(fb)

	for n_match, m in enumerate(match):
		rels = m[0].replace("(","").replace(")","").split()
		rel_matches.append(rels)
		
		feedback_alt_1 = feedback_copy.replace(feedback.split(m[0])[0]+m[0],"HashJoin"+m[0])
		feedback_alt_2 = feedback_copy.replace(feedback.split(m[0])[0]+m[0],"NestLoop"+m[0])
		
		time_alt_1= 0
		time_alt_2= 0

		hit_1 = False
		hit_2 = False

		with open(file,"r") as f:
			for line in f:
				if feedback_alt_1 in line:
					hit_1 = True
					time_alt_1 = line.split(" / ")[0].split(" ")[-1]
				if feedback_alt_2 in line:
					hit_2 = True
					time_alt_2 = line.split(" / ")[0].split(" ")[-1]

			if not hit_1:
				with open("explicit/"+ file.split("/")[-1]) as query_file:
						query_string = query_file.read()
						time_alt_1 = get_missing_time("/*+"+feedback_alt_1+"*/\n"+query_string)
						with open("../../feedback/fullData/"+file.split("/")[-1],"r+") as clean_file:
							content = clean_file.read()
							clean_file.seek(0, 0)
							clean_file.write("/*+"+feedback_alt_1+"*/"+" time: "+str(time_alt_1)+" / "+str(time_alt_1)+"\n"+content)

			if not hit_2:
				with open("explicit/"+ file.split("/")[-1]) as query_file:
						query_string = query_file.read()
						time_alt_2 = get_missing_time("/*+"+feedback_alt_2+"*/\n"+query_string)
						with open("../../feedback/fullData/"+file.split("/")[-1],"r+") as clean_file:
							content = clean_file.read()
							clean_file.seek(0, 0)
							clean_file.write("/*+"+feedback_alt_2+"*/"+" time: "+str(time_alt_2)+" / "+str(time_alt_2)+"\n"+content)


			time_alt_1 = float(time_alt_1) 
			time_alt_2 = float(time_alt_2) 

		if has_empty_result:
			feedback_list.append([0,0])
		else:
			feedback_list.append([time_alt_1,time_alt_2])
		f_l.append(feedback.split(m[0])[0])
		feedback = feedback.replace(feedback.split(m[0])[0]+m[0],"")
		
		if row_dict[" ".join(rels)] == 0:
			has_empty_result = True

	root_rel = rel_matches[-1][0]
	main_key = ""
	prev_rel = []
	prev_was_sub = False

	for n_rel, rels in enumerate(rel_matches):
		if rels[0] != root_rel:
			prev_was_sub = True
		elif rels[0] == root_rel and prev_was_sub:
			prev_was_sub = False
			if main_key == "":
				main_key = str(root_rel)+"/"+("#").join(prev_rel)
			else:
				main_key += "/"+("#").join(prev_rel)
		else:
			if main_key == "":
				main_key += root_rel+"/"+("/").join(rels[n_rel+1:])
			else: 
				main_key += "/"+("/").join(rels[n_rel+1:]) 
		prev_rel = rels

		if rels[0] != root_rel:
			insert_key = ("/").join(rels)
			insert_rels = []
			for ir in ("/").join(rels).split("/"):
				if "#" in ir:
					for ir2 in ir.split("#"):
						insert_rels.append(ir2)
				else:
					insert_rels.append(ir)
			for ir in insert_rels:
				insert_key = insert_key.replace(ir, alias[ir])

			selectivity = sel_dict[insert_rels[-1]]
			if len(rels) == 2:
				sel_1 = sel_dict[insert_rels[-2]]
				sel_2 = sel_dict[insert_rels[-1]]
				replace_operator = reference_branch.getNext("#"+insert_key.split("/")[-2], sel_1).getNext("#"+insert_key.split("/")[-1], sel_2).getRecommended()		
				reference_branch=reference_branch.getNext("#"+insert_key.split("/")[-2], sel_1)
			else:
				replace_operator = reference_branch.getNext("#"+insert_key.split("/")[-1], selectivity).getRecommended()
			reference_branch=reference_branch.getNext("#"+insert_key.split("/")[-1], selectivity)	
			feedback_alt = feedback_alt.replace(f_l[n_rel]+"("+(" ").join(rels)+")",replace_operator+"("+(" ").join(rels)+")")
			if n_rel < len(rel_matches)-1 and rel_matches[n_rel+1][0] == root_rel:
				skip_bound = True

		else:
			insert_key = main_key
			insert_rels = []
			for ir in ("/").join(rels).split("/"):
				if "#" in ir:
					for ir2 in ir.split("#"):
						insert_rels.append(ir2)
				else:
					insert_rels.append(ir)
			for ir in insert_rels:
				insert_key = insert_key.replace(ir, alias[ir])

			selectivity = sel_dict[insert_rels[-1]]
			if len(rels) == 2 and not "#" in insert_key.split("/")[-1]:
				sel_1 = sel_dict[insert_rels[-2]]
				sel_2 = sel_dict[insert_rels[-1]]
				replace_operator = reference_branch.getNext(insert_key.split("/")[-2], sel_1).getNext(insert_key.split("/")[-1], sel_2).getRecommended()			
				reference_branch=reference_branch.getNext(insert_key.split("/")[-2], sel_1)
			else:
				replace_operator = reference_branch.getNext(insert_key.split("/")[-1], selectivity).getRecommended()
			reference_branch=reference_branch.getNext(insert_key.split("/")[-1], selectivity)	
			feedback_alt = feedback_alt.replace(f_l[n_rel]+"("+(" ").join(rels)+")",replace_operator+"("+(" ").join(rels)+")")
			
			contained_nodes += 1

			if skip_bound:
				skip_bound = False

	
	if feedback_alt != feedback_copy:
		with open(file,"r") as f:
			if not feedback_alt in f.read():
				print("feedback not contained", file)
				with open("explicit/"+ file.split("/")[-1]) as query_file:
					query_string = query_file.read()
					time_reeval = get_missing_time("/*+"+feedback_alt+"*/\n"+query_string)
					with open("../../feedback/fullData/"+file.split("/")[-1],"r+") as clean_file:
						content = clean_file.read()
						clean_file.seek(0, 0)
						clean_file.write("/*+"+feedback_alt+"*/"+" time: "+str(time_reeval)+" / "+str(time_reeval)+"\n"+content)
		with open(file,"r") as f:
			for line in f:
				if feedback_alt in line:
					time_fb = line.split(" / ")[0].split(" ")[-1]
					if feedback_alt != feedback_copy and not 'out' in time_fb:
						time_lost += max(0,float(time_fb) -float(best_time))
					if 'out' in time_fb:
						time_out_cnt += 1 
					break




print("delta best:", str(round(time_lost,2))+"s","nodes:", getKeyCount(plan_cache))
