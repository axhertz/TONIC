# TONIC
Repository of the manuscript: <em>Turbo-Charging SPJ Query Plans with Learned Optimal Physical Join Operator Selections</em>


VLDB'22


This repository contains scripts to evaluate core characteristics of the QEP-S. Each sub-directory contains a folder with precomputed query feedback and base-table selectivities. Filter selectivies are only used by the <em>selectivity-aware QEP-S</em>. The node implementation of the <em>plain</em> and <em>filter-aware</em> design implicitly uses [0,1] as selectivity intervall.

The <em> Quick Evaluation</em> scripts do not require any actual database connection. The steps for (re)computing the respective feedback and statistics are detailed in <em> Verbose Evaluation</em>.

## Requirements: ##
- sudo apt install build-essential cmake python3-pip libpq-dev python3-dev
- sudo pip3 install psycopg2
- sudo pip3 install glob2 


## Quick Evaluation: 

1. **Individual Experiments:** To run individual experiments use **`run_qeps.sh`** in the corresponding sub-directories. Running the experiments may require the installation of additional modules via `pip3 install`. Please run **`dataShift/run_qeps.sh`** at least once as other experiments, e.g., the adaptivity evaluation, may require a <em>pretrained</em> QEPS-S from the reduced data set.

2. **All Experiments:** To run all experiments subsequently, please execute **`run_all_experiments.sh`**.



## Verbose Evaluation: 

Recomputation of the query feedback and statistics requires the following steps:

1. **PostgreSQL:** [Install Postgres](https://www.postgresql.org/download/linux/ubuntu/) and [load the (frozen) IMDB data](https://github.com/gregrahn/join-order-benchmark).
2. **Reduced-Data:** Create another JOB instance where half the tuples from tables with at least 100k tuples are randomly dropped.
3. **Query-Feedback:** [Install the plan_hint_extension](https://github.com/ossc-db/pg_hint_plan) (see documentation [here](https://pghintplan.osdn.jp/pg_hint_plan.html)). Using the extension, execute each query with all possible physical operator combinations. For details see `utils/operatorPermutation`.
4. **Miscellaneous**: To recompute base-table selectivities for the <em>selectivity-aware</em> QEP-S, please look at `utils/selectivityDict.py`. To halt QEP-S branching for already empty join results, `utils/getIntermediateSize.py` recomputes the necessary intermediate result sizes. Lastly, filter expressions for the <em>filter-aware</em> QEP-S have been extracted according to `utils/filterDict.py`.



