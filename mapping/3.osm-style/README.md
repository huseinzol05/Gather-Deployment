# how-to

1. Download data,

```bash
mkdir data
file=malaysia-singapore-brunei-latest.osm.pbf
wget https://download.geofabrik.de/asia/${file}
docker run -v $PWD/${file}:/data.osm.pbf -v $PWD/data:/var/lib/postgresql/12/main overv/openstreetmap-tile-server:1.3.10 import
```

2. Serve backend,

```
mkdir data-tile
docker run -p 8080:80 \
-v $PWD/data:/var/lib/postgresql/12/main \
-v $PWD/data-tile:/var/lib/mod_tile \
overv/openstreetmap-tile-server:1.3.10 run
```

3. Visit map,

```bash
http://localhost:8080/
```