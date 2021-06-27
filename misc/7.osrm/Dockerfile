FROM osrm/osrm-backend AS base

ADD http://download.geofabrik.de/asia/malaysia-singapore-brunei-latest.osm.pbf /data/malaysia-singapore-brunei-latest.osm.pbf

RUN osrm-extract -p /opt/car.lua /data/malaysia-singapore-brunei-latest.osm.pbf

RUN osrm-partition /data/malaysia-singapore-brunei-latest.osrm

RUN osrm-customize /data/malaysia-singapore-brunei-latest.osrm

ENTRYPOINT osrm-routed --algorithm mld /data/malaysia-singapore-brunei-latest.osrm

