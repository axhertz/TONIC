
#!/bin/bash

echo "plain QEPS"
cd plainQEPS
python3 runStrictPlain_maintenance.py

echo "selectivity-aware QEPS"
cd ../selAwareQEPS
python3 runStrictSel_maintenance.py

echo "filter-aware QEPS"
cd ../filterAwareQEPS
python3 runStrictFilter_maintenance.py