import os

for i in range(0,10,1):

	os.system('python3 runPlain_maintenance.py {} {}'.format("reduced_data",i/10))
	os.system('python3 runPlain_lookup.py')

print("finished")
