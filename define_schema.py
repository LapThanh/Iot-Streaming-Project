from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, BooleanType, IntegerType, ArrayType,DoubleType,TimestampType
from pyspark.sql.functions import col, from_json

schema_journey = StructType() \
    .add("device_id", StringType()) \
    .add("timestamp", TimestampType()) \
    .add("location",ArrayType(DoubleType())) \
    .add("speed", FloatType()) \
    .add("direction", StringType()) \
    .add("make", StringType()) \
    .add("model", StringType()) \
    .add("year", IntegerType()) \
    .add("fuelType", StringType())    

schema_sensor = StructType() \
    .add("device_id", StringType()) \
    .add("temperature", StringType()) \
    .add("humidity", StringType()) \
    .add("pressure", StringType()) \
    .add("battery_status", StringType()) \
    .add("location", ArrayType(DoubleType())) \
    .add("timestamp", TimestampType())

schema_motion = StructType() \
    .add("device_id", StringType()) \
    .add("motion_detected", BooleanType()) \
    .add("temperature", StringType()) \
    .add("battery_level", FloatType()) \
    .add("location", ArrayType(DoubleType())) \
    .add("device_status", StringType()) \
    .add("timestamp", TimestampType())

schema_air_quality = StructType() \
    .add("device_id", StringType()) \
    .add("pm2_5", FloatType()) \
    .add("pm10", FloatType()) \
    .add("co2_level", FloatType()) \
    .add("temperature", StringType()) \
    .add("air_quality_index", FloatType()) \
    .add("location", ArrayType(DoubleType())) \
    .add("timestamp", TimestampType())

schema_environmental_temperature = StructType() \
    .add("device_id", StringType()) \
    .add("temperature", StringType()) \
    .add("humidity", StringType()) \
    .add("dew_point", FloatType()) \
    .add("heat_index", FloatType()) \
    .add("location", ArrayType(DoubleType())) \
    .add("timestamp", TimestampType())