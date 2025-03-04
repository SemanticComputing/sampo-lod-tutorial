# create-lod

## Data

The data in the CSVs is based on the data in [OperaSampo — Opera and music theatre performances in Finland 1830–1960](https://www.ldf.fi/dataset/operasampo) (Licensed under CC BY 4.0, Licensor: Taideyliopisto, Semanttisen laskennan tutkimusryhmä (SeCo)).

## Folders

### csv/

Folder containing all the original data used in the conversion process in CSV format:

- `foc_Composition.csv`: File for all the compositions and their information.
- `foc_CompositionLibretist.csv`: File for linking libretists (persons) to compositions.
- `foc_CompositionRole.csv`: File for all the composition role characters and their information.
- `foc_Performance.csv`: File for all the performances and their information.
- `foc_PerformanceRole.csv`: File for all linking performers, their role characters and performances to each other
    - e.g., Dumani G. performed in the role "Remigio" in the performance "La Navarraise (1896-10-31)"
- `foc_Person.csv`: File for all the people and their information.
- `foc_Place.csv`: File for all the performance venues and their information.
- `foc_Producer.csv`: File for all the producers and their information.

### scripts/

Folder containing the scripts for the conversion process. 
The running instructions for the scripts are contained inside the folder.

### ttl/

Folder for all the Turtle-serialized files created in the conversion process.

## Fuseki setup

### Build Fuseki container for publishing the data

`docker build -t dhnb-opera-fuseki .`

### Run

`docker run -d -p 3048:3030 --name dhnb-opera dhnb-opera-fuseki`

Get the Fuseki control panel password with `docker logs dhnb-opera`

The Fuseki control panel will be available at: http://localhost:3048/

### Upgrade

```
docker build -t dhnb-opera-fuseki .
docker stop dhnb-opera
docker rm dhnb-opera
docker run -d -p 3048:3030 --restart unless-stopped --name dhnb-opera dhnb-opera-fuseki
```