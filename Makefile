# TODO: add "all" directive
# all:
#

build-docker:
	@docker build -t safecast-spark .

# TODO: add directive to download the latest daily export into the data/ directory
# download:
#

# renders the dail export into a series of geojson files
# TODO: don't hardcode the file to use into create_geojson.py!
render-geojson:
	@docker run -p 4040:4040 -v $$(pwd)/data:/data safecast-spark:latest spark-submit create_geojson.py

# creates an mbtiles vector tile set from the geojson files output by the Spark job
# TODO: parameterize this with the date as well?
create-mbtiles:
	@tippecanoe -o data/measurements-20180828.mbtiles -z 10 -as -P -l bgeigie-measurements data/measurements-20180828-geojson/*.txt