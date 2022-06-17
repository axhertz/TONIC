
#!/bin/bash
trap "exit" INT
#Plain QEP-S
echo '### plain QEP-S:'
cd ./reducedData/plainQEPS/


echo 'reduced data -- plain:'
python3 runPlain_maintenance.py
python3 runPlain_lookup.py

cd ../../fullData/plainQEPS

echo 'full data -- plain:'
python3 runPlain_maintenance.py full_data
python3 runPlain_lookup.py full_data

echo 'data shift -- plain:'
python3 runPlain_maintenance.py reduced_data
python3 runPlain_lookup.py reduced_data
cd ../..



echo '### filter-aware QEP-S:'
#Filter Aware
cd ./reducedData/filterAwareQEPS/

echo 'half data -- filter-aware:'
python3 runFilterAware_maintenance.py
python3 runFilterAware_lookup.py


cd ../../fullData/filterAwareQEPS

echo 'full data -- filter-aware:'
python3 runFilterAware_maintenance.py full_data
python3 runFilterAware_lookup.py full_data

echo 'data shift -- filter-aware:'
python3 runFilterAware_maintenance.py reduced_data
python3 runFilterAware_lookup.py reduced_data

