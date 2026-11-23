# Databricks notebook source
from pyspark.sql.functions import current_timestamp, col

base = "abfss://travel-events@traveldatayogesh.dfs.core.windows.net"

raw_path        = f"{base}/raw/"
schema_path     = f"{base}/autoloader/schema/travel_events/"
checkpoint_path = f"{base}/checkpoints/bronze/travel_events/"
bronze_path     = f"{base}/bronze/travel_events/"

# COMMAND ----------

# Auto Loader: reads only new JSONL files, tracked by the checkpoint
bronze_stream_df = (
    spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", schema_path)
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .load(raw_path)
        .withColumn("ingestion_time", current_timestamp())
        .withColumn("source_file", col("_metadata.file_path"))
)

# COMMAND ----------

query = (
    bronze_stream_df.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_path)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .start(bronze_path)
)
query.awaitTermination()

# COMMAND ----------

bronze_df = spark.read.format("delta").load(bronze_path)
print("Bronze count:", bronze_df.count())
bronze_df.show(5, truncate=False)