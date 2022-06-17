import os

for i in range(1,10,1):

	os.system('python3 runPlain_maintenance.py {} {}'.format("empty",i/10))
	os.system('python3 runPlain_lookup.py')

print("finished")
