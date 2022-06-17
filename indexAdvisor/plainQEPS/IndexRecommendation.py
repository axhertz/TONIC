import os
import glob
import pickle
from node import Node


contained_nodes = 0


time_lost = 0
time_out_cnt = 0


def getKeyCount(plan_cache):
	key_cnt = 1
	for key in plan_cache.child_nodes.keys():
		for interval in plan_cache.child_nodes[key].keys():
			key_cnt += getKeyCount(plan_cache.child_nodes[key][interval])
	return key_cnt


def getCostSummary(plan_cache):
	costDict = {}
	freqDict = {}
	for key in plan_cache.child_nodes.keys():
		if not key+"."+plan_cache.child_nodes[key][(0,1)].attr in costDict:
			costDict[key+"."+plan_cache.child_nodes[key][(0,1)].attr] = 0
		current_child = plan_cache.child_nodes[key][(0,1)]
		if current_child.hashCost > current_child.nestCost:
			costDict[key+"."+plan_cache.child_nodes[key][(0,1)].attr] +=  current_child.hashCost - current_child.nestCost
		costDict2, freqDict2 = getCostSummary(current_child)
		for key2 in costDict2:
			if key2 not in costDict.keys():
				costDict[key2] = 0
			costDict[key2] += costDict2[key2]


	return costDict, freqDict


def simulateIndexDel(plan_cache, rel, attr):
	for key in plan_cache.child_nodes.keys():
		if (key == rel or key == "#"+rel) and attr == plan_cache.child_nodes[key][(0,1)].attr:
			plan_cache.child_nodes[key][(0,1)].nestCost += 10**20
		simulateIndexDel(plan_cache.child_nodes[key][(0,1)], rel, attr)



#key_list = ['#cc', 'cc#cct', '#mk', '#an', 'an#n', '#mi_idx', 'mi_idx#it', '#mc', 'mc#cn', '#mi', 'mi#it', '#ci', '#t', 'ci#rt#t', 'ci#n', 'cc', 'ci#n#chn', '#pi', 'pi#it', '#ct', 'mc#ct#cn', '#ml', 'ml#lt', 'ml', 'cc#cct#cct', 'pi', '#lt', 'rt', 'cct', 'kt', 'ct', '#cct', 'mk#k', '#chn', 'lt', '#cn', 'it', 'an', 'mi_idx', 'mk', 'k', '#it', 'at', '#rt', 'chn', '#k', 'n', 'cn', 'mc', '#n', 't', 'mi', 'ci']
plan_cache = Node("root")
with open("plain_qeps.pkl","rb") as fb:
	plan_cache = pickle.load(fb)

csummary,_ = getCostSummary(plan_cache)
theKeys = csummary.keys()

theKeysSorted = sorted(csummary, key=csummary.get)
theKeysSorted = [k for k in theKeysSorted if not "#" in k]

#print("start ####")
for k in theKeysSorted:
	if "#" in k: continue
	if k.split(".")[-1] == "id" : continue

	print(csummary[k])
	with open("plain_qeps.pkl","rb") as fb:
		plan_cache = pickle.load(fb)


	simulateIndexDel(plan_cache, k.split(".")[-2], k.split(".")[-1])


	with open("plain_qeps_del_index.pkl", "wb") as fb:
		pickle.dump(plan_cache,fb)

	os.system('python3 runPlain_lookup.py {}'.format(k))



