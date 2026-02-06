from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

spark = (
    SparkSession.builder
    .appName("EarthquakeKafkaStream")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("id", StringType()),
    StructField("place", StringType()),
    StructField("magnitude", DoubleType()),
    StructField("time", LongType()),
    StructField("longitude", DoubleType()),
    StructField("latitude", DoubleType())
])

kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "earthquakes")
    .option("startingOffsets", "latest")
    .load()
)

json_df = kafka_df.selectExpr("CAST(value AS STRING)")

parsed_df = json_df.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

query = (
    parsed_df.writeStream
    .format("csv")                              # ✅ THIS WAS MISSING
    .outputMode("append")
    .option("path", "output/csv")               # ✅ ACTUAL DATA LOCATION
    .option("checkpointLocation", "output/checkpoint")
    .trigger(processingTime="10 seconds")       # ✅ forces file commits
    .start()
)

print("🚀 Streaming started. Writing CSV files...")
query.awaitTermination()
