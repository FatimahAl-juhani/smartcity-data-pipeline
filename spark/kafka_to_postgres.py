from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

# --------------------------------------------------
# Spark Session
# --------------------------------------------------
spark = (
    SparkSession.builder
    .appName("KafkaToPostgres")
    # IMPORTANT: checkpoint must be writable inside container
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints/smartcity")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# --------------------------------------------------
# Kafka message schema
# --------------------------------------------------
schema = (
    StructType()
    .add("city", StringType())
    .add("speed", IntegerType())
    .add("congestion", IntegerType())
)

# --------------------------------------------------
# Read from Kafka
# --------------------------------------------------
kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "smartcity-kafka:9092")
    .option("subscribe", "smartcity_events")
    .option("startingOffsets", "latest")
    .option("failOnDataLoss", "false")
    .load()
)

parsed_df = (
    kafka_df
    .selectExpr("CAST(value AS STRING) AS value")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

# --------------------------------------------------
# Write each micro-batch to PostgreSQL
# --------------------------------------------------
def write_to_postgres(batch_df, batch_id):
    if batch_df.rdd.isEmpty():
        return

    (
        batch_df.write
        .format("jdbc")
        .option("url", "jdbc:postgresql://smartcity-postgres:5432/smartcity")
        .option("dbtable", "smartcity_events")
        .option("user", "smartcity")
        .option("password", "smartcity")
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )

# --------------------------------------------------
# Start Streaming Query
# --------------------------------------------------
query = (
    parsed_df.writeStream
    .foreachBatch(write_to_postgres)
    .outputMode("append")
    .start()
)

query.awaitTermination()
