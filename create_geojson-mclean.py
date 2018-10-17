import json
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

CSV_SCHEMA = StructType([
    StructField('id', IntegerType(), False),
    StructField('user_id', IntegerType(), False),
    StructField('captured_time', TimestampType(), False),
    StructField('latitude', FloatType(), False),
    StructField('longitude', FloatType(), False),
    StructField('value', FloatType(), False),
    StructField('unit', StringType(), False),
    StructField('device_id', IntegerType(), True)
])

def to_geojson(row):
    feature = {
        'type': 'Feature',
        'properties': {
            'value': row.value,
            'unit': row.unit,
            'orig_value': row.orig_value,
            'orig_unit': row.orig_unit,
            'observation_time': row.captured_time.isoformat(),
            'observation_timestamp': int("{:%s}".format(row.captured_time)),
            'device_id': row.device_id
        },
        'geometry': {
            'type': 'Point',
            'coordinates': [row.longitude, row.latitude]
        }
    }
    return json.dumps(feature)

def convert_units(row):
    row_dict = row.asDict()

    # keep original value and units
    row_dict['orig_value'] = row_dict['value']
    row_dict['orig_unit'] = row_dict['unit']

    # convert all units to usv
    if row_dict['unit'] == 'cpm':
        # bGeigies
        if row_dict['device_id'] == None:
            row_dict['value'] = row_dict['value'] * 0.0029940119760479
        elif row_dict['device_id'] in (5,15,16,17,18,22,69,89):
            row_dict['value'] = row_dict['value'] * 0.0028571428571429
        elif row_dict['device_id'] in (6,7,11,13,23):
            row_dict['value'] = row_dict['value'] * 0.01
        elif row_dict['device_id'] in (4,9,10,12,19,24):
            row_dict['value'] = row_dict['value'] * 0.0075757575757576
        elif row_dict['device_id'] == 21:
            row_dict['value'] = row_dict['value'] * 0.0005714285714285714

    row_dict['unit'] = 'usv'

    return Row(**row_dict)

def main():
    spark = SparkSession.builder.appName('stuff').getOrCreate()
    csv_df = spark.read.csv('/data/mclean-out.csv', header=True, schema=CSV_SCHEMA)
    converted_units_rdd = csv_df.rdd.map(convert_units)
    geojson_rdd = converted_units_rdd.map(to_geojson)
    geojson_df = spark.createDataFrame(geojson_rdd, StringType())
    geojson_df.write.text('/data/mclean-geojson-1/')

if __name__ == '__main__':
    main()
