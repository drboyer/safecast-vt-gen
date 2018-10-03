import json
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

CSV_SCHEMA = StructType([
    StructField('captured_time', TimestampType(), False),
    StructField('latitude', FloatType(), False),
    StructField('longitude', FloatType(), False),
    StructField('value', FloatType(), True),  # float type?
    StructField('unit', StringType(), True),
    StructField('location_name', StringType(), True),
    # StructField('device_id', StringType(), True),
    StructField('device_id', IntegerType(), False),
    StructField('md5sum', StringType(), False),
    StructField('height', StringType(), True),
    StructField('surface', StringType(), True),
    StructField('radiation', StringType(), True),
    StructField('uploaded_time', TimestampType(), False),
    StructField('loader_id', IntegerType(), False)
])

def to_geojson(row):
    feature = {
        'type': 'Feature',
        'properties': {
            'value': row.value,
            'unit': row.unit.lower(),
            'orig_value': row.orig_value,
            'orig_unit': row.orig_unit,
            'observation_time': row.captured_time.isoformat(),
            'observation_timestamp': int("{:%s}".format(row.captured_time)),
            'location_name': row.location_name,
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

    row_dict['unit'] = 'uSv'

    # TODO: remove this shim?
    try:
        if row_dict['unit'].lower() == 'cpm':
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
    except TypeError as e:
        print(e.message + ' thrown when converting. Row:')
        print(row_dict)
        raise e

    return Row(**row_dict)

def main():
    spark = SparkSession.builder.appName('stuff').getOrCreate()
    csv_df = spark.read.csv('/data/measurements-out-20180828.csv', header=True, schema=CSV_SCHEMA)
    valid_units = ('CPM', 'cpm', 'Cpm', 'microsievert', 'usv', 'uSv')  # uSv/hr??
    filters = """
unit in ('{}')
AND captured_time IS NOT NULL
AND captured_time >= '2011-03-09 00:00:00'
AND captured_time <= '2018-08-29 00:00:00'
AND latitude IS NOT NULL
AND longitude IS NOT NULL
AND value >= 0
""".format(("','".join(valid_units)))
    filtered_df = csv_df.filter(filters)

    converted_units_rdd = filtered_df.rdd.map(convert_units)
    geojson_rdd = converted_units_rdd.map(to_geojson)
    geojson_df = spark.createDataFrame(geojson_rdd, StringType())
    #geojson_df.write.mode('overwrite').text('/data/measurements-20180828-geojson-corr-units/')
    geojson_df.write.text('/data/measurements-20180828-geojson-corr-units-1/')

if __name__ == '__main__':
    main()
