
## Data

The data in the CSVs is based on the data in [OperaSampo — Opera and music theatre performances in Finland 1830–1960](https://www.ldf.fi/dataset/operasampo) (Licensed under CC BY 4.0, Licensor: Taideyliopisto, Semanttisen laskennan tutkimusryhmä (SeCo)).

## Build Fuseki container for publishing the data

`docker build -t dhnb-opera-fuseki .`

## Run

`docker run -d -p 3048:3030 --name dhnb-opera dhnb-opera-fuseki`

Get the Fuseki control panel password with `docker logs dhnb-opera`

## Upgrade

```
docker build -t dhnb-opera-fuseki .
docker stop dhnb-opera
docker rm dhnb-opera
docker run -d -p 3048:3030 --restart unless-stopped --name dhnb-opera dhnb-opera-fuseki
```