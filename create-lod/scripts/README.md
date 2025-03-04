# Scripts for running the conversion from CSV to RDF

## Script dependencies

- `pandas`
- `untangle`
- `rdflib`
- `bs4`

Dependencies can be installed with `pip`, e.g.,
```
pip install pandas
```

## Running the scripts

There are two ways to run the scripts:

### run_conversion.py

All scripts can be run with `run_conversion.py`:

```
python run_conversion.py
```

This will run all the `convert_[type_of_instance].py` scripts to handle each of the CSV files in the `../csv` folder.

The created Turtle files will be serialized in the folder `ttl/` one directory up.

### run_conversion.ipynb

An alternative to running the above `run_conversion.py` in a Jupyter Notebook format.

Running this notebook will install all the necessary dependencies and run all the `convert_[type_of_instance].py` scripts to handle each of the CSV files in the `../csv` folder.

The created Turtle files will be serialized in the folder `ttl/` one directory up.