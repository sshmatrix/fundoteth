# fundoteth

## Eligibility for Fun?

- 1000+ compute nodes

- HTCondor Cluster Manager installed on headnode

## Test Fun

- Install `python3` [[Source](https://www.python.org/downloads/)]

- Install dependencies: `pip install -r dependencies.log`

- Run `./genDag.sh`

- Run `condor_submit_dag -maxidle <some value> dag.dag`

- Listen for success: `./check.sh`
