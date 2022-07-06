
#!/bin/bash
trap "exit" INT
echo "+++ run time and size experiment +++"
cd C++
bash run_qeps.sh

echo "+++ run data shift experiment +++"
cd ../dataShift
bash run_qeps.sh

echo "+++ run adaptivity experiment +++"
cd ../adaptivity
bash run_qeps.sh


echo "+++ run prefix reutilization experiment +++"
cd ../prefixReutilization
bash run_qeps.sh

echo "+++ run gamma experiment +++"
cd ../gamma
bash run_qeps.sh


#echo "+++ run index rating experiment +++"
#cd ../indexAdvisor
#bash run_qeps.sh
