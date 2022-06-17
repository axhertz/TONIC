
#!/bin/bash

trap "exit" INT
cd plainQEPS
array=( 1 0.99 0.95 0.9 0.8 0.7 0.6)
#array=( 1 )
for gamma in "${array[@]}"
do
echo "### run gamma = $gamma"
sed -i "s/self.gamma = 1/self.gamma = $gamma/g" "node.py"
python3 runPlain_maintenance.py
python3 IndexRecommendation.py
sed -i "s/self.gamma = $gamma/self.gamma = 1/g" "node.py"
done

