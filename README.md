# Sampo LOD tutorial

Auxiliary files for the Sampo LOD tutorial.

## create-lod

The folder `create-lod` has the relevant files for the part "Creating LOD from databases".

### Contents

- `csv`: A folder containing CSV files with example data to be used for data transformation.
- `scripts`: A folder containing Python scripts that convert the CSV data from the folder above into Turtle-serialized RDF.
- `ttl`: A folder containing the output files from the conversion.
- `Dockerfile` and `assembler.ttl` for running the data on a local Fuseki SPARQL server using Docker
    - Instructions for building and running in the README inside the `create-lod` folder

## set-up-sampo-ui

The folder `set-up-sampo-ui` has the relevant files for the part "Creating a semantic portal easily using Sampo-UI".

### Contents

- Sampo-UI configuration for the data created in `create-lod` with a local Fuseki SPARQL server running on port 3048 as specified in the Docker instructions in `create-lod`
    - **Requirements:** Node.js® (version 16.13.0), Nodemon
    - On first start, you'll need to install all the Node modules used by Sampo-UI. This can be done by running the command `npm install` in the `set-up-sampo-ui` folder.
    - The application is run with `npm run dev` in the `set-up-sampo-ui` folder.
