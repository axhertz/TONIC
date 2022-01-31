
#!/bin/bash

#Plain QEP-S
echo '### plain QEP-S:'
cd plainQEPS/
python3 runStrictPlain_maintenance.py
python3 runStrictPlain_lookup.py

#Selectivity Aware
echo '### selectivity-aware QEP-S:'
cd ../selAwareQEPS/
python3 runStrictSel_maintenance.py
python3 runStrictSel_lookup.py

#Filter Aware
echo '### filter-aware QEP-S:'
cd ../filterAwareQEPS/
python3 runStrictFilter_maintenance.py
python3 runStrictFilter_lookup.py

