
#!/bin/bash
trap "exit" INT
#Plain QEP-S
echo '### plain QEP-S:'
cd ./halfData/plainQEPS/

echo 'half data -- plain:'
python3 runStrictPlain_maintenance.py
python3 runStrictPlain_lookup.py

cd ../../fullData/plainQEPS

echo 'full data -- plain:'
python3 runStrictPlain_maintenance.py full_data
python3 runStrictPlain_lookup.py full_data


echo 'data shift -- plain:'
python3 runStrictPlain_maintenance.py half_data
python3 runStrictPlain_lookup.py half_data

cd ../..

#Selectivity Aware
echo '### selectivity-aware QEP-S:'
cd ./halfData/selAwareQEPS/

echo 'half data -- sel.-aware:'
python3 runStrictSel_maintenance.py
python3 runStrictSel_lookup.py

cd ../../fullData/selAwareQEPS/

echo 'full data -- sel.-aware:'
python3 runStrictSel_maintenance.py full_data
python3 runStrictSel_lookup.py full_data

echo 'data shift sel.-aware:'
python3 runStrictSel_maintenance.py half_data
python3 runStrictSel_lookup.py half_data



cd ../..
echo '### filter-aware QEP-S:'
#Filter Aware
cd ./halfData/filterAwareQEPS/

echo 'half data -- filter-aware:'
python3 runStrictFilter_maintenance.py
python3 runStrictFilter_lookup.py

cd ../../fullData/filterAwareQEPS

echo 'full data -- filter-aware:'
python3 runStrictFilter_maintenance.py full_data
python3 runStrictFilter_lookup.py full_data


echo 'data shift -- filter-aware:'
python3 runStrictFilter_maintenance.py half_data
python3 runStrictFilter_lookup.py half_data


