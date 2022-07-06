
#!/bin/bash

trap "exit" INT


#Plain QEP-S
echo '### plain QEP-S:'
cd plainQEPS
echo '### start from empty QEP-S:'
python3 run.py
echo '### start from pretrained QEP-S:'
python3 run_pretrained.py
cd ..




echo '### filter-aware QEP-S:'
cd filterAwareQEPS
echo '### start from empty QEP-S:'
python3 run.py
echo '### start from pretrained QEP-S:'
python3 run_pretrained.py





