
#!/bin/bash

echo "plain QEPS"
cd plainQEPS
python3 runPlain_maintenance.py


echo "filter-aware QEPS"
cd ../filterAwareQEPS
python3 runFilterAware_maintenance.py