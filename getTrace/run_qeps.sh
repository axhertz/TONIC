
#!/bin/bash

#Plain QEP-S
echo '### plain QEP-S:'
cd plainQEPS/
python3 runPlain_maintenance.py
python3 runPlain_lookup.py


#Filter Aware
echo '### filter-aware QEP-S:'
cd ../filterAwareQEPS/
python3 runFilterAware_maintenance.py
python3 runFilterAware_lookup.py

