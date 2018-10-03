# safecast-vt-gen

Render a Mapbox vector tileset from Safecast Radiation data. Takes a [daily export](https://github.com/Safecast/safecastapi/wiki/Data-Sets#daily-export)
of all the Safecast radiation data (~12 GB download) and turns it into a single .mbtiles file
that can be uploaded to [Mapbox](https://www.mapbox.com) and visualized on a map.

## Background

### What is Safecast?

Safecast is a fully open citizen-science program created after the March 2011 earthquake in Japan
to collect radiation data. Over several iterations in hardware/software design, other environmental
observations like temperature and particulate matter (air quality) are also collected.

More details at https://blog.safecast.org/.

## Architecture

TODO: add diagram

Data is downloaded locally, ETL'd into a set of line-delimited GeoJSON files using Apache Spark running in
a Docker container, then processed into a packaged set of vector tile (.mbtiles file) using [tippecanoe](https://github.com/mapbox/tippecanoe).

## Resources

TODO: Add more

- [Safecast Data Sets](https://github.com/Safecast/safecastapi/wiki/Data-Sets)