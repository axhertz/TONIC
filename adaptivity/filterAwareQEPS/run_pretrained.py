import os


for i in range(0,10,1):

	os.system('python3 runStrictFilter_maintenance.py {} {}'.format("half_data",i/10))
	os.system('python3 runStrictFilter_lookup.py')

print("finished")
