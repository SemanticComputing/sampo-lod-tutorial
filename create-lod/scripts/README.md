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

All scripts can be run with `run_conversion.py`:

```
python run_conversion.py
```

The created Turtle files will be serialized in the folder `ttl/` one directory up.