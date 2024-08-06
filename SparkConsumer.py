from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json,lit,when
from define_schema import schema_air_quality,schema_journey,schema_environmental_temperature,schema_motion,schema_sensor
from pyspark.sql.types import StructType, StructField, StringType, FloatType, BooleanType, IntegerType, ArrayType
import random
import time

# nen bo vao file .env, day la demo

kafka_bootstrap_servers = 'pkc-p11xm.us-east-1.aws.confluent.cloud:9092'
kafka_username = 'BQCIJS2RHPEQGJJZ' 
kafka_password = '7Zg7mbMRLR4dNhIof/b/JhfH/tqxS54HBNmtea5awim21zdnhsaqw2ail+f3zv7Z'

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .master("spark://172.24.0.3:7077") \
    .getOrCreate()


# doc nhieu topic trong kafka
def read_topic(topic,schema): 
    return (
    spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", topic) \
        .option("kafka.security.protocol", "SASL_SSL") \
        .option("kafka.sasl.mechanism", "PLAIN") \
        .option("kafka.sasl.jaas.config", f'org.apache.kafka.common.security.plain.PlainLoginModule required username="{kafka_username}" password="{kafka_password}";') \
        .load()\
        .selectExpr("CAST(value AS STRING) as json_value") \
        .select(from_json(col("json_value"), schema).alias("data")) \
        .select("data.*")
)       

journey_df = read_topic('topic0',schema_journey)
sensor_df = read_topic("topic1",schema_sensor)
motion_df = read_topic("topic2",schema_motion)
air_df = read_topic("topic3",schema_air_quality)
enviroment_df = read_topic("topic4",schema_environmental_temperature)


def random_temperature():
    return round(random.uniform(15.0, 30.0), 2)

def random_humidity():
    return round(random.uniform(30.0, 90.0), 2)

def random_pressure():
    return round(random.uniform(950.0, 1050.0), 2)

def handle_invalid_data(df):
    if 'temperature' in df.columns:
        df = df.withColumn(
            "temperature",
            when(col("temperature") == "invalid_temperature", lit(random_temperature()))
            .otherwise(
                when(col("temperature").cast(FloatType()).between(15, 30.0), col("temperature").cast(FloatType()))
                .otherwise(lit(random_temperature()))
            )
        )
    
    if 'humidity' in df.columns:
        df = df.withColumn(
            "humidity",
            when(col("humidity") == "invalid_humidity", lit(random_humidity()))
            .otherwise(
                when(col("humidity").cast(FloatType()).between(30.0, 90.0), col("humidity").cast(FloatType()))
                .otherwise(lit(random_humidity()))
            )
        )
    
    if 'pressure' in df.columns:
        df = df.withColumn(
            "pressure",
            when(col("pressure") == "invalid_pressure", lit(random_pressure()))
            .otherwise(
                when(col("pressure").cast(FloatType()).between(950.0, 1050.0), col("pressure").cast(FloatType()))
                .otherwise(lit(random_pressure()))
            )
        )
    df = df.dropna()
    return df    
sensor_df = handle_invalid_data(sensor_df)
air_df = handle_invalid_data(air_df)
motion_df = handle_invalid_data(motion_df)
enviroment_df = handle_invalid_data(enviroment_df)
journey_df = handle_invalid_data(journey_df)

jdbc_url = "jdbc:postgresql://postgres:5432/airflow"
jdbc_properties = {
    "user": "airflow",
    "password": "airflow",
    "driver": "org.postgresql.Driver"
}
def WriteDataToTimeScale(df,table,checkpoint):
    query =df.writeStream \
        .outputMode("append") \
        .foreachBatch(lambda batch_df, epoch_id: batch_df.write.jdbc(
            url=jdbc_url,
            table=table,
            mode="append",
            properties=jdbc_properties
        )) \
        .option("checkpointLocation",  f"/app/checkpoint/{checkpoint}") \
        .start()
    return query
    

queries = [
    WriteDataToTimeScale(journey_df, "livedatabase.journey", "JourneyCheckPoint"),
    WriteDataToTimeScale(sensor_df, "livedatabase.sensor", "SensorCheckpoint"),
    WriteDataToTimeScale(air_df, "livedatabase.air_quality", "AirCheckPoint"),
    WriteDataToTimeScale(motion_df, "livedatabase.motion", "MotionCheckpoint"),
    WriteDataToTimeScale(enviroment_df, "livedatabase.environmental_temperature", "EnvironmentCheckpoint")
]

# Chờ tất cả các luồng dữ liệu hoàn tất
for query in queries:
    query.awaitTermination()