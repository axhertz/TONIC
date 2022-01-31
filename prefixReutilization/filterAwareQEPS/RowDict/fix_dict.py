import pickle

fix_file = "21c.pkl"

with open(fix_file,"rb") as fb:
	row_dict = pickle.load(fb)

row_dict['ml lt t mc ct cn mk k mi'] = 0

with open(fix_file,"wb") as fw:
	pickle.dump(row_dict,fw)