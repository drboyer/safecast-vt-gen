# TODO: add "all" directive
# all:
#

docker-build:
	@docker build -t safecast-spark .

# TODO: add directive to download the latest daily export into the data/ directory
# download:
#

# renders the dail export into a series of geojson files
# TODO: don't hardcode the file to use into create_geojson.py!
render-measurements-geojson:
	@docker run -p 4040:4040 -v $$(pwd)/data:/data safecast-spark:latest spark-submit --total-executor-cores 10 create_geojson-raw_measurements.py

render-mclean-geojson:
	@docker run -p 4040:4040 -v $$(pwd)/data:/data safecast-spark:latest spark-submit --total-executor-cores 10 create_geojson-mclean.py

# creates an mbtiles vector tile set from the geojson files output by the Spark job
# TODO: parameterize this with the date as well?
create-measurements-mbtiles:
	@tippecanoe -o data/measurements-20180828.mbtiles -z 10 -as -P -l bgeigie-measurements data/measurements-20180828-geojson/*.txt

create-mclean-mbtiles:
	@tippecanoe -o data/mclean.mbtiles -z 10 -as -P -l bgeigie-measurements data/mclean-geojson/*.txt
