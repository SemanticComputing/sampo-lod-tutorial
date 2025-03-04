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

### run_conversion.py / run_conversion.sh

If you have all the dependencies installed, all scripts can be run with `run_conversion.py`:

```
python run_conversion.py
```

This will run all the `convert_[type_of_instance].py` scripts to handle each of the CSV files in the `../csv` folder.

You can also run the shell script `run_conversion.sh`, which first installs the dependencies and then runs the above Python script:

```
./run_conversion.sh
```

*Running the shell script requires the file to have execute (x) permission (Properties > Permissions).*

The created Turtle files will be serialized in the folder `ttl/` one directory up.

### run_conversion.ipynb

An alternative to running the above `run_conversion.py` in a Jupyter Notebook format.

Running this notebook will install all the necessary dependencies and run all the `convert_[type_of_instance].py` scripts to handle each of the CSV files in the `../csv` folder.

The created Turtle files will be serialized in the folder `ttl/` one directory up.