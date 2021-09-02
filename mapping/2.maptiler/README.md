# how-to

1. Download data,

```bash
# https://data.maptiler.com/downloads/asia/malaysia-singapore-brunei/, link only valid for 1 hour
# so you need to manual copy and paste the link
wget -c https://data.maptiler.com/download/WyIxNjllYjYxMC1jZmRiLTRiMmItODc5Zi0wN2Q5ZmY2MmQzMTciLCItMSIsODg2OF0.YTBqtg.2nQR7hksDwdxVE3-cEqc_xf3WqA/maptiler-osm-2017-07-03-v3.6.1-asia_malaysia-singapore-brunei.mbtiles?usage=personal -O maptiler-osm-2017-07-03-v3.6.1-asia_malaysia-singapore-brunei.mbtiles

# https://data.maptiler.com/maps/?msii=351bead2-e3f8-4a7d-888e-0809677f6824
wget https://data.maptiler.com/download/WyIxNjllYjYxMC1jZmRiLTRiMmItODc5Zi0wN2Q5ZmY2MmQzMTciLCItMSIsMjEyOTld.YTBtZw.67xrBsgGbeZHJ5lDtBN5puDv6JM/maptiler-server-map-styles-3.12.zip
mkdir data
unzip maptiler-server-map-styles-3.12.zip
cp -r maptiler-server-map-styles-3.12/* data
cp maptiler-osm-2017-07-03-v3.6.1-asia_malaysia-singapore-brunei.mbtiles data/maptiler-osm.mbtiles
```

2. Serve server,

```bash
WORK_DIR=$PWD/data docker run -d -p 3650:3650 -v $WORK_DIR:$WORK_DIR maptiler/server --workDir=$WORK_DIR --withAdmin=false
```

3. Visit map,

```bash
http://localhost:3650/api/maps/basic#11.17/2.9912/101.669
```

<img src="selangor.png" width="20%">