# how-to

1. Download and process data,

```bash
file=malaysia-singapore-brunei-latest
# ~174MB
wget http://download.geofabrik.de/asia/${file}.osm.pbf
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/${file}.osm.pbf
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/${file}.osrm
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/${file}.osrm
```

2. Serve backend,

```bash
file=malaysia-singapore-brunei-latest
docker run -d -t -i -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/${file}.osrm
```