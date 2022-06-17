import pickle

fix_file = "33c.pkl"

with open(fix_file,"rb") as fb:
	row_dict = pickle.load(fb)

row_dict['ml lt t2 t1 kt1 kt2 mi_idx1 it1 mi_idx2 it2'] = 0

with open(fix_file,"wb") as fw:
	pickle.dump(row_dict,fw)