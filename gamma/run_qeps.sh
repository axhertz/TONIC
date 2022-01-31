
#!/bin/bash
trap "exit" INT
array=( 1 0.99 0.95 0.9 0.8 0.7 0.6)
for gamma in "${array[@]}"
do
	FILE="./half_data/strict_plain_qeps_half_gamma_$gamma.pkl"
	if test -f "$FILE"; then
    	rm "$FILE"
	fi
	FILE="./full_data/strict_plain_qeps_half_gamma_$gamma.pkl"
	if test -f "$FILE"; then
    	rm "$FILE"
	fi
	FILE="./full_data/strict_plain_qeps_gamma_$gamma.pkl"
	if test -f "$FILE"; then
    	rm "$FILE"
	fi
done

for gamma in "${array[@]}"
do
echo "run gamma = $gamma"	
cd half_data/

sed -i "s/self.gamma = 1/self.gamma = $gamma/g" "node.py"
FILE="strict_plain_qeps_half_gamma_$gamma.pkl"

echo 'pretrain QEP-S on half data...' 
for i in {1..100}
do
   python3 runStrictPlain_maintenance.py
done
sed -i "s/self.gamma = $gamma/self.gamma = 1/g" "node.py"
cp "$FILE" "../full_data/$FILE" 

cd ../full_data
sed -i "s/self.gamma = 1/self.gamma = $gamma/g" "node.py"
FILE="strict_plain_qeps_gamma_$gamma.pkl"

echo 'finished pretraining, evaluate QEP-S full data' 
echo 'reiterating workload over full data:'
python3 runStrictPlain_lookup.py
for i in {1..100}
do
   python3 runStrictPlain_maintenance.py
   python3 runStrictPlain_lookup.py
done
sed -i "s/self.gamma = $gamma/self.gamma = 1/g" "node.py"
cd ..

done

