import pickle

gamma_dict = {}
gamma_dict[1] = 8.75
gamma_dict[0.99]= 8.75
gamma_dict[0.95]= 8.75
gamma_dict[0.9] = 8.74
gamma_dict[0.8]= 8.85
gamma_dict[0.7]= 18.87
gamma_dict[0.6]=18.94

with open("timediff_gamma.pkl","wb") as fb:
	pickle.dump(gamma_dict,fb)